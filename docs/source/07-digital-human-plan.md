# 📚 数字人知识库集成方案

## 一、目标架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户交互                              │
│              (语音/文字 → 数字人回复)                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     mao-skill 对话系统                        │
│  • 分析模式 (结构化输出)                                       │
│  • 对话模式 (第一人称) ← 数字人使用这个                         │
│  • Persona: 毛泽东思维框架                                    │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│     RAG 知识库           │     │     记忆系统             │
│  • docs/user/ 内容       │     │  • 对话历史              │
│  • 向量检索              │     │  • 用户画像              │
│  • 来源追溯              │     │  • 上下文管理            │
└─────────────────────────┘     └─────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│                      数字人输出                               │
│  ┌─────────────────┐        ┌─────────────────┐             │
│  │  TTS 语音合成   │        │  Live2D 形象    │             │
│  │  CosyVoice2    │        │  表情/动作      │             │
│  │  benjamin 音色 │        │  唇形同步       │             │
│  └─────────────────┘        └─────────────────┘             │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、组件选型

### 1. RAG 知识库

| 方案 | 特点 | 推荐度 |
|------|------|--------|
| **LangChain + ChromaDB** | 轻量本地部署，免费 | ⭐⭐⭐⭐⭐ |
| RAGFlow | 效果好，但需Docker | ⭐⭐⭐⭐ |
| QAnything | 网易出品，易用 | ⭐⭐⭐⭐ |

**推荐**: LangChain + ChromaDB（轻量、免费、可定制）

### 2. TTS 语音

| 方案 | 特点 | 推荐度 |
|------|------|--------|
| **CosyVoice2** | 效果好，需付费 | ⭐⭐⭐⭐⭐ |
| **ChatTTS** | 免费开源，对话自然 | ⭐⭐⭐⭐⭐ |
| EdgeTTS | 免费微软，效果一般 | ⭐⭐⭐ |

**推荐**: ChatTTS（免费）或 CosyVoice2（效果更好）

### 3. 数字人形象

| 方案 | 特点 | 推荐度 |
|------|------|--------|
| **Live2D** | 主流2D虚拟形象 | ⭐⭐⭐⭐⭐ |
| SadTalker | 静态图生成视频 | ⭐⭐⭐ |
| EasyAIVTuber | 开源VTuber | ⭐⭐⭐ |

**推荐**: Live2D 模型 + 配套引擎

---

## 三、集成方案

### 方案A: 轻量级（推荐）

```
成本: 免费
部署: 本地 Python
效果: ⭐⭐⭐⭐
```

组件：
- LLM: Claude API / GPT / 通义
- RAG: LangChain + ChromaDB
- TTS: ChatTTS (开源免费)
- 形象: Live2D 模型

### 方案B: 专业级

```
成本: ¥200+/月
部署: 云服务
效果: ⭐⭐⭐⭐⭐
```

组件：
- LLM: Claude API
- RAG: RAGFlow (云)
- TTS: CosyVoice2 (付费)
- 形象: Live2D + 专业引擎

---

## 四、实施步骤

### 第一步：RAG 知识库接入

```python
# 1. 安装依赖
pip install langchain chromadb langchain-community

# 2. 构建向量库
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import Chroma

# 加载 docs/user/ 内容
loader = DirectoryLoader("docs/user/", glob="**/*.md")
docs = loader.load()

# 分割文本
splitter = MarkdownHeaderTextSplitter()
splits = splitter.split_documents(docs)

# 创建向量库
vectorstore = Chroma.from_documents(splits, embeddings)
```

### 第二步：对话系统

```python
# 使用 mao-skill 的对话模式 persona
SYSTEM_PROMPT = """你是毛泽东...
对话模式特点：
- 第一人称"我"
- 口语化、有幽默感
- 善用比喻
- 时而自嘲
"""

# RAG 检索
query = user_input
docs = vectorstore.similarity_search(query, k=3)
context = "\n".join([d.page_content for d in docs])

# 构建 prompt
full_prompt = f"{SYSTEM_PROMPT}\n\n参考知识:\n{context}\n\n用户: {query}"
```

### 第三步：语音合成

```python
# ChatTTS 示例
import ChatTTS
chat = ChatTTS.Chat()
chat.load()

text = llm_response  # 大模型回复
wav = chat.generate(text)
chat.save(wav, "output.wav")
```

### 第四步：数字人形象

```
1. 准备 Live2D 模型 (mao_pro)
2. 配置唇形同步
3. 集成表情动作库
4. 对接 TTS 音频
```

---

## 五、文件结构

```
mao-skill/
├── SKILL.md              # 对话框架
├── sync.py               # 知识库同步
├── rag/                  # RAG 模块 (新建)
│   ├── __init__.py
│   ├── vectorstore.py    # 向量库管理
│   ├── retriever.py      # 检索器
│   └── config.py         # 配置
├── digital_human/        # 数字人模块 (新建)
│   ├── __init__.py
│   ├── tts.py            # 语音合成
│   ├── avatar.py         # 形象控制
│   └── runner.py         # 运行器
└── docs/
    └── user/             # 知识库内容
        ├── books/
        ├── notes/
        └── images/
```

---

## 六、配置示例

### config.py
```python
# RAG 配置
RAG_CONFIG = {
    "vectorstore_dir": ".vectorstore",
    "embedding_model": "mxbai-embed-large",
    "top_k": 3,
}

# TTS 配置
TTS_CONFIG = {
    "engine": "chat_tts",  # 或 "cosyvoice"
    "voice": "benjamin",
    "speed": 0.9,
}

# 数字人配置
AVATAR_CONFIG = {
    "model": "mao_pro",
    "live2d_path": "./models/mao_pro.model3.json",
    "lip_sync": True,
    "expressions": ["happy", "neutral", "serious"],
}
```

---

## 七、快速开始

```bash
# 1. 安装依赖
pip install langchain chromadb chat-tts

# 2. 初始化 RAG
python -c "from rag import VectorStore; vs = VectorStore(); vs.build()"

# 3. 启动数字人
python digital_human/runner.py
```

---

## 八、进阶功能

| 功能 | 说明 |
|------|------|
| **多角色切换** | 切换不同人格（毛泽东/周恩来/等） |
| **记忆系统** | 长期记忆用户偏好 |
| **知识更新** | 自动同步 docs/user/ 新内容 |
| **语音交互** | 语音对话，而非文字 |
| **情绪识别** | 根据用户情绪调整回复风格 |

---

*持续更新中...*
*方案设计: 2026-05-01*