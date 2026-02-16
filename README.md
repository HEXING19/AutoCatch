# AutoCatch - Universal Automation Agent 🤖

[English](#english) | [中文](#chinese)

<a name="english"></a>

## English

AutoCatch is an intelligent automation agent that watches your workflow and learns to replicate it. By analyzing screen recordings using Google's Gemini 1.5 Pro Multimodal model, it understands your actions and executes them automatically on your machine.

### 🚀 Features

- **Visual Understanding**: Uses Gemini 1.5 Pro to analyze video keyframes and understand complex workflows.
- **Cross-Platform**: Built with Python and PyAutoGUI, capable of running on macOS, Windows, and Linux.
- **Smart Sampling**: Automatically extracts keyframes based on visual changes to optimize API usage.
- **High Precision**: Supports high-resolution analysis (up to 2048px) and coordinate mapping for accurate interactions.
- **Dry Run Mode**: Test the analysis and generated plan without executing actions.

### 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HEXING19/AutoCatch.git
   cd AutoCatch
   ```

2. **Install dependencies**
   Recommend using a virtual environment (Python 3.10+):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configuration**
   Copy the example environment file and add your Google Gemini API key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```ini
   GEMINI_API_KEY=your_api_key_here
   # Optional: Proxy settings if needed
   # http_proxy=http://127.0.0.1:7890
   # https_proxy=http://127.0.0.1:7890
   ```

### 📖 Usage

1. **Record a workflow**
   Use QuickTime or any screen recorder to capture the task you want to automate. Save it as `Screen.mov` (or any other name) in the project directory.
   *Tip: For best results, record the full screen.*

2. **Run the agent**
   ```bash
   python3 main.py Screen.mov
   ```

3. **Watch it happen**
   - The agent will extract keyframes and send them to Gemini for analysis.
   - It will generate a step-by-step action plan (displayed in the terminal).
   - After a 5-second countdown, it will take control of your mouse and keyboard to execute the workflow.
   - **Important**: Switch to the target application window during the 5-second countdown!

#### Options
- **Dry Run**: Generate the plan without executing it.
  ```bash
  python3 main.py Screen.mov --dry-run
  ```

### 📂 Project Structure

- `main.py`: Entry point of the application.
- `core/`:
  - `video.py`: Handles video processing and smart keyframe extraction.
  - `brain.py`: Interfaces with Gemini API for workflow analysis.
  - `executor.py`: Executes the generated action plan using PyAutoGUI.
- `config.py`: Configuration settings.
- `.env`: API keys and secrets (Git ignored).

### ⚠️ Notes

- **Screen Resolution**: The agent works best when the playback resolution matches the recording resolution.
- **Safety**: Move your mouse to a corner of the screen to trigger the PyAutoGUI fail-safe and abort execution if needed.

### 📄 License

MIT License

---

<a name="chinese"></a>

## 中文 (Chinese)

AutoCatch 是一个智能自动化代理，它通过观察您的工作流程来学习并复制操作。它利用 Google Gemini 1.5 Pro 多模态模型分析屏幕录像，理解您的动作，并在您的机器上自动执行这些操作。

### 🚀 功能特点

- **视觉理解**：使用 Gemini 1.5 Pro 分析视频关键帧，理解复杂的工作流程。
- **跨平台**：基于 Python 和 PyAutoGUI 构建，支持在 macOS、Windows 和 Linux 上运行。
- **智能采样**：根据视觉变化自动提取关键帧，优化 API 使用并捕捉关键动作。
- **高精度**：支持高分辨率分析（最高 2048px）和坐标映射，确保交互准确。
- **空运行模式 (Dry Run)**：在不实际执行操作的情况下测试分析结果和生成的计划。

### 🛠️ 安装指南

1. **克隆仓库**
   ```bash
   git clone https://github.com/HEXING19/AutoCatch.git
   cd AutoCatch
   ```

2. **安装依赖**
   建议使用虚拟环境 (Python 3.10+)：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **配置**
   复制示例环境文件并添加您的 Google Gemini API 密钥：
   ```bash
   cp .env.example .env
   ```
   编辑 `.env` 文件：
   ```ini
   GEMINI_API_KEY=your_api_key_here
   # 可选：如果需要代理设置
   # http_proxy=http://127.0.0.1:7890
   # https_proxy=http://127.0.0.1:7890
   ```

### 📖 使用说明

1. **录制工作流**
   使用 QuickTime 或任何录屏软件捕捉您想要自动化的任务。将视频保存为 `Screen.mov`（或其他名称）在项目目录下。
   *提示：为了获得最佳效果，建议录制全屏。*

2. **运行代理**
   ```bash
   python3 main.py Screen.mov
   ```

3. **见证自动化**
   - 代理将提取关键帧并发送给 Gemini 进行分析。
   - 它将生成分步操作计划（显示在终端中）。
   - 倒计时5秒后，它将控制您的鼠标和键盘执行工作流。
   - **重要提示**：在5秒倒计时期间，请切换到目标应用程序窗口！

#### 选项
- **空运行 (Dry Run)**：仅生成计划，不执行任何操作。
  ```bash
  python3 main.py Screen.mov --dry-run
  ```

### 📂 项目结构

- `main.py`: 程序的入口点。
- `core/`:
  - `video.py`: 处理视频处理和智能关键帧提取。
  - `brain.py`: 与 Gemini API 接口，进行工作流分析。
  - `executor.py`: 使用 PyAutoGUI 执行生成的操作计划。
- `config.py`: 配置设置。
- `.env`: API 密钥和机密信息（已被 Git 忽略）。

### ⚠️ 注意事项

- **屏幕分辨率**：当回放分辨率与录制分辨率匹配时，代理的效果最佳。
- **安全机制**：如果需要紧急停止，将鼠标快速移动到屏幕角落将触发 PyAutoGUI 的故障安全机制并中止执行。

### 📄 许可证

MIT License
