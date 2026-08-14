import datetime
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
try:
    import ctypes
except Exception:
    ctypes = None

from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QProgressBar,
)

# 全局常量
def resolve_runtime_base_dir():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        executable_path = Path(sys.executable).resolve()
        if executable_path.exists():
            return executable_path.parent
    return Path(__file__).resolve().parent


def normalize_resource_target(target_path, include_leading_slash=True):
    normalized = str(target_path or "").strip().replace("\\", "/")
    normalized = normalized.strip()
    if not normalized:
        normalized = "assets"
    if include_leading_slash:
        if not normalized.startswith("/"):
            normalized = f"/{normalized.lstrip('/')}"
    else:
        normalized = normalized.lstrip("/")
    normalized = normalized.replace("//", "/")
    return normalized


BASE_DIR = resolve_runtime_base_dir()  # 项目根目录
FONTS_DIR = BASE_DIR / "fonts"  # 字体目录
ASSETS_DIR = BASE_DIR / "assets"  # 资源目录
DEFAULT_WINDOW_ICON = ASSETS_DIR / "package.ico"
OUTPUT_PATH = Path(r"D:\output")  # 输出目录
LOG_FILE = ASSETS_DIR / "package_tool.log"  # 日志文件路径
WINDOW_WIDTH = 1280  # 窗口宽度
WINDOW_HEIGHT = 760  # 窗口高度
LOG_PANEL_WIDTH = 580  # 日志面板宽度
LIST_HEIGHT = 180  # 文件列表高度
TEXT_BOX_HEIGHT = 92  # 资源和日志显示框高度
BUTTON_COLOR = "#0f6cbd"
BUTTON_HOVER_COLOR = "#125fb7"
BUTTON_DISABLED_COLOR = "#9db7cb"
BUTTON_DISABLED_TEXT = "#eef4fa"
BACKGROUND_COLOR = "#f4f6fb"
TEXT_COLOR = "#1f2937"
BORDER_COLOR = "#d7dee8"
PANEL_RADIUS = 10
BUTTON_FONT_NAME = "Microsoft YaHei"
BUTTON_FONT_SIZE = 11
ICON_FONT_NAME = "IconFont"
ICON_FONT_SIZE = 16
LOG_FONT_NAME = "LogFont"
LOG_FONT_SIZE = 9
BODY_FONT_NAME = "Microsoft YaHei"
BODY_FONT_SIZE = 10

ICON_FONT_FILE = FONTS_DIR / "icon_font.ttf"
LOG_FONT_FILE = FONTS_DIR / "log_font.ttf"
BODY_FONT_FILE = FONTS_DIR / "body_font.ttf"


def get_time():  # 获取当前时间
    formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


def format_log_message(message, level="INFO"):  # 生成统一日志格式
    return f"[{get_time()}][{level}]: {message}"


def write_log(message, level="INFO", log_mode_f=1):  # 将步骤信息写入日志文件
    if log_mode_f == 0:
        return
    if log_mode_f == 1:
        log_message = format_log_message(message, level)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
        return
    print("日志模式错误，无法写入日志。错误信息如下")
    print(f"message: {message}")
    print(f"Log_Mode_F: {log_mode_f}")


def load_custom_font(font_path, fallback_name):
    if font_path.exists():
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        if font_id >= 0:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                return families[0]
    return fallback_name


def load_font_families():
    global ICON_FONT_NAME, LOG_FONT_NAME, BODY_FONT_NAME
    ICON_FONT_NAME = load_custom_font(ICON_FONT_FILE, ICON_FONT_NAME)
    LOG_FONT_NAME = load_custom_font(LOG_FONT_FILE, LOG_FONT_NAME)
    BODY_FONT_NAME = load_custom_font(BODY_FONT_FILE, BODY_FONT_NAME)


def ensure_runtime_dirs():  # 确保资源目录和输出目录存在
    ASSETS_DIR.mkdir(exist_ok=True)
    OUTPUT_PATH.mkdir(exist_ok=True)
    if not LOG_FILE.exists():
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"[{get_time()}][INFO]: 日志文件已初始化\n")
    write_log("资源目录与输出目录已准备就绪", "INFO")


ensure_runtime_dirs()


def strip_package_quotes(value):
    if value is None:
        return ""
    text = str(value).strip()
    while len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        text = text[1:-1].strip()
    return text


