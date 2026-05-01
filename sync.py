# -*- coding: utf-8 -*-
"""
mao-skill 增量同步系统
========================
真正的增量同步：只同步新增/修改/删除的文件
不再每次重复插入所有内容
"""
import os
import sys
import json
import hashlib
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Tuple

# Windows 编码修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


# ============== 配置 ==============
SKILL_DIR = Path(__file__).parent
SOURCE_DIR = SKILL_DIR / "docs" / "source"
USER_DIR = SKILL_DIR / "docs" / "user"
SKILL_FILE = SKILL_DIR / "SKILL.md"
INDEX_FILE = SKILL_DIR / ".sync_index.json"

# 支持的文件格式
SUPPORTED_EXTS = {'.txt', '.md', '.pdf', '.png', '.jpg', '.jpeg'}

# 章节标记
SECTION_START = "## 📚 七、知识谱系（我从哪里来）"
SECTION_END = "## 📅 八、人生里程碑"


# ============== 核心类 ==============
class SyncIndex:
    """同步索引管理器 - 记录每个文件在SKILL.md中的位置"""

    def __init__(self):
        self.data = {
            "version": "2.0",
            "last_sync": None,
            "files": {}  # {relative_path: {hash, index, title}}
        }
        if INDEX_FILE.exists():
            try:
                self.data = json.loads(INDEX_FILE.read_text(encoding='utf-8'))
            except:
                pass

    def save(self):
        self.data["last_sync"] = datetime.now().isoformat()
        INDEX_FILE.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding='utf-8')

    def get_file_state(self, relative_path: str) -> Optional[Dict]:
        return self.data["files"].get(relative_path)

    def update_file(self, relative_path: str, file_hash: str, index: int, title: str):
        self.data["files"][relative_path] = {
            "hash": file_hash,
            "index": index,
            "title": title,
            "synced_at": datetime.now().isoformat()
        }

    def remove_file(self, relative_path: str):
        if relative_path in self.data["files"]:
            del self.data["files"][relative_path]

    def get_all_files(self) -> Dict:
        return self.data.get("files", {})

    def get_sorted_files(self) -> List[Tuple[str, Dict]]:
        """获取排序后的文件列表"""
        files = self.data.get("files", {})
        return sorted(files.items(), key=lambda x: x[1].get("index", 999))


