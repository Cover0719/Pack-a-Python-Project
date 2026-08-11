# Python 项目打包助手

## 功能说明
- 选择一个 Python 项目目录。
- 自动扫描目录中的 Python 文件，并在界面中展示。
- 选择要打包的 Python 文件。
- 可选择图标文件与资源目录。
- 使用 PyInstaller 将项目打包为目录或单文件输出。

## 使用前准备
1. 安装依赖：
   - `pip install -r requirements.txt`
2. 运行主程序：
   - `python main.py`

## 输出说明
- 打包结果默认输出到 `output` 目录。
- 你也可以修改脚本中的 `OUTPUT_PATH` 常量。
