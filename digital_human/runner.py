# -*- coding: utf-8 -*-
"""
mao-skill 数字人运行器
======================
语音对话 + RAG知识库 + Live2D形象

使用:
    python runner.py              # 交互模式
    python runner.py --web        # Web模式
    python runner.py --build-rag  # 构建知识库
"""
import os
import sys
import argparse
from pathlib import Path

# Windows 编码修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 添加项目根目录到路径
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

from digital_human import DigitalHuman
from digital_human.config import Config
from digital_human.tts import TTSEngine
from digital_human.rag import ChromaKB


def cmd_build_rag(args):
    """构建 RAG 向量库"""
    print("🔨 构建 RAG 知识库...")
    print("=" * 50)

    config = Config()
    kb = ChromaKB(config)
    kb.build(force=args.force)

    print("=" * 50)
    if kb.initialized:
        print("✅ 知识库构建完成")
    else:
        print("❌ 知识库构建失败")


def cmd_tts(args):
    """TTS 测试"""
    print("🔊 TTS 测试...")
    print("=" * 50)

    config = Config()
    config.tts_engine = args.engine or config.tts_engine

    tts = TTSEngine(config)
    audio_path = tts.speak(args.text)

    print("=" * 50)
    if audio_path:
        print(f"✅ 语音已生成: {audio_path}")
        if args.play:
            tts.play_last()
    else:
        print("❌ 语音生成失败")


def cmd_chat(args):
    """对话模式"""
    print("💬 启动对话模式...")
    print("=" * 50)

    config = Config()
    dh = DigitalHuman()
    dh.config.tts_engine = args.tts or dh.config.tts_engine

    dh.start()

    # 如果指定了构建 RAG
    if args.build_rag:
        print("\n📚 构建知识库...")
        kb = ChromaKB(config)
        kb.build(force=True)

    print("\n" + "=" * 50)
    print("请输入对话（输入 q 退出）")
    print("=" * 50)

    while dh.running:
        try:
            user_input = input("\n你: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['q', 'quit', 'exit', '退出']:
                break

            # 对话
            response = dh.chat(user_input)
            print(f"\n毛泽东: {response}")

            # 可选：语音播放
            if args.speak and dh.tts.last_audio_path:
                dh.tts.play_last()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[ERROR] {e}")

    dh.stop()


def cmd_web(args):
    """Web 界面模式"""
    print("🌐 Web 界面模式 (待实现)")
    print("[INFO] 可以使用 Gradio 快速搭建:")
    print("       pip install gradio")
    print("       参考: https://gradio.app")


def main():
    parser = argparse.ArgumentParser(
        description="mao-skill 数字人",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python runner.py --build-rag              # 构建知识库
  python runner.py --tts "你好"             # 测试语音
  python runner.py --chat                   # 对话模式
  python runner.py --web                    # Web模式(待实现)
        """
    )

    sub = parser.add_subparsers(dest="cmd", required=True)

    # 构建 RAG
    p_rag = sub.add_parser("build-rag", help="构建 RAG 知识库")
    p_rag.add_argument("--force", "-f", action="store_true", help="强制重建")

    # TTS 测试
    p_tts = sub.add_parser("tts", help="测试 TTS 语音")
    p_tts.add_argument("text", help="要转换的文字")
    p_tts.add_argument("--engine", "-e", help="TTS 引擎 (chat_tts/edge/cosyvoice)")
    p_tts.add_argument("--play", "-p", action="store_true", help="生成后自动播放")

    # 对话模式
    p_chat = sub.add_parser("chat", help="交互式对话")
    p_chat.add_argument("--build-rag", "-r", action="store_true", help="启动前构建知识库")
    p_chat.add_argument("--tts", "-t", help="TTS 引擎")
    p_chat.add_argument("--speak", "-s", action="store_true", help="自动播放语音")

    # Web模式
    p_web = sub.add_parser("web", help="Web界面 (待实现)")

    args = parser.parse_args()

    if args.cmd == "build-rag":
        cmd_build_rag(args)
    elif args.cmd == "tts":
        cmd_tts(args)
    elif args.cmd == "chat":
        cmd_chat(args)
    elif args.cmd == "web":
        cmd_web(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()