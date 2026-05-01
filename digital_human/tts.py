# -*- coding: utf-8 -*-
"""TTS 语音合成引擎"""

from pathlib import Path
from typing import Optional
import subprocess
import os


class TTSEngine:
    """语音合成引擎"""

    def __init__(self, config):
        self.config = config
        self.engine = config.tts_engine
        self.last_audio_path: Optional[Path] = None

    def speak(self, text: str) -> Optional[Path]:
        """将文字转为语音"""
        if not text:
            return None

        # 清理文本
        text = self._clean_text(text)

        if self.engine == "chat_tts":
            return self._chat_tts(text)
        elif self.engine == "edge":
            return self._edge_tts(text)
        elif self.engine == "cosyvoice":
            return self._cosyvoice(text)
        else:
            print(f"[WARN] 未知的 TTS 引擎: {self.engine}")
            return None

    def _clean_text(self, text: str) -> str:
        """清理文本，移除特殊符号"""
        # 移除括号内容（如动作描述）
        import re
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'（.*?）', '', text)
        text = re.sub(r'\(.*?\)', '', text)
        # 移除多余空白
        text = ' '.join(text.split())
        return text[:500]  # 限制长度

    def _chat_tts(self, text: str) -> Optional[Path]:
        """使用 ChatTTS 语音合成"""
        try:
            import ChatTTS
        except ImportError:
            print("[ERROR] 请安装 ChatTTS: pip install chat-tts")
            return None

        try:
            chat = ChatTTS.Chat()
            chat.load()

            # 生成语音
            wav = chat.generate(text)

            # 保存文件
            output_dir = self.config.project_dir / "output"
            output_dir.mkdir(exist_ok=True)

            import random
            filename = f"mao_{random.randint(1000,9999)}.wav"
            self.last_audio_path = output_dir / filename

            chat.save(wav, str(self.last_audio_path))
            print(f"[OK] 语音已保存: {self.last_audio_path}")

            return self.last_audio_path

        except Exception as e:
            print(f"[ERROR] ChatTTS 生成失败: {e}")
            return None

    def _edge_tts(self, text: str) -> Optional[Path]:
        """使用 Edge TTS (免费)"""
        try:
            import edge_tts
        except ImportError:
            print("[ERROR] 请安装 edge-tts: pip install edge-tts")
            return None

        import asyncio
        import random

        async def _speak():
            output_dir = self.config.project_dir / "output"
            output_dir.mkdir(exist_ok=True)

            filename = f"mao_{random.randint(1000,9999)}.mp3"
            output_path = output_dir / filename

            # 使用中文男声
            communicate = edge_tts.Communicate(text, "zh-CN-YunxiNeural")
            await communicate.save(str(output_path))

            return output_path

        try:
            self.last_audio_path = asyncio.run(_speak())
            print(f"[OK] 语音已保存: {self.last_audio_path}")
            return self.last_audio_path
        except Exception as e:
            print(f"[ERROR] Edge TTS 生成失败: {e}")
            return None

    def _cosyvoice(self, text: str) -> Optional[Path]:
        """使用 CosyVoice2 (需配置硅基流动API)"""
        print("[INFO] CosyVoice2 需要配置硅基流动 API")
        print("[INFO] 请访问: https://siliconflow.cn")

        # TODO: 实现 CosyVoice2 调用
        return None

    def play_last(self):
        """播放上次生成的语音"""
        if not self.last_audio_path or not self.last_audio_path.exists():
            print("[WARN] 没有可播放的语音")
            return

        import platform
        system = platform.system()

        try:
            if system == "Windows":
                os.startfile(str(self.last_audio_path))
            elif system == "Darwin":  # macOS
                subprocess.run(["open", str(self.last_audio_path)])
            elif system == "Linux":
                subprocess.run(["xdg-open", str(self.last_audio_path)])
            print(f"[OK] 正在播放: {self.last_audio_path.name}")
        except Exception as e:
            print(f"[ERROR] 播放失败: {e}")


# 便捷函数
def speak(text: str, engine: str = "chat_tts") -> Optional[Path]:
    """快速语音合成"""
    from .config import Config
    config = Config()
    config.tts_engine = engine

    tts = TTSEngine(config)
    return tts.speak(text)


if __name__ == "__main__":
    # 测试
    test_text = "你好，我是毛泽东。有什么问题尽管问我。"
    path = speak(test_text, "edge")
    print(f"生成文件: {path}")