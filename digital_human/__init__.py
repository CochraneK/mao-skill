# -*- coding: utf-8 -*-
"""
mao-skill 数字人模块
=====================
语音对话 + RAG知识库 + Live2D形象

使用示例:
    from runner import DigitalHuman

    dh = DigitalHuman()
    dh.run()  # 启动对话
"""

__version__ = "0.1.0"

from .tts import TTSEngine
from .rag import KnowledgeBase
from .config import Config

__all__ = ["TTSEngine", "KnowledgeBase", "Config", "DigitalHuman"]


class DigitalHuman:
    """数字人主类"""

    def __init__(self):
        self.config = Config()
        self.tts = TTSEngine(self.config)
        self.knowledge = KnowledgeBase(self.config)
        self.running = False

    def start(self):
        """启动数字人"""
        print("🎭 Mao 数字人启动中...")
        print(f"   TTS: {self.config.tts_engine}")
        print(f"   RAG: {self.config.vectorstore_dir}")
        self.running = True
        print("✅ 启动完成！")

    def stop(self):
        """停止数字人"""
        self.running = False
        print("👋 数字人已停止")

    def chat(self, user_input: str) -> str:
        """对话接口"""
        # 1. RAG 检索相关知识
        context = self.knowledge.retrieve(user_input)

        # 2. 构建 prompt (使用 mao-skill 对话模式)
        prompt = self._build_prompt(user_input, context)

        # 3. 调用 LLM (需要接入 Claude/GPT)
        response = self._call_llm(prompt)

        # 4. TTS 语音输出
        self.tts.speak(response)

        return response

    def _build_prompt(self, user_input: str, context: str) -> str:
        """构建提示词"""
        return f"""你是毛泽东。以第一人称"我"进行对话。
特点：口语化、有幽默感、善用比喻、时而自嘲。

参考知识:
{context}

请用毛泽东的语气回复：
"""

    def _call_llm(self, prompt: str) -> str:
        """调用大模型 (需接入 Claude API)"""
        # TODO: 接入 Claude/GPT API
        return "[需要接入 LLM API]"

    def run(self):
        """交互式运行"""
        self.start()
        print("\n请输入对话（输入 q 退出）：")

        while self.running:
            try:
                user_input = input("\n你: ")
                if user_input.lower() in ['q', 'quit', 'exit']:
                    break
                if user_input.strip():
                    response = self.chat(user_input)
                    print(f"\n毛泽东: {response}")
            except KeyboardInterrupt:
                break

        self.stop()


if __name__ == "__main__":
    dh = DigitalHuman()
    dh.run()