# PackPython AI Agent

## 项目概述

PackPython 是一个 PyQt5 GUI 打包助手，用于将 Python 项目打包为可分发的程序。它使用 PyInstaller 执行打包，并提供以下功能：

- 选择 Python 项目目录
- 扫描并选择要打包的 Python 文件
- 选择图标文件、资源目录和输出目录
- 生成单文件或单目录打包
- 快速打包模式（跳过 UPX、降低日志级别）
- 隐藏命令行界面（Windows GUI 模式）
- 内置日志面板和进度条
- 打包完成后可直接打开输出目录

## 关键文件

- `main.py`：主窗口与打包逻辑核心
- `assets/package.ico`：主窗口图标和默认打包图标资源
- `requirements.txt`：项目依赖

## 代码规范与约定

- 使用 `PyQt5` 作为 GUI 框架
- 全局常量集中定义在 `main.py` 顶部
- 所有按钮使用统一字体常量 `BUTTON_FONT_NAME` / `BUTTON_FONT_SIZE`
- 日志写入文件并显示在 `QPlainTextEdit`
- 打包操作在 `QThread` 后台线程中执行，避免阻塞 UI
- 打包命令通过 `build_pyinstaller_command()` 组装
- 记录当前选项状态：单文件、快速打包、隐藏命令行界面

## 当前实现细节

- `PackageGui` 控件布局采用 `QVBoxLayout` 和 `QSplitter`
- `build_pyinstaller_command()` 支持 `--windowed` 参数用于隐藏控制台
- `run_pyinstaller()` 负责执行子进程并逐行读取输出
- `PackagingWorker` 在后台运行打包，并通过信号更新主界面

## 未来扩展建议

- 增加打包配置保存/加载功能
- 支持更多 PyInstaller 选项，如 `--add-data` 的多个路径
- 添加运行时配置文件和自定义图标
- 增加打包日志导出和错误详情窗口
- 支持跨平台命令行选项提示

## AI 任务指引

如果要为此项目继续编写 AI 代码：

1. 先从 `main.py` 中提取 UI 控件和信号连接
2. 保持 `build_pyinstaller_command()` 和 `run_pyinstaller()` 的单一职责
3. 任何新增 UI 控件都应使用现有字体常量和样式
4. 新功能优先考虑在不破坏现有打包流程的前提下扩展
5. 避免增加主动依赖，尽量使用标准库和已存在依赖