class KnowledgeSync:
    """知识库同步器 - 真正的增量同步"""

    def __init__(self):
        self.index = SyncIndex()
        self.stats = {"added": 0, "updated": 0, "deleted": 0, "unchanged": 0}

    # -------- 文件扫描 --------
    def scan_directory(self, dir_path: Path, category: str, start_index: int) -> List[Tuple[Path, str, int]]:
        """扫描目录，返回 (filepath, category, index) 列表"""
        files = []
        if not dir_path.exists():
            return files

        for i, filepath in enumerate(sorted(dir_path.rglob('*')), start=start_index):
            if not filepath.is_file():
                continue
            if filepath.suffix.lower() not in SUPPORTED_EXTS:
                continue
            if filepath.name.startswith('.') or filepath.suffix.lower() == '.py':
                continue
            files.append((filepath, category, i))

        return files

    def get_all_files(self) -> List[Tuple[Path, str, int]]:
        """获取所有需要同步的文件"""
        all_files = []

        # source: 01-06 范围
        all_files.extend(self.scan_directory(SOURCE_DIR, "source", 1))

        # user: 从07开始
        source_count = len([f for f in all_files if f[1] == "source"])
        user_start = source_count + 1
        all_files.extend(self.scan_directory(USER_DIR, "user", user_start))

        return sorted(all_files, key=lambda x: x[2])  # 按index排序

    # -------- 内容提取 --------
    def extract_content(self, filepath: Path) -> Tuple[str, str]:
        """提取文件内容"""
        suffix = filepath.suffix.lower()

        if suffix == '.txt':
            return filepath.read_text(encoding='utf-8'), "txt"
        elif suffix == '.md':
            return filepath.read_text(encoding='utf-8'), "md"
        elif suffix == '.pdf':
            return self._extract_pdf(filepath), "pdf"
        elif suffix in ['.png', '.jpg', '.jpeg']:
            return self._extract_image(filepath), "image"
        return "", "unsupported"

    def _extract_pdf(self, filepath: Path) -> str:
        try:
            import fitz
            doc = fitz.open(filepath)
            text = "\n".join([page.get_text() for page in doc])
            doc.close()
            return text
        except ImportError:
            return "[需要安装 pymupdf: pip install pymupdf]"
        except:
            return "[PDF读取失败]"

    def _extract_image(self, filepath: Path) -> str:
        try:
            from PIL import Image
            import pytesseract
            return pytesseract.image_to_string(Image.open(filepath), lang='chi_sim+eng')
        except ImportError:
            return "[需要安装 pillow pytesseract + tesseract-ocr]"
        except:
            return "[OCR识别失败]"

    # -------- 内容生成 --------
    def generate_entry(self, filepath: Path, content: str, index: int, category: str) -> str:
        """生成知识库条目"""
        title = re.sub(r'^\d+[-_\s]*', '', filepath.stem)
        suffix = filepath.suffix.lower()

        icons = {".txt": "📝", ".md": "📄", ".pdf": "📚", ".png": "🖼️", ".jpg": "🖼️", ".jpeg": "🖼️"}
        category_label = {"source": "🔧 蒸馏", "user": "👤 用户"}

        # 清理内容
        lines = [l for l in content.split('\n') if l.strip()]
        cleaned = '\n'.join(lines[:500])  # 限制行数
        if len(content.split('\n')) > 500:
            cleaned += "\n\n... [已截断] ..."

        # 移除 frontmatter
        if cleaned.startswith('---'):
            parts = cleaned.split('---', 2)
            if len(parts) >= 3:
                cleaned = parts[2]

        return f"""### {icons.get(suffix, '📄')} {index:02d}. {title}

**分类**: {category_label.get(category, '📚')} | **格式**: {suffix[1:].upper()}
**来源**: `{filepath.name}`

---

{cleaned}

---
"""

    # -------- 增量同步核心 --------
    def sync(self) -> Dict:
        """执行增量同步"""
        all_files = self.get_all_files()
        current_paths = {str(f.relative_to(SKILL_DIR)) for f, _, _ in all_files}
        indexed_paths = set(self.index.get_all_files().keys())

        # 1. 检测删除的文件
        deleted = indexed_paths - current_paths
        for path in deleted:
            self._remove_entry(path)
            self.index.remove_file(path)
            self.stats["deleted"] += 1
            print(f"  🗑️ Deleted: {os.path.basename(path)}")

        # 2. 检测新增和修改的文件
        for filepath, category, index in all_files:
            relative_path = str(filepath.relative_to(SKILL_DIR))
            file_hash = hashlib.md5(filepath.read_bytes()).hexdigest()

            old_state = self.index.get_file_state(relative_path)

            if old_state is None:
                # 新文件
                content, _ = self.extract_content(filepath)
                if content.strip():
                    self._insert_entry(filepath, content, index, category)
                    self.index.update_file(relative_path, file_hash, index, filepath.stem)
                    self.stats["added"] += 1
                    print(f"  ✅ Added: {filepath.name} [#{index:02d}]")

            elif old_state["hash"] != file_hash:
                # 文件已修改
                content, _ = self.extract_content(filepath)
                if content.strip():
                    self._update_entry(relative_path, filepath, content, index, category)
                    self.index.update_file(relative_path, file_hash, index, filepath.stem)
                    self.stats["updated"] += 1
                    print(f"  🔄 Updated: {filepath.name} [#{index:02d}]")

            else:
                self.stats["unchanged"] += 1

        self.index.save()
        return self.stats

    def _find_entry_bounds(self, title: str) -> Tuple[int, int]:
        """在SKILL.md中查找章节的起始和结束位置"""
        if not SKILL_FILE.exists():
            return -1, -1

        content = SKILL_FILE.read_text(encoding='utf-8')
        lines = content.split('\n')

        start_idx = -1
        end_idx = -1

        for i, line in enumerate(lines):
            if f"### " in line and title in line:
                start_idx = i
            if start_idx >= 0 and end_idx < 0:
                if line.strip() == '---' or (line.strip().startswith('### ') and i > start_idx):
                    end_idx = i
                    break

        return start_idx, end_idx

    def _insert_entry(self, filepath: Path, content: str, index: int, category: str):
        """插入新条目"""
        entry = self.generate_entry(filepath, content, index, category)

        if not SKILL_FILE.exists():
            print("  [ERROR] SKILL.md not found")
            return

        content_md = SKILL_FILE.read_text(encoding='utf-8')

        # 在七章和八章之间插入
        if SECTION_START in content_md and SECTION_END in content_md:
            parts = content_md.split(SECTION_START, 1)
            if len(parts) == 2:
                header = parts[0] + SECTION_START
                rest = parts[1]
                pos = header.find(SECTION_END)
                if pos > 0:
                    new_content = header[:pos] + "\n\n" + entry + "\n" + header[pos:]
                else:
                    new_content = header + "\n\n" + entry + "\n" + rest
                SKILL_FILE.write_text(new_content, encoding='utf-8')

    def _update_entry(self, relative_path: str, filepath: Path, content: str, index: int, category: str):
        """更新现有条目"""
        # 简单方案：删除旧条目，插入新条目
        self._remove_entry(relative_path)
        self._insert_entry(filepath, content, index, category)

    def _remove_entry(self, relative_path: str):
        """从SKILL.md中移除条目"""
        old_state = self.index.get_file_state(relative_path)
        if not old_state:
            return

        title = old_state.get("title", "")
        if not title:
            return

        if not SKILL_FILE.exists():
            return

        content = SKILL_FILE.read_text(encoding='utf-8')
        lines = content.split('\n')

        # 找到要删除的章节
        start_idx = -1
        end_idx = -1

        for i, line in enumerate(lines):
            if f"### " in line and title in line and f"{old_state.get('index', ''):02d}" in line:
                start_idx = i
            if start_idx >= 0 and end_idx < 0:
                if line.strip() == '---':
                    end_idx = i
                    break
                if i > start_idx and line.strip().startswith('### '):
                    # 找到下一个章节
                    for j in range(i, len(lines)):
                        if lines[j].strip() == '---':
                            end_idx = j
                            break
                    break

        if start_idx >= 0 and end_idx >= 0:
            new_lines = lines[:start_idx] + lines[end_idx+1:]
            SKILL_FILE.write_text('\n'.join(new_lines), encoding='utf-8')

    def show_status(self):
        """显示同步状态"""
        files = self.index.get_sorted_files()
        print(f"\n📚 已同步文件: {len(files)}")
        print("-" * 50)
        for path, info in files:
            icon = "🔧" if "source" in path else "👤"
            print(f"  {icon} #{info.get('index', 0):02d} {info.get('title', 'unknown')}")
        print(f"\n最后同步: {self.index.data.get('last_sync', '从未')}")


