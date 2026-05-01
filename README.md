# 🧠 mao-skill — 毛泽东思维视角 AI Skill

<p align="center">
  <img src="assets/hero-banner.svg" alt="mao-skill 头图" width="100%"/>
</p>

<p align="center">
  <strong>用毛泽东的认知框架分析问题、做出判断、给出建议</strong>
</p>

---

## 🚀 快速开始

```bash
# 1. 初始化
python sync.py --init

# 2. 添加你的资料到 docs/user/
#    - docs/user/books/    ← 放书籍/PDF
#    - docs/user/notes/    ← 放笔记/txt
#    - docs/user/images/   ← 放图片

# 3. 同步到 SKILL.md
python sync.py --sync

# 4. 查看状态
python sync.py --status
```

---

## 📁 项目结构

```
mao-skill/
├── SKILL.md                    # 主文件
├── sync.py                     # 增量同步脚本
├── .sync_index.json            # 同步索引（自动生成）
├── assets/                     # 配图
│   ├── hero-banner.svg
│   ├── architecture-diagram.svg
│   ├── pipeline-diagram.svg
│   └── vtuber-diagram.svg
└── docs/
    ├── source/                 # 🔧 蒸馏数据 (01-06)
    │   └── *.md
    └── user/                   # 👤 你的资料 (07+)
        ├── books/              # 书籍/PDF
        ├── notes/              # 笔记/txt
        └── images/             # 图片
```

---

## 📖 使用说明

### 添加新资料

1. 把文件放入 `docs/user/` 对应目录
2. 运行 `python sync.py --sync`
3. 内容自动增量同步到 SKILL.md

### 支持格式

| 目录 | 格式 | 说明 |
|------|------|------|
| `books/` | .md, .txt, .pdf | 书籍、文档 |
| `notes/` | .md, .txt | 笔记 |
| `images/` | .png, .jpg | 图片（OCR识别文字） |

### 增量同步特性

- ✅ **只同步变更**：新增/修改/删除的文件
- ✅ **自动编号**：source 01-06，user 从07开始
- ✅ **内容追踪**：通过 hash 检测变化
- ✅ **删除检测**：删除文件会自动从 SKILL.md 移除

---

## 🔧 命令

```bash
python sync.py --sync     # 执行同步
python sync.py --status   # 查看状态
python sync.py --init     # 初始化目录
python sync.py --tree     # 查看目录结构
```

---

## 📚 SKILL.md 结构

| 章节 | 内容 |
|------|------|
| 一~六 | 核心内容（5模型+10启发式+表达DNA等） |
| 七 | 知识谱系 ← 同步内容插入位置 |
| 八 | 人生里程碑 |

---

*星星之火，可以燎原。* 🔥