def parse_package_file(project_dir):
    project_dir = Path(project_dir)
    config_path = project_dir / ".package"
    if not config_path.exists():
        write_log(f"未发现 .package 配置文件: {config_path}", "INFO")
        return {}

    config = {}
    with open(config_path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "#" in line:
                line = line.split("#", 1)[0].strip()
            if not line or "=" not in line:
                continue
            key, value = [part.strip() for part in line.split("=", 1)]
            key = key.strip()
            value = strip_package_quotes(value)
            if not key:
                continue
            if key == "add_file" and key in config:
                existing = config[key]
                if isinstance(existing, list):
                    existing.append(value)
                else:
                    config[key] = [existing, value]
            elif key in config:
                config[key] = value
            else:
                config[key] = value
    write_log(f"已读取 .package 配置文件: {config_path}", "INFO")
    return config


def resolve_project_relative_value(value, project_dir):
    project_dir = Path(project_dir)
    cleaned = strip_package_quotes(value).replace("\\", "/").strip()
    if not cleaned:
        return project_dir
    if cleaned.startswith("/"):
        cleaned = cleaned.lstrip("/")
    candidate = Path(cleaned)
    if not candidate.is_absolute():
        candidate = project_dir / candidate
    return candidate


def collect_python_files(project_dir):  # 扫描项目目录下的 Python 文件
    if not project_dir or not Path(project_dir).exists():
        write_log("项目目录不存在，无法扫描 Python 文件", "WARNING")
        return []
    project_dir = Path(project_dir)
    ignored_dirs = {".git", ".idea", ".venv", "venv", "__pycache__", "node_modules"}
    python_files = []
    for search_path in project_dir.rglob("*.py"):
        if any(part in ignored_dirs for part in search_path.parts):
            continue
        python_files.append(search_path)
    python_files = sorted(python_files, key=lambda p: str(p))
    write_log(f"已扫描到 {len(python_files)} 个 Python 文件", "INFO")
    return python_files


def build_pyinstaller_command(entry_scripts, project_name, output_dir, icon_path=None, resources_path=None, onefile=False, fast_mode=False, hide_console=False, reduce_size=False, resource_entries=None):  # 构造 PyInstaller 打包命令
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--distpath",
        str(output_dir),
        "--workpath",
        str(output_dir / "build"),
        "--specpath",
        str(output_dir / "spec"),
    ]
    if fast_mode or reduce_size:
        command.extend(["--log-level", "WARN"])
        command.extend(["--noupx"])
        command.extend(["--clean"])
    if reduce_size:
        command.extend(["--optimize", "2"])
        if sys.platform.startswith("linux"):
            command.append("--strip")
    if hide_console:
        command.append("--windowed")
    if onefile:
        command.append("--onefile")
    else:
        command.append("--onedir")
    command.extend(["--name", project_name])
    trusted_icon = Path(icon_path) if icon_path else DEFAULT_WINDOW_ICON
    if trusted_icon and trusted_icon.exists():
        command.extend(["--icon", str(trusted_icon)])
    if resource_entries:
        for source_path, target_path in resource_entries:
            source = Path(source_path)
            if source.exists():
                packaging_target = normalize_resource_target(target_path, include_leading_slash=False)
                command.extend(["--add-data", f"{source}{os.pathsep}{packaging_target}"])
    elif resources_path and Path(resources_path).exists():
        command.extend(["--add-data", f"{resources_path}{os.pathsep}resources"])
    command.extend([str(script) for script in entry_scripts])
    write_log(f"已生成打包命令: {' '.join(command)}", "INFO")
    return command


