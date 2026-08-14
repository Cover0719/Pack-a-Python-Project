# PackPython 项目说明

## 1. 项目概述

PackPython 是一个基于 PyQt5 的 Python 打包助手，主要功能包括：

- 选择项目目录
- 扫描并筛选要打包的 Python 文件
- 选择图标、资源和输出目录
- 生成单文件或单目录输出
- 开启快速打包模式
- 隐藏命令行窗口
- 查看打包日志和进度
- 支持从 `.package` 配置文件自动加载打包参数

---

## 2. 文件说明

- `main.py`：主程序，包含界面、逻辑和打包流程
- `assets/package.ico`：默认图标
- `assets/help.md`：当前帮助文档
- `.package`：自动加载的项目打包配置文件
- `.package.example`：配置模板示例

---

## 3. 常量说明

### BASE_DIR

- 初始化位置：第 19 行
- 作用：项目根目录，所有相对路径都以它为基础。
- 常见值：
  - `Path(__file__).resolve().parent`
- 被引用位置：
  - 被 `FONTS_DIR`、`ASSETS_DIR`、`OUTPUT_PATH` 引用
  - 被项目目录选择框作为默认起始目录

### FONTS_DIR

- 初始化位置：第 20 行
- 作用：字体目录。
- 常见值：
  - `BASE_DIR / "fonts"`
- 被引用位置：
  - 被 `ICON_FONT_FILE`、`LOG_FONT_FILE`、`BODY_FONT_FILE` 引用

### ASSETS_DIR

- 初始化位置：第 21 行
- 作用：资源目录，用于存放图标和辅助文件。
- 常见值：
  - `BASE_DIR / "assets"`
- 被引用位置：
  - 被 `DEFAULT_WINDOW_ICON`、`LOG_FILE` 和图标选择器引用

### DEFAULT_WINDOW_ICON

- 初始化位置：第 22 行
- 作用：默认窗口图标。
- 常见值：
  - `ASSETS_DIR / "package.ico"`
- 被引用位置：
  - 被 `PackageGui.__init__()` 引用
  - 被 `main()` 引用，作为回退图标

### OUTPUT_PATH

- 初始化位置：第 23 行
- 作用：默认输出目录。
- 常见值：
  - `Path(r"D:\output")`
- 被引用位置：
  - 被 `PackageGui.__init__()` 引用
  - 被 `select_output_dir()` 默认打开路径使用

### LOG_FILE

- 初始化位置：第 24 行
- 作用：日志文件路径。
- 常见值：
  - `ASSETS_DIR / "package_tool.log"`
- 被引用位置：
  - 被 `write_log()` 写入
  - 被 `open_log_file()` 打开

### WINDOW_WIDTH

- 初始化位置：第 25 行
- 作用：主窗口默认宽度。
- 常见值：
  - `1280`
- 被引用位置：
  - 被 `PackageGui.__init__()` 使用

### WINDOW_HEIGHT

- 初始化位置：第 26 行
- 作用：主窗口默认高度。
- 常见值：
  - `760`
- 被引用位置：
  - 被 `PackageGui.__init__()` 使用

### LOG_PANEL_WIDTH

- 初始化位置：第 27 行
- 作用：日志面板宽度。
- 常见值：
  - `580`
- 被引用位置：
  - 被布局代码引用，用于分栏比例

### LIST_HEIGHT

- 初始化位置：第 28 行
- 作用：文件列表框高度。
- 常见值：
  - `180`
- 被引用位置：
  - 被 `QListWidget` 相关布局引用

### TEXT_BOX_HEIGHT

- 初始化位置：第 29 行
- 作用：资源列表和日志区高度。
- 常见值：
  - `92`
- 被引用位置：
  - 被资源列表和日志文本框引用

### BUTTON_COLOR

- 初始化位置：第 30 行
- 作用：按钮主颜色。
- 常见值：
  - `"#0f6cbd"`
- 被引用位置：
  - 被 `_build_ui()` 的样式表引用

### BUTTON_HOVER_COLOR

- 初始化位置：第 31 行
- 作用：按钮悬停时的颜色。
- 常见值：
  - `"#125fb7"`
