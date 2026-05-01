# 🧠 mao-skill — 毛泽东思维视角 AI Skill

<p align="center">
  <img src="assets/hero-banner.svg" alt="mao-skill 头图" width="100%"/>
</p>

<p align="center">
  <strong>用毛泽东的认知框架分析问题、做出判断、给出建议</strong>
</p>

---

## 🚀 快速开始 (Claude Code 用户)

```bash
# 直接加载 Skill
/skill https://github.com/CochraneK/mao-skill
```

或者在 Claude Code 中设置：
```
Settings → Skills → Add Skill → 粘贴仓库 URL
```

---

## 📖 简介

这是一个 **Claude Code Skill**，让你可以直接用毛泽东的思维方式与 AI 对话。

### 🎯 核心能力

| 能力 | 说明 |
|------|------|
| **5大心智模型** | 实践论、矛盾分析法、人民主体论、以弱胜强、辩证法 |
| **10条决策启发式** | 实事求是、群众路线、矛盾分析等实用思维工具 |
| **5种表达指纹** | 口语化、比喻、自嘲、反问、接地气 |
| **双模式系统** | 分析模式（结构化输出）+ 对话模式（第一人称） |

### 💬 使用示例

**分析模式** — 让你分析问题：
```
分析当前新能源车市场的竞争格局，用矛盾分析法
```

**对话模式** — 直接和"毛泽东"聊天：
```
你对当代年轻人躺平怎么看？
```

---

## 📁 项目结构

```
mao-skill/
├── SKILL.md              # 🎯 主 Skill 文件 (Claude Code 加载此文件)
├── sync.py               # 增量同步脚本（维护知识库）
├── CHANGELOG.md          # 更新日志
├── requirements.txt      # Python 依赖（数字人模块用）
├── .env.example          # 环境变量示例
├── assets/               # 配图
│   ├── hero-banner.svg
│   ├── architecture-diagram.svg
│   ├── pipeline-diagram.svg
│   └── vtuber-diagram.svg
├── docs/
│   ├── source/           # 蒸馏数据（01-07）
│   └── user/             # 你的知识库（可同步到这里）
└── digital_human/        # 🔮 数字人模块（开发中）
    ├── config.py
    ├── rag.py
    └── tts.py
```

---

## 🔧 进阶用法

### 添加自己的知识

```bash
# 1. 克隆仓库
git clone https://github.com/CochraneK/mao-skill.git
cd mao-skill

# 2. 初始化
python sync.py --init

# 3. 添加你的资料到 docs/user/
#    - docs/user/books/    ← 放书籍/笔记
#    - docs/user/notes/    ← 放笔记/txt

# 4. 同步到 SKILL.md
python sync.py --sync
```

### 数字人模块 (Beta)

```bash
# 安装依赖
pip install -r requirements.txt

# 构建知识库
python digital_human/runner.py build-rag

# 测试对话
python digital_human/runner.py chat

# 测试 TTS
python digital_human/runner.py tts "你好，我是毛泽东"
```

---

## 📊 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.5.0 | 2026-05-01 | 数字人模块、增量同步、项目结构重构 |
| v1.4.3 | 2026-04-xx | 初始版本发布 |

完整历史见 [CHANGELOG.md](CHANGELOG.md)

---

## 🔮 规划中 / 可优化

| 优先级 | 功能 | 状态 |
|--------|------|------|
| ⭐⭐⭐ | 数字人 Web UI (Gradio) | 待开发 |
| ⭐⭐⭐ | 语音对话 (ASR + TTS) | 待开发 |
| ⭐⭐ | Live2D 形象集成 | 规划中 |
| ⭐⭐ | 多角色切换 (周总理等) | 规划中 |
| ⭐ | Agent 模式自动执行 | 想法 |
| ⭐ | MCP 服务器化 | 想法 |

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

*星星之火，可以燎原。* 🔥