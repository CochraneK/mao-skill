# mao-skill 快速开始脚本
# Windows: 使用 setup.bat 或手动运行下方命令

@echo off
echo ====================================
echo mao-skill 快速开始
echo ====================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未检测到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo [1/4] 初始化目录...
python sync.py --init

echo.
echo [2/4] 安装依赖...
pip install langchain langchain-community chromadb -q

echo.
echo [3/4] 构建 RAG 知识库...
python digital_human/runner.py build-rag

echo.
echo [4/4] 启动对话...
python digital_human/runner.py chat

pause