- 被引用位置：
  - 被 `_build_ui()` 的样式表引用

### BUTTON_DISABLED_COLOR

- 初始化位置：第 32 行
- 作用：禁用状态下按钮背景色。
- 常见值：
  - `"#9db7cb"`
- 被引用位置：
  - 被 `_build_ui()` 引用

### BUTTON_DISABLED_TEXT

- 初始化位置：第 33 行
- 作用：禁用状态下字体颜色。
- 常见值：
  - `"#eef4fa"`
- 被引用位置：
  - 被 `_build_ui()` 引用

### BACKGROUND_COLOR

- 初始化位置：第 34 行
- 作用：界面背景色。
- 常见值：
  - `"#f4f6fb"`
- 被引用位置：
  - 被 `_build_ui()` 引用

### TEXT_COLOR

- 初始化位置：第 35 行
- 作用：界面常规文字色。
- 常见值：
  - `"#1f2937"`
- 被引用位置：
  - 被 `_build_ui()` 引用

### BORDER_COLOR

- 初始化位置：第 36 行
- 作用：控件边框颜色。
- 常见值：
  - `"#d7dee8"`
- 被引用位置：
  - 被 `_build_ui()` 引用

### PANEL_RADIUS

- 初始化位置：第 37 行
- 作用：控件圆角半径。
- 常见值：
  - `10`
- 被引用位置：
  - 被 `_build_ui()` 引用

### BUTTON_FONT_NAME

- 初始化位置：第 38 行
- 作用：按钮使用字体名称。
- 常见值：
  - `"Microsoft YaHei"`
- 被引用位置：
  - 被按钮控件设置字体时引用

### BUTTON_FONT_SIZE

- 初始化位置：第 39 行
- 作用：按钮字体大小。
- 常见值：
  - `11`
- 被引用位置：
  - 被按钮控件设置字体时引用

### ICON_FONT_NAME

- 初始化位置：第 40 行
- 作用：图标字体名称。
- 常见值：
  - `"IconFont"`
  - 加载后的字体族名
- 被引用位置：
  - 被 `load_font_families()` 更新

### ICON_FONT_SIZE

- 初始化位置：第 41 行
- 作用：图标字体大小。
- 常见值：
  - `16`
- 被引用位置：
  - 被图标样式设置引用

### LOG_FONT_NAME

- 初始化位置：第 42 行
- 作用：日志区字体名称。
- 常见值：
  - `"LogFont"`
- 被引用位置：
  - 被日志文本框设置引用

### LOG_FONT_SIZE

- 初始化位置：第 43 行
- 作用：日志区字体大小。
- 常见值：
  - `9`
- 被引用位置：
  - 被日志文本框设置引用

### BODY_FONT_NAME

- 初始化位置：第 44 行
- 作用：主界面常规字体名称。
- 常见值：
  - `"Microsoft YaHei"`
- 被引用位置：
  - 被 `PackageGui.__init__()` 和 `_build_ui()` 引用

### BODY_FONT_SIZE

- 初始化位置：第 45 行
- 作用：主界面常规字体大小。
- 常见值：
  - `10`
- 被引用位置：
  - 被窗口和控件字体设置引用

### ICON_FONT_FILE

- 初始化位置：第 47 行
- 作用：图标字体文件路径。
- 常见值：
  - `FONTS_DIR / "icon_font.ttf"`
- 被引用位置：
  - 被 `load_custom_font()` 调用

### LOG_FONT_FILE

- 初始化位置：第 48 行
- 作用：日志字体文件路径。
- 常见值：
  - `FONTS_DIR / "log_font.ttf"`
- 被引用位置：
  - 被 `load_custom_font()` 调用

### BODY_FONT_FILE

- 初始化位置：第 49 行
- 作用：正文字体文件路径。
- 常见值：
  - `FONTS_DIR / "body_font.ttf"`
- 被引用位置：
  - 被 `load_custom_font()` 调用

---

## 4. 变量说明

### ctypes

- 初始化位置：第 6 行
- 作用：用于 Windows 下设置应用任务栏标识。
- 常见值：
  - `None`
  - `ctypes.windll.shell32`
- 被引用位置：
  - 被 `main()` 引用，用于设置 AppUserModelID