def run_pyinstaller(entry_scripts, project_dir, project_name, output_dir, icon_path=None, resources_path=None, onefile=False, fast_mode=False, log_emitter=None, progress_emitter=None, hide_console=False, reduce_size=False, resource_entries=None):  # 执行打包流程
    pyinstaller_scripts = [Path(script) for script in entry_scripts]
    if not pyinstaller_scripts:
        write_log("没有选择任何 Python 文件，打包已取消", "WARNING")
        return None
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    def emit_log(message, level="INFO"):
        write_log(message, level)
        if callable(log_emitter):
            log_emitter(format_log_message(message, level), level)

    def emit_progress(value):
        if callable(progress_emitter):
            progress_emitter(max(0, min(100, int(value))))

    emit_progress(5)

    command = build_pyinstaller_command(
        pyinstaller_scripts,
        project_name,
        output_dir,
        icon_path,
        resources_path,
        onefile,
        fast_mode=fast_mode,
        hide_console=hide_console,
        reduce_size=reduce_size,
        resource_entries=resource_entries,
    )
    emit_log(f"开始在项目目录 {project_dir} 中执行打包", "INFO")

    output_lines = []
    try:
        with subprocess.Popen(
            command,
            cwd=str(project_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        ) as process:
            for raw_line in process.stdout:
                if raw_line is None:
                    continue
                line = raw_line.rstrip()
                if not line:
                    continue
                output_lines.append(line)
                if "Analyzing" in line:
                    emit_progress(20)
                elif "Building EXE" in line or "Building COLLECT" in line or "Collecting" in line:
                    emit_progress(45)
                elif "Fixing" in line or "UPX" in line or "copying" in line.lower() or "adding" in line.lower():
                    emit_progress(70)
                elif "completed successfully" in line.lower() or "finished" in line.lower():
                    emit_progress(90)
                emit_log(line, "INFO")
            returncode = process.wait()
            completed_process = subprocess.CompletedProcess(command, returncode, stdout="\n".join(output_lines), stderr="")
    except FileNotFoundError as exc:
        emit_log(f"调用 PyInstaller 失败: {exc}", "ERROR")
        return None

    if completed_process.returncode == 0:
        emit_progress(100)
        emit_log("打包已成功完成，输出目录已生成", "SUCCESS")
        if resource_entries:
            for source_path, relative_target in resource_entries:
                source = Path(source_path)
                if not source.exists():
                    continue
                normalized_relative = normalize_resource_target(relative_target, include_leading_slash=False)
                destination = output_dir / "dist" / project_name / normalized_relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                if source.is_dir():
                    shutil.copytree(source, destination, dirs_exist_ok=True)
                else:
                    shutil.copy2(source, destination)
                emit_log(f"已复制资源：{source} -> {destination}", "INFO")
        return completed_process

    error_text = completed_process.stderr or completed_process.stdout or "未知打包错误"
    emit_log(f"打包失败: {error_text}", "ERROR")
    return completed_process


class PackagingWorker(QObject):  # 后台打包线程
    finished = pyqtSignal(object)
    log_signal = pyqtSignal(str, str)
    progress_signal = pyqtSignal(int)

    def __init__(self, entry_scripts, project_dir, project_name, output_dir, icon_path, resources_path, onefile, fast_mode=False, hide_console=False, reduce_size=False, resource_entries=None):
        super().__init__()
        self.entry_scripts = entry_scripts
        self.project_dir = project_dir
        self.project_name = project_name
        self.output_dir = output_dir
        self.icon_path = icon_path
        self.resources_path = resources_path
        self.onefile = onefile
        self.fast_mode = fast_mode
        self.hide_console = hide_console
        self.reduce_size = reduce_size
        self.resource_entries = resource_entries or []

    def run(self):  # 执行打包任务
        result = run_pyinstaller(
            self.entry_scripts,
            self.project_dir,
            self.project_name,
            self.output_dir,
            self.icon_path,
            self.resources_path,
            self.onefile,
            log_emitter=self.log_signal.emit,
            progress_emitter=self.progress_signal.emit,
            fast_mode=self.fast_mode,
            hide_console=self.hide_console,
            reduce_size=self.reduce_size,
            resource_entries=self.resource_entries,
        )
        self.finished.emit(result)


class PackageGui(QMainWindow):  # 创建主界面窗口
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python 项目打包助手")
        if DEFAULT_WINDOW_ICON.exists():
            self.setWindowIcon(QIcon(str(DEFAULT_WINDOW_ICON)))
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setFont(QFont(BODY_FONT_NAME, BODY_FONT_SIZE))
        self.project_dir = None
        self.detected_files = []
        self.selected_scripts = []
        self.icon_path = None
        self.resources_path = None
        self.output_dir = OUTPUT_PATH
        self.selected_resource_paths = []
        self.resource_entries = []
        self.packaging_thread = None
        self.packaging_worker = None
        self._build_ui()
        write_log("GUI 主窗口已创建", "INFO")
        self._append_log(format_log_message("GUI 主窗口已创建", "INFO"))

    def _build_ui(self):  # 创建界面控件
        self.setStyleSheet(
            f"""
            QMainWindow {{ background: {BACKGROUND_COLOR}; color: {TEXT_COLOR}; }}
            QWidget {{ font-family: '{BODY_FONT_NAME}'; }}
            QPushButton {{
                background: {BUTTON_COLOR};
                color: white;
                border: none;
                border-radius: {PANEL_RADIUS}px;
                padding: 8px 14px;
                min-height: 32px;
                font-weight: 500;
            }}
            QPushButton:hover {{ background: {BUTTON_HOVER_COLOR}; }}
            QPushButton:disabled {{ background: {BUTTON_DISABLED_COLOR}; color: {BUTTON_DISABLED_TEXT}; }}
            QLineEdit, QPlainTextEdit, QListWidget {{
                border: 1px solid {BORDER_COLOR};
                border-radius: 8px;
                padding: 6px;
                background: white;
            }}
            QProgressBar {{
                border: 1px solid {BORDER_COLOR};
                border-radius: 8px;
                text-align: center;
                background: white;
                color: {TEXT_COLOR};
            }}
            QProgressBar::chunk {{ background: {BUTTON_COLOR}; border-radius: 8px; }}
            QFrame {{ background: transparent; }}
            QLabel {{ color: #334155; }}
            """
        )

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(10)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(8)
        self.splitter.setChildrenCollapsible(False)

        left_widget = QWidget(self)
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        row1 = QHBoxLayout()
        select_project_btn = QPushButton("选择 Python 项目")
        select_project_btn.clicked.connect(self.select_project_dir)
        select_project_btn.setFont(QFont(BUTTON_FONT_NAME, BUTTON_FONT_SIZE))
        row1.addWidget(select_project_btn)
        self.project_path_label = QLabel("未选择项目")
        self.project_path_label.setWordWrap(True)
        row1.addWidget(self.project_path_label, 1)
        left_layout.addLayout(row1)

        row2 = QHBoxLayout()
        select_file_btn = QPushButton("选择要打包的 Python 文件")
        select_file_btn.clicked.connect(self.select_python_files)
        select_file_btn.setFont(QFont(BUTTON_FONT_NAME, BUTTON_FONT_SIZE))
        row2.addWidget(select_file_btn)
        self.file_count_label = QLabel("未选择打包文件")
        self.file_count_label.setWordWrap(True)
        row2.addWidget(self.file_count_label, 1)
        left_layout.addLayout(row2)

        file_frame = QFrame(self)
        file_frame.setFrameShape(QFrame.StyledPanel)
        file_frame_layout = QVBoxLayout(file_frame)
        file_frame_layout.addWidget(QLabel("已识别的 Python 文件"))
        self.file_list_widget = QListWidget()
        self.file_list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.file_list_widget.setMinimumHeight(LIST_HEIGHT)
        self.file_list_widget.setMaximumHeight(LIST_HEIGHT)
        file_frame_layout.addWidget(self.file_list_widget)
        left_layout.addWidget(file_frame)

        icon_row = QHBoxLayout()
        icon_btn = QPushButton("选择图标文件")
        icon_btn.clicked.connect(self.select_icon_file)
        icon_btn.setFont(QFont(BUTTON_FONT_NAME, BUTTON_FONT_SIZE))
        icon_row.addWidget(icon_btn)
        self.icon_path_label = QLabel("未选择图标，将默认使用package.ico")
        self.icon_path_label.setWordWrap(True)
        self.icon_path_label.setFont(QFont(BODY_FONT_NAME, BODY_FONT_SIZE))
        icon_row.addWidget(self.icon_path_label, 1)
        left_layout.addLayout(icon_row)

        resource_row = QHBoxLayout()
        resource_btn = QPushButton("添加打包资源")
        resource_btn.clicked.connect(self.add_resource_entry)
        resource_btn.setFont(QFont(BUTTON_FONT_NAME, BUTTON_FONT_SIZE))
        resource_row.addWidget(resource_btn)
        self.resources_path_label = QLabel("未添加资源")
        self.resources_path_label.setWordWrap(True)
        resource_row.addWidget(self.resources_path_label, 1)
        left_layout.addLayout(resource_row)

        self.resources_panel = QWidget(self)
        resources_panel_layout = QHBoxLayout(self.resources_panel)
        resources_panel_layout.setContentsMargins(0, 0, 0, 0)
        resources_panel_layout.setSpacing(6)

        left_resources_widget = QWidget(self)
        left_resources_layout = QVBoxLayout(left_resources_widget)
        left_resources_layout.setContentsMargins(0, 0, 0, 0)
        left_resources_layout.addWidget(QLabel("电脑中的路径"))
        self.resource_source_list = QListWidget()
        self.resource_source_list.setMinimumHeight(TEXT_BOX_HEIGHT)
        self.resource_source_list.setMaximumHeight(TEXT_BOX_HEIGHT)
        left_resources_layout.addWidget(self.resource_source_list)

        right_resources_widget = QWidget(self)
        right_resources_layout = QVBoxLayout(right_resources_widget)
        right_resources_layout.setContentsMargins(0, 0, 0, 0)
        right_resources_layout.addWidget(QLabel("打包项目中的相对路径"))
        self.resource_target_list = QListWidget()
        self.resource_target_list.setMinimumHeight(TEXT_BOX_HEIGHT)
        self.resource_target_list.setMaximumHeight(TEXT_BOX_HEIGHT)
        right_resources_layout.addWidget(self.resource_target_list)

        resources_panel_layout.addWidget(left_resources_widget, 1)
        resources_panel_layout.addWidget(right_resources_widget, 1)
        left_layout.addWidget(self.resources_panel)

        output_row = QHBoxLayout()
        output_btn = QPushButton("选择输出目录")
        output_btn.clicked.connect(self.select_output_dir)
        output_btn.setFont(QFont(BUTTON_FONT_NAME, BUTTON_FONT_SIZE))
        output_row.addWidget(output_btn)
        self.output_path_label = QLabel(str(self.output_dir))
        self.output_path_label.setWordWrap(True)
        output_row.addWidget(self.output_path_label, 1)
        left_layout.addLayout(output_row)

        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("打包名称："))
        default_project_name = BASE_DIR.name if BASE_DIR.exists() else "my_app"
        self.project_name_input = QLineEdit(default_project_name)
        name_row.addWidget(self.project_name_input, 1)
        self.onefile_checkbox = QCheckBox("生成单文件")
        self.onefile_checkbox.setFont(QFont(BUTTON_FONT_NAME, BUTTON_FONT_SIZE))
        name_row.addWidget(self.onefile_checkbox)
        self.fast_build_checkbox = QCheckBox("快速打包（跳过 UPX，降低日志级别）")
        self.fast_build_checkbox.setChecked(False)
        self.fast_build_checkbox.setFont(QFont(BUTTON_FONT_NAME, BUTTON_FONT_SIZE))
        name_row.addWidget(self.fast_build_checkbox)
        left_layout.addLayout(name_row)

        options_row = QHBoxLayout()
        self.hide_console_checkbox = QCheckBox("隐藏命令行界面")
        self.hide_console_checkbox.setFont(QFont(BUTTON_FONT_NAME, BUTTON_FONT_SIZE))
        self.hide_console_checkbox.setChecked(False)
        options_row.addWidget(self.hide_console_checkbox)
        self.reduce_size_checkbox = QCheckBox("减少包体积（优化、去除 UPX）")
        self.reduce_size_checkbox.setChecked(False)
        self.reduce_size_checkbox.setFont(QFont(BUTTON_FONT_NAME, BUTTON_FONT_SIZE))
        options_row.addWidget(self.reduce_size_checkbox)
        options_row.addStretch(1)
        left_layout.addLayout(options_row)

        button_row = QHBoxLayout()
        self.start_btn = QPushButton("开始打包")
        self.start_btn.clicked.connect(self.start_packaging)
        self.start_btn.setFont(QFont(BUTTON_FONT_NAME, BUTTON_FONT_SIZE))
        button_row.addWidget(self.start_btn)
        log_btn = QPushButton("查看日志")
        log_btn.clicked.connect(self.open_log_file)
        log_btn.setFont(QFont(BUTTON_FONT_NAME, BUTTON_FONT_SIZE))
        button_row.addWidget(log_btn)
        left_layout.addLayout(button_row)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("打包进度: %p%")
        self.progress_bar.setVisible(False)
        left_layout.addWidget(self.progress_bar)

        log_widget = QWidget(self)
        log_layout = QVBoxLayout(log_widget)
        log_layout.setContentsMargins(0, 0, 0, 0)
        log_layout.setSpacing(6)
        log_layout.addWidget(QLabel("打包日志"))
        self.log_text_view = QPlainTextEdit()
        self.log_text_view.setReadOnly(True)
        self.log_text_view.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.log_text_view.setPlaceholderText("日志内容会在这里显示")
        self.log_text_view.setFont(QFont(LOG_FONT_NAME, LOG_FONT_SIZE))
        log_layout.addWidget(self.log_text_view)

        self.splitter.addWidget(left_widget)
        self.splitter.addWidget(log_widget)
        self.splitter.setSizes([WINDOW_WIDTH - LOG_PANEL_WIDTH, LOG_PANEL_WIDTH])
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 0)
        root_layout.addWidget(self.splitter)

    def _append_log(self, message):  # 向日志面板追加内容
        hbar = self.log_text_view.horizontalScrollBar()
        vbar = self.log_text_view.verticalScrollBar()
        horizontal_value = hbar.value()
        at_bottom = vbar.value() == vbar.maximum()
        self.log_text_view.appendPlainText(message)
        hbar.setValue(horizontal_value)
        if at_bottom:
            self.log_text_view.verticalScrollBar().setValue(self.log_text_view.verticalScrollBar().maximum())

    @pyqtSlot(int)
    def handle_progress(self, value):
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(value)

    @pyqtSlot(str, str)
    def handle_log_message(self, message, level):  # 在主线程中更新日志面板
        self._append_log(message)

    def _apply_setting_value(self, setting_value):
        values = [part.strip() for part in str(setting_value).split(",") if part.strip()]
        if len(values) < 4:
            if len(values) == 3:
                self.onefile_checkbox.setChecked(values[0] == "1")
                self.fast_build_checkbox.setChecked(values[1] == "1")
                self.hide_console_checkbox.setChecked(values[2] == "1")
                self.reduce_size_checkbox.setChecked(False)
                write_log(f"配置中的 setting 参数仅包含 3 个值，已按兼容模式处理: {setting_value}", "WARNING")
                self._append_log(format_log_message(f"配置中的 setting 参数仅包含 3 个值，已按兼容模式处理: {setting_value}", "WARNING"))
                return
            write_log(f"配置中的 setting 参数格式无效: {setting_value}", "WARNING")
            return
        self.onefile_checkbox.setChecked(values[0] == "1")
        self.fast_build_checkbox.setChecked(values[1] == "1")
        self.hide_console_checkbox.setChecked(values[2] == "1")
        self.reduce_size_checkbox.setChecked(values[3] == "1")
        write_log(f"已根据 .package 中的 setting 参数更新打包设置: {setting_value}", "INFO")
        self._append_log(format_log_message(f"已根据 .package 中的 setting 参数更新打包设置: {setting_value}", "INFO"))

    def _apply_pack_file_selection(self, pack_file_value):
        names = [part.strip() for part in str(pack_file_value).split(";") if part.strip()]
        selected_paths = []
        for name in names:
            candidate = resolve_project_relative_value(name, self.project_dir)
            if candidate.exists():
                selected_paths.append(candidate)
        self.selected_scripts = selected_paths
        self.file_list_widget.clearSelection()
        self.file_list_widget.setCurrentRow(-1)
        for file_path in self.selected_scripts:
            try:
                relative_path = str(file_path.relative_to(self.project_dir))
            except ValueError:
                relative_path = str(file_path)
            for index in range(self.file_list_widget.count()):
                if self.file_list_widget.item(index).text() == relative_path:
                    self.file_list_widget.item(index).setSelected(True)
                    break
        self.file_count_label.setText(f"已选择 {len(self.selected_scripts)} 个文件")
        write_log(f"已从 .package 自动选择打包文件: {[str(path) for path in self.selected_scripts]}", "INFO")

    def _apply_add_file_entries(self, add_file_value):
        if isinstance(add_file_value, (list, tuple)):
            raw_entries = []
            for entry in add_file_value:
                if entry is None:
                    continue
                raw_entries.extend([part.strip() for part in str(entry).split(";") if part.strip()])
        else:
            raw_entries = [part.strip() for part in str(add_file_value).split(";") if part.strip()]

        added_entries = []
        for item in raw_entries:
            candidate = resolve_project_relative_value(item, self.project_dir)
            if not candidate.exists():
                write_log(f"未找到 .package 中的 add_file 资源: {candidate}", "WARNING")
                continue
            item_path = str(item).replace("\\", "/").strip()
            normalized_item = item_path.lstrip("/")
            relative_dir = str(Path(normalized_item).parent).replace("\\", "/").strip("/")
            if not relative_dir:
                relative_dir = "assets"
            added_entries.append((str(candidate), relative_dir))
        if added_entries:
            self.resource_entries = added_entries
            write_log(f"已从 .package 自动添加资源: {added_entries}", "INFO")
            self._append_log(format_log_message(f"已从 .package 自动添加资源: {added_entries}", "INFO"))
        self._refresh_resource_lists()

    def _load_package_file_settings(self):
        if not self.project_dir or not self.project_dir.exists():
            return
        config_file = self.project_dir / ".package"
        if not config_file.exists():
            write_log(f"未发现项目配置文件 .package，路径为: {config_file}", "INFO")
            return
        config = parse_package_file(self.project_dir)
        if not config:
            return

        if not self.project_name_input.text().strip() or self.project_name_input.text().strip() == "my_app":
            self.project_name_input.setText(self.project_dir.name)

        path_value = config.get("path")
        if path_value:
            candidate = resolve_project_relative_value(path_value, self.project_dir)
            if candidate.exists() and candidate.is_dir():
                self.project_dir = candidate
                self.project_path_label.setText(str(self.project_dir))
                write_log(f"已根据 .package 中的 path 设定项目目录: {self.project_dir}", "INFO")

        self.detected_files = collect_python_files(self.project_dir)
        self.populate_file_listbox()

        pack_value = config.get("pack_file")
        if pack_value:
            self._apply_pack_file_selection(pack_value)

        add_value = config.get("add_file")
        if add_value:
            self._apply_add_file_entries(add_value)

        ico_value = config.get("ico_path")
        if ico_value:
            candidate = resolve_project_relative_value(ico_value, self.project_dir)
            if candidate.exists():
                self.icon_path = candidate
                self.icon_path_label.setText(str(candidate))
                write_log(f"已根据 .package 中的 ico_path 配置图标: {candidate}", "INFO")

        setting_value = config.get("setting")
        if setting_value:
            self._apply_setting_value(setting_value)

        reduce_size_value = config.get("reduce_size")
        if reduce_size_value is not None:
            self.reduce_size_checkbox.setChecked(str(reduce_size_value).strip().lower() in {"1", "true", "yes", "on"})

    def select_project_dir(self):  # 选择 Python 项目目录
        directory = QFileDialog.getExistingDirectory(self, "选择 Python 项目目录", str(BASE_DIR))
        if not directory:
            write_log("用户取消了项目目录选择", "INFO")
            return
        self.project_dir = Path(directory)
        self.project_path_label.setText(str(self.project_dir))
        if not self.project_name_input.text().strip() or self.project_name_input.text().strip() == "my_app":
            self.project_name_input.setText(self.project_dir.name)
        self.detected_files = collect_python_files(self.project_dir)
        self.populate_file_listbox()
        self._load_package_file_settings()
        write_log(f"已选择项目目录: {self.project_dir}", "INFO")
        self._append_log(format_log_message(f"已选择项目目录: {self.project_dir}", "INFO"))

    def populate_file_listbox(self):  # 将识别到的 Python 文件填充到列表框中
        self.file_list_widget.clear()
        for python_file in self.detected_files:
            relative_path = str(python_file.relative_to(self.project_dir))
            self.file_list_widget.addItem(relative_path)
        self.file_count_label.setText(f"已识别 {len(self.detected_files)} 个文件")

    def select_python_files(self):  # 从项目中选择要打包的 Python 文件
        if not self.project_dir:
            QMessageBox.warning(self, "提示", "请先选择一个 Python 项目目录")
            return
        selected_files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择要打包的 Python 文件",
            str(self.project_dir),
            "Python 文件 (*.py);;所有文件 (*.*)",
        )
        if not selected_files:
            write_log("用户取消了打包文件选择", "INFO")
            return
        self.selected_scripts = [Path(file_path) for file_path in selected_files]
        self.file_list_widget.clearSelection()
        self.file_list_widget.setCurrentRow(-1)
        for file_path in self.selected_scripts:
            try:
                relative_path = str(file_path.relative_to(self.project_dir))
            except ValueError:
                relative_path = str(file_path)
            for index in range(self.file_list_widget.count()):
                if self.file_list_widget.item(index).text() == relative_path:
                    self.file_list_widget.item(index).setSelected(True)
                    break
        self.file_count_label.setText(f"已选择 {len(self.selected_scripts)} 个文件")
        write_log(f"已选择打包文件: {self.selected_scripts}", "INFO")
        self._append_log(format_log_message(f"已选择打包文件: {self.selected_scripts}", "INFO"))

    def select_icon_file(self):  # 选择打包图标文件
        icon_file, _ = QFileDialog.getOpenFileName(
            self,
            "选择图标文件",
            str(ASSETS_DIR),
            "图标文件 (*.ico);;图片文件 (*.png *.jpg *.jpeg);;所有文件 (*.*)",
        )
        if not icon_file:
            write_log("用户取消了图标选择", "INFO")
            return
        selected_icon = Path(icon_file)
        self.icon_path = selected_icon
        self.icon_path_label.setText(str(self.icon_path))
        if DEFAULT_WINDOW_ICON.exists():
            self.setWindowIcon(QIcon(str(DEFAULT_WINDOW_ICON)))
        if sys.platform.startswith("win") and self.icon_path.suffix.lower() != ".ico":
            QMessageBox.information(
                self,
                "提示",
                "窗口图标已使用 assets/package.ico，Windows 可执行文件图标仍需 .ico 文件。",
            )
            write_log(f"已选择图标文件: {self.icon_path}，窗口图标使用默认 package.ico。", "WARNING")
        else:
            write_log(f"已选择图标文件: {self.icon_path}", "INFO")
        self._append_log(format_log_message(f"已选择图标文件: {self.icon_path}", "INFO"))

    def _refresh_resource_lists(self):
        self.resource_source_list.clear()
        self.resource_target_list.clear()
        for source_path, target_path in self.resource_entries:
            self.resource_source_list.addItem(source_path)
            self.resource_target_list.addItem(normalize_resource_target(target_path, include_leading_slash=True))
        if self.resource_entries:
            self.resources_path_label.setText(f"已添加 {len(self.resource_entries)} 个资源")
        else:
            self.resources_path_label.setText("未添加资源")

    def add_resource_entry(self):  # 添加打包资源并指定在项目中的相对路径
        resource_file, _ = QFileDialog.getOpenFileName(
            self,
            "选择要打包的资源文件",
            str(BASE_DIR),
            "所有文件 (*.*)",
        )
        if not resource_file:
            write_log("用户取消了资源添加", "INFO")
            return

        selected_resource = Path(resource_file)
        dialog = QDialog(self)
        dialog.setWindowTitle("确认资源路径")
        dialog.setModal(True)
        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.addWidget(QLabel("当前选择的文件路径："))
        source_label = QLabel(str(selected_resource))
        source_label.setWordWrap(True)
        dialog_layout.addWidget(source_label)
        dialog_layout.addWidget(QLabel("请输入在打包项目中的相对路径："))
        target_input = QLineEdit("/assets")
        dialog_layout.addWidget(target_input)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        dialog_layout.addWidget(button_box)

        if dialog.exec_() != QDialog.Accepted:
            write_log("用户取消了资源确认", "INFO")
            return

        relative_target = normalize_resource_target(target_input.text(), include_leading_slash=False)
        if not relative_target:
            relative_target = "assets"

        self.resource_entries.append((str(selected_resource), relative_target))
        self._refresh_resource_lists()
        write_log(f"已添加资源: {selected_resource} -> {relative_target}", "INFO")
        self._append_log(format_log_message(f"已添加资源: {selected_resource} -> {relative_target}", "INFO"))

    def select_output_dir(self):  # 选择打包输出目录
        output_dir = QFileDialog.getExistingDirectory(self, "选择打包输出目录", str(OUTPUT_PATH))
        if not output_dir:
            write_log("用户取消了输出目录选择", "INFO")
            return
        self.output_dir = Path(output_dir)
        self.output_path_label.setText(str(self.output_dir))
        write_log(f"已选择输出目录: {self.output_dir}", "INFO")
        self._append_log(format_log_message(f"已选择输出目录: {self.output_dir}", "INFO"))

    def start_packaging(self):  # 开始执行打包流程
        if not self.project_dir:
            QMessageBox.critical(self, "错误", "请先选择项目目录")
            return
        selected_items = self.file_list_widget.selectedItems()
        if selected_items:
            self.selected_scripts = [self.project_dir / item.text() for item in selected_items]
        if not self.selected_scripts:
            QMessageBox.critical(self, "错误", "请至少选择一个要打包的 Python 文件")
            return
        project_name = self.project_name_input.text().strip() or self.project_dir.name
        onefile = self.onefile_checkbox.isChecked()
        reduce_size = self.reduce_size_checkbox.isChecked()
        self.start_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        self.packaging_thread = QThread(self)
        self.packaging_worker = PackagingWorker(
            self.selected_scripts,
            self.project_dir,
            project_name,
            self.output_dir,
            self.icon_path,
            self.resources_path,
            onefile,
            fast_mode=self.fast_build_checkbox.isChecked(),
            hide_console=self.hide_console_checkbox.isChecked(),
            reduce_size=reduce_size,
            resource_entries=self.resource_entries,
        )
        self.packaging_worker.moveToThread(self.packaging_thread)
        self.packaging_thread.started.connect(self.packaging_worker.run)
        self.packaging_worker.log_signal.connect(self.handle_log_message)
        self.packaging_worker.progress_signal.connect(self.handle_progress)
        self.packaging_worker.finished.connect(self.on_packaging_finished)
        self.packaging_worker.finished.connect(self.packaging_thread.quit)
        self.packaging_worker.finished.connect(self.packaging_worker.deleteLater)
        self.packaging_thread.finished.connect(self.packaging_thread.deleteLater)
        self.packaging_thread.start()
        write_log("已启动后台打包线程", "INFO")
        self._append_log(format_log_message("已启动后台打包线程", "INFO"))

    @pyqtSlot(object)
    def on_packaging_finished(self, result):  # 处理打包任务结束
        self.start_btn.setEnabled(True)
        self.progress_bar.setValue(100)
        if result is None:
            QMessageBox.critical(self, "打包失败", "打包过程未完成，请查看日志")
            return
        if result.returncode == 0:
            message_box = QMessageBox(self)
            message_box.setIcon(QMessageBox.Information)
            message_box.setWindowTitle("成功")
            message_box.setText(f"项目已打包成功，输出目录：{self.output_dir}")
            open_button = message_box.addButton("打开输出目录", QMessageBox.AcceptRole)
            close_button = message_box.addButton("关闭", QMessageBox.RejectRole)
            message_box.exec_()
            if message_box.clickedButton() == open_button:
                self.open_output_folder()
        else:
            QMessageBox.critical(self, "打包失败", "打包过程返回了错误，请查看日志")

    def open_output_folder(self):
        try:
            if sys.platform.startswith("win"):
                os.startfile(str(self.output_dir))
            elif sys.platform.startswith("darwin"):
                subprocess.run(["open", str(self.output_dir)], check=False)
            else:
                subprocess.run(["xdg-open", str(self.output_dir)], check=False)
        except Exception as exc:
            write_log(f"打开输出目录失败: {exc}", "WARNING")
            QMessageBox.warning(self, "提示", f"无法打开输出目录：{exc}")

    def open_log_file(self):  # 打开日志文件以便查看
        try:
            if sys.platform.startswith("win"):
                os.startfile(LOG_FILE)
            else:
                subprocess.run(["xdg-open", str(LOG_FILE)], check=False)
        except Exception as exc:
            write_log(f"打开日志文件失败: {exc}", "WARNING")
            QMessageBox.warning(self, "提示", f"无法直接打开日志文件：{exc}")


def main():  # 程序入口
    # 在 Windows 上设置 AppUserModelID，可以帮助任务栏显示正确的图标
    if sys.platform.startswith("win") and ctypes is not None:
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Cover0719.PackPython")
        except Exception:
            pass
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    load_font_families()
    app.setFont(QFont(BODY_FONT_NAME, BODY_FONT_SIZE))
    # 优先在已打包（frozen）环境下使用 exe 自身图标，保证任务栏/窗口显示一致
    if getattr(sys, "frozen", False):
        try:
            exe_icon = QIcon(sys.executable)
            if not exe_icon.isNull():
                app.setWindowIcon(exe_icon)
            else:
                if DEFAULT_WINDOW_ICON.exists():
                    app.setWindowIcon(QIcon(str(DEFAULT_WINDOW_ICON)))
        except Exception:
            if DEFAULT_WINDOW_ICON.exists():
                app.setWindowIcon(QIcon(str(DEFAULT_WINDOW_ICON)))
    else:
        if DEFAULT_WINDOW_ICON.exists():
            app.setWindowIcon(QIcon(str(DEFAULT_WINDOW_ICON)))
    window = PackageGui()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()