# ============== 主程序 ==============
def main():
    parser = argparse.ArgumentParser(description='mao-skill 增量同步')
    parser.add_argument('--sync', action='store_true', help='执行同步')
    parser.add_argument('--status', action='store_true', help='查看状态')
    parser.add_argument('--init', action='store_true', help='初始化目录')
    args = parser.parse_args()

    sync = KnowledgeSync()

    if args.status:
        sync.show_status()
    elif args.init:
        # 初始化目录
        SOURCE_DIR.mkdir(parents=True, exist_ok=True)
        USER_DIR.mkdir(parents=True, exist_ok=True)
        (USER_DIR / "books").mkdir(exist_ok=True)
        (USER_DIR / "notes").mkdir(exist_ok=True)
        (USER_DIR / "images").mkdir(exist_ok=True)
        print("✅ 目录初始化完成")
        print(f"   source: {SOURCE_DIR}")
        print(f"   user/:  {USER_DIR}/")
        print(f"   user/books:   {USER_DIR / 'books'}")
        print(f"   user/notes:   {USER_DIR / 'notes'}")
        print(f"   user/images:  {USER_DIR / 'images'}")
    elif args.sync:
        print("🔄 mao-skill 增量同步")
        print("=" * 50)
        stats = sync.sync()
        print("=" * 50)
        print(f"✅ 完成: 新增{stats['added']} | 更新{stats['updated']} | 删除{stats['deleted']} | 无变化{stats['unchanged']}")
    else:
        # 默认显示帮助
        parser.print_help()


if __name__ == '__main__':
    main()