### Qt

- 初始化位置：第 10 行
- 作用：Qt 核心模块。
- 常见值：
  - `Qt.Horizontal`
- 被引用位置：
  - 被 `QSplitter` 初始化引用

### QThread

- 初始化位置：第 10 行
- 作用：后台线程对象。
- 常见值：
  - `QThread()` 实例
- 被引用位置：
  - 被 `start_packaging()` 和 `PackagingWorker` 相关代码引用

### QObject

- 初始化位置：第 10 行
- 作用：Qt 对象基类。
- 常见值：
  - `PackagingWorker` 实例
- 被引用位置：
  - 被 `PackagingWorker` 类定义引用

### pyqtSignal

- 初始化位置：第 10 行
- 作用：定义信号。
- 常见值：
  - `finished`
  - `log_signal`
  - `progress_signal`
- 被引用位置：
  - 被 `PackagingWorker` 类定义引用

### pyqtSlot

- 初始化位置：第 10 行
- 作用：Qt 槽函数装饰器。
- 常见值：
  - 装饰器对象
- 被引用位置：
  - 被 `handle_progress()`、`handle_log_message()`、`on_packaging_finished()` 引用

### QFont

- 初始化位置：第 11 行
- 作用：字体对象。
- 常见值：
  - `QFont(...)`
- 被引用位置：
  - 被窗口和控件字体设置引用

### QFontDatabase

- 初始化位置：第 11 行
- 作用：字体数据库。
- 常见值：
  - 实例对象
- 被引用位置：
  - 被 `load_custom_font()` 引用

### QIcon

- 初始化位置：第 12 行
- 作用：图标对象。
- 常见值：
  - 有效图标
  - 空图标
- 被引用位置：
  - 被 `PackageGui.__init__()` 和 `main()` 引用

### QApplication

- 初始化位置：第 13 行
- 作用：Qt 应用对象。
- 常见值：
  - `QApplication(sys.argv)`
- 被引用位置：
  - 被 `main()` 引用

### QCheckBox

- 初始化位置：第 13 行
- 作用：打包选项控件。
- 常见值：
  - `True` / `False`
- 被引用位置：
  - 被 `start_packaging()` 和 `_apply_setting_value()` 引用

### QDialog

- 初始化位置：第 13 行
- 作用：弹窗容器。
- 常见值：
  - `QDialog` 实例
- 被引用位置：
  - 被 `add_resource_entry()` 引用

### QDialogButtonBox

- 初始化位置：第 13 行
- 作用：确认和取消按钮组。
- 常见值：
  - `QDialogButtonBox.Ok | QDialogButtonBox.Cancel`
- 被引用位置：
  - 被资源确认对话框引用

### QFileDialog

- 初始化位置：第 13 行
- 作用：文件和目录选择框。
- 常见值：
  - 文件路径字符串
  - 目录路径字符串
- 被引用位置：
  - 被选择项目、脚本、图标、资源和输出目录功能引用

### QFrame

- 初始化位置：第 13 行
- 作用：容器框架。
- 常见值：
  - `QFrame` 实例
- 被引用位置：
  - 被文件列表框容器引用

### QHBoxLayout

- 初始化位置：第 13 行
- 作用：横向布局管理器。
- 常见值：
  - `QHBoxLayout()`
- 被引用位置：
  - 被界面各行布局引用

### QLabel

- 初始化位置：第 13 行
- 作用：标签组件。
- 常见值：
  - 文本标签
- 被引用位置：
  - 被路径、状态和标题区域引用

### QListWidget

- 初始化位置：第 13 行
- 作用：列表控件。
- 常见值：
  - `file_list_widget`
  - `resource_source_list`
  - `resource_target_list`
- 被引用位置：
  - 被文件和资源列表填充与刷新逻辑引用

### QMainWindow

- 初始化位置：第 13 行
- 作用：主窗口类。
- 常见值：
  - `PackageGui` 实例
- 被引用位置：
  - 被 `PackageGui` 继承

### QMessageBox

- 初始化位置：第 13 行
- 作用：提示框组件。
- 常见值：
  - 错误提示
  - 成功提示
- 被引用位置：
  - 被打包校验、成功提示和错误提示引用

### QPushButton

- 初始化位置：第 13 行
- 作用：按钮控件。
- 常见值：
  - 各类功能按钮
- 被引用位置：
  - 被项目选择、文件选择、打包等功能引用

### QPlainTextEdit

- 初始化位置：第 13 行
- 作用：只读日志显示控件。
- 常见值：
  - 日志文本内容
- 被引用位置：
  - 被日志区显示逻辑引用

### QSplitter

- 初始化位置：第 13 行
- 作用：左右分栏控件。
- 常见值：
  - `QSplitter(Qt.Horizontal)`
- 被引用位置：
  - 被界面布局引用

### QVBoxLayout

- 初始化位置：第 13 行
- 作用：垂直布局管理器。
- 常见值：
  - `QVBoxLayout()`
- 被引用位置：
  - 被主界面和窗口区域布局引用

### QWidget

- 初始化位置：第 13 行
- 作用：基础容器控件。
- 常见值：
  - `central_widget`
  - `left_widget`
  - `log_widget`
- 被引用位置：
  - 被界面模块装配引用

### QLineEdit

- 初始化位置：第 13 行
- 作用：文字输入框。
- 常见值：
  - `project_name_input`
  - `target_input`
- 被引用位置：
  - 被项目名和资源路径输入引用

### QProgressBar

- 初始化位置：第 13 行
- 作用：进度条控件。
- 常见值：
  - `0~100`
- 被引用位置：
  - 被进度更新逻辑引用

### self.project_dir

- 初始化位置：第 286 行
- 作用：当前项目目录。
- 常见值：
  - `Path` 对象
  - `None`
- 被引用位置：
  - 被 `collect_python_files()`、`select_project_dir()`、`_load_package_file_settings()` 引用

### self.resource_entries

- 初始化位置：第 300 行
- 作用：已添加的资源项列表。
- 常见值：
  - `[]`
  - `[(source_path, relative_target), ...]`
- 被引用位置：
  - 被 `_refresh_resource_lists()` 和 `start_packaging()` 引用

---

## 5. 函数说明

### get_time()

- 初始化位置：第 52-55 行
- 作用：获取当前时间，并格式化为 `yyyy-mm-dd HH:MM:SS`。
- 引用内容：无
- 被引用位置：
  - 被 `format_log_message()` 引用
  - 被 `ensure_runtime_dirs()` 引用

### format_log_message(message, level="INFO")

- 初始化位置：第 58-60 行
- 作用：生成统一的日志输出格式。
- 引用内容：
  - `message`
  - `level`
- 被引用位置：
  - 被 `write_log()` 和日志事件使用

### write_log(message, level="INFO", log_mode_f=1)

- 初始化位置：第 63-75 行
- 作用：将日志写入 `LOG_FILE`。
- 引用内容：
  - `message`
  - `level`
  - `log_mode_f`
- 被引用位置：
  - 被多处日志写入逻辑引用

### load_custom_font(font_path, fallback_name)

- 初始化位置：第 78-85 行
- 作用：加载自定义字体，失败则回退备用字体。
- 引用内容：
  - `font_path`
  - `fallback_name`
- 被引用位置：
  - 被 `load_font_families()` 引用

### load_font_families()

- 初始化位置：第 88-92 行
- 作用：加载图标、日志和正文字体。
- 引用内容：
  - `ICON_FONT_NAME`
  - `LOG_FONT_NAME`
  - `BODY_FONT_NAME`
- 被引用位置：
  - 被 `main()` 引用

### ensure_runtime_dirs()

- 初始化位置：第 95-103 行
- 作用：确保资源目录和输出目录存在，并初始化日志文件。
- 引用内容：无
- 被引用位置：
  - 程序启动时自动调用

### strip_package_quotes(value)

- 初始化位置：第 107-114 行
- 作用：去掉字符串两侧的单引号或双引号。
- 引用内容：
  - `value`
- 被引用位置：
  - 被 `parse_package_file()` 和 `resolve_project_relative_value()` 引用

### parse_package_file(project_dir)

- 初始化位置：第 117-141 行
- 作用：读取 `.package` 文件，解析 `key=value` 参数并忽略注释和空行。
- 引用内容：
  - `project_dir`
- 被引用位置：
  - 被 `_load_package_file_settings()` 引用

### resolve_project_relative_value(value, project_dir)

- 初始化位置：第 143-155 行
- 作用：把项目内相对路径转成实际 `Path`。
- 引用内容：
  - `value`
  - `project_dir`
- 被引用位置：
  - 被 `_apply_pack_file_selection()`、`_apply_add_file_entries()`、`_load_package_file_settings()` 引用

### collect_python_files(project_dir)

- 初始化位置：第 157-172 行
- 作用：扫描目录下的 Python 文件，过滤常见无关目录。
- 引用内容：
  - `project_dir`
- 被引用位置：
  - 被 `select_project_dir()` 和 `_load_package_file_settings()` 引用

### build_pyinstaller_command(...)

- 初始化位置：第 174-214 行
- 作用：拼接 PyInstaller 命令。
- 引用内容：
  - `entry_scripts`
  - `project_name`
  - `output_dir`
  - `icon_path`
  - `resources_path`
  - `onefile`
  - `fast_mode`
  - `hide_console`
  - `resource_entries`
- 被引用位置：
  - 被 `run_pyinstaller()` 引用

### run_pyinstaller(...)

- 初始化位置：第 217-302 行
- 作用：执行 PyInstaller 打包，并更新日志与进度。
- 引用内容：
  - `entry_scripts`
  - `project_dir`
  - `project_name`
  - `output_dir`
  - `icon_path`
  - `resources_path`
  - `onefile`
  - `fast_mode`
  - `log_emitter`
  - `progress_emitter`
  - `hide_console`
  - `resource_entries`
- 被引用位置：
  - 被 `PackagingWorker.run()` 引用

### PackagingWorker(QObject)

- 初始化位置：第 304-343 行
- 作用：后台打包线程对象。
- 引用内容：
  - `finished`
  - `log_signal`
  - `progress_signal`
- 被引用位置：
  - 被 `start_packaging()` 创建并启动

### PackageGui.__init__()

- 初始化位置：第 345-370 行
- 作用：初始化主窗口和基础数据。
- 引用内容：无
- 被引用位置：
  - 被 `main()` 里实例化

### PackageGui._build_ui()

- 初始化位置：第 372-591 行
- 作用：创建界面布局和控件。
- 引用内容：无
- 被引用位置：
  - 被 `__init__()` 调用

### PackageGui._append_log(message)

- 初始化位置：第 593-602 行
- 作用：追加日志文本到界面的日志区。
- 引用内容：
  - `message`
- 被引用位置：
  - 被 `handle_log_message()` 调用

### PackageGui.handle_progress(value)

- 初始化位置：第 604-607 行
- 作用：更新进度条。
- 引用内容：
  - `value`
- 被引用位置：
  - 由后台线程的 `progress_signal` 连接

### PackageGui.handle_log_message(message, level)

- 初始化位置：第 609-612 行
- 作用：接收后台日志并显示在界面中。
- 引用内容：
  - `message`
  - `level`
- 被引用位置：
  - 由后台线程的 `log_signal` 连接

### PackageGui._apply_pack_file_selection(pack_file_value)

- 初始化位置：第 615-636 行
- 作用：根据 `.package` 自动勾选 Python 文件。
- 引用内容：
  - `pack_file_value`
- 被引用位置：
  - 被 `_load_package_file_settings()` 引用

### PackageGui._apply_add_file_entries(add_file_value)

- 初始化位置：第 638-659 行
- 作用：根据 `.package` 自动添加资源项。
- 引用内容：
  - `add_file_value`
- 被引用位置：
  - 被 `_load_package_file_settings()` 引用

### PackageGui._apply_setting_value(setting_value)

- 初始化位置：第 661-673 行
- 作用：根据 `.package` 中的 `setting` 参数更新打包设置。
- 引用内容：
  - `setting_value`
- 被引用位置：
  - 被 `_load_package_file_settings()` 引用

### PackageGui._load_package_file_settings()

- 初始化位置：第 675-718 行
- 作用：读取 `.package` 配置并应用到 GUI 中。
- 引用内容：无
- 被引用位置：
  - 被 `select_project_dir()` 调用

### PackageGui.select_project_dir()

- 初始化位置：第 720-735 行
- 作用：选择项目目录并扫描其 Python 文件。
- 引用内容：无
- 被引用位置：
  - 被“选择项目目录”按钮触发

### PackageGui.populate_file_listbox()

- 初始化位置：第 737-744 行
- 作用：填充项目中已识别的 Python 文件列表。
- 引用内容：无
- 被引用位置：
  - 被 `select_project_dir()` 和 `_load_package_file_settings()` 引用

### PackageGui.select_python_files()

- 初始化位置：第 746-775 行
- 作用：手动从项目中选择要打包的 Python 文件。
- 引用内容：无
- 被引用位置：
  - 被“选择打包文件”按钮触发

### PackageGui.select_icon_file()

- 初始化位置：第 777-812 行
- 作用：选择图标文件，并在需要时回退到默认图标。
- 引用内容：无
- 被引用位置：
  - 被“选择图标文件”按钮触发

### PackageGui._refresh_resource_lists()

- 初始化位置：第 814-824 行
- 作用：刷新电脑路径和项目内相对路径列表。
- 引用内容：无
- 被引用位置：
  - 被 `add_resource_entry()` 和 `.package` 自动导入逻辑引用

### PackageGui.add_resource_entry()

- 初始化位置：第 826-861 行
- 作用：打开资源文件对话框，并要求确认目标路径。
- 引用内容：无
- 被引用位置：
  - 被“添加打包资源”按钮触发

### PackageGui.select_output_dir()

- 初始化位置：第 863-872 行
- 作用：选择输出目录。
- 引用内容：无
- 被引用位置：
  - 被“选择输出目录”按钮触发

### PackageGui.start_packaging()

- 初始化位置：第 874-908 行
- 作用：校验参数并启动后台打包线程。
- 引用内容：无
- 被引用位置：
  - 被“开始打包”按钮触发

### PackageGui.on_packaging_finished(result)

- 初始化位置：第 910-929 行
- 作用：处理打包完成状态并弹出结果窗口。
- 引用内容：
  - `result`
- 被引用位置：
  - 被后台线程 `finished` 信号连接

### PackageGui.open_output_folder()

- 初始化位置：第 931-943 行
- 作用：打开打包输出目录。
- 引用内容：无
- 被引用位置：
  - 被成功提示框按钮引用

### PackageGui.open_log_file()

- 初始化位置：第 945-956 行
- 作用：打开日志文件。
- 引用内容：无
- 被引用位置：
  - 被“查看日志”按钮引用

### main()

- 初始化位置：第 958-981 行
- 作用：程序入口，负责设置应用图标和显示窗口。
- 引用内容：无
- 被引用位置：
  - 被脚本入口 `if __name__ == "__main__":` 调用

---

## 6. `.package` 配置说明

项目支持在项目根目录创建 `.package` 文件，用于自动加载打包参数。格式说明如下：

- 注释：所有 `#` 后面的内容会被忽略
- 空行会被忽略
- 每行一个参数：`key=value`
- 主要参数：
  - `path`：项目绝对路径
  - `pack_file`：要打包的 Python 文件名，多个用 `;` 分隔
  - `add_file`：资源文件列表，路径使用项目内相对路径，如 `/assets/package.ico`
  - `ico_path`：图标文件路径，使用项目内相对路径
  - `setting`：勾选设置，格式为 `生成单文件,加快打包,隐藏命令行`，例如 `1,1,1`

读取配置后会自动：

- 填充项目目录
- 自动选择对应 Python 文件
- 自动导入资源
- 自动设置图标路径
- 自动勾选打包选项
- 记录日志

---

## 7. 使用建议

1. 先确认项目目录有效且包含 Python 文件。
2. 如需自动化打包，可在根目录放置 `.package` 文件。
3. 如需新功能，优先保持函数职责清晰，不要在一个函数中混合 UI 与打包逻辑。
4. 新增常量、变量或函数后，必须同步更新本帮助文档。
5. 读取配置、执行打包和输出日志时，必须保留完整日志记录，便于后续排查问题。
