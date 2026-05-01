# -*- coding: utf-8 -*-
"""数字人配置"""

import os
from pathlib import Path


class Config:
    """配置类"""

    def __init__(self):
        # 项目根目录
        self.project_dir = Path(__file__).parent.parent

        # ===== LLM 配置 =====
        self.llm_provider = os.getenv("LLM_PROVIDER", "claude")  # claude/openai/qwen
        self.claude_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")

        # ===== RAG 配置 =====
        self.vectorstore_dir = self.project_dir / ".vectorstore"
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "mxbai-embed-large")
        self.top_k = 3

        # ===== TTS 配置 =====
        self.tts_engine = os.getenv("TTS_ENGINE", "chat_tts")  # chat_tts/cosyvoice/edge
        self.voice = "benjamin"
        self.speed = 0.9

        # ===== Live2D 配置 =====
        self.live2d_model = "mao_pro"
        self.live2d_path = self.project_dir / "models" / "mao_pro.model3.json"
        self.lip_sync = True

        # ===== 知识库路径 =====
        self.knowledge_dir = self.project_dir / "docs" / "user"

        # ===== 对话配置 =====
        self.max_history = 10  # 对话历史保留条数
        self.persona = self._default_persona()

    def _default_persona(self) -> str:
        """默认人格"""
        return """你是毛泽东。
- 用第一人称"我"回答
- 口语化、有幽默感
- 善用比喻（用农田、厨房里的事物打比方）
- 时而自嘲
- 必要时用反问引导对方思考
- 不掉书袋，把思想消化成自己的话说
- 短句为主，不要长篇大论"""

    def validate(self) -> bool:
        """验证配置"""
        if self.llm_provider == "claude" and not self.claude_api_key:
            print("[WARN] ANTHROPIC_API_KEY 未设置")
        return True


# 全局配置实例
config = Config()