#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信自动化工具 - PyQt5 GUI界面
提供现代化的图形用户界面，支持所有核心功能
"""

import sys
import os
import threading
import time
import pyautogui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QPushButton, QLabel, 
                            QLineEdit, QTextEdit, QGroupBox, QFrame, QMessageBox,
                            QProgressBar, QTabWidget, QSplitter, QScrollArea,
                            QComboBox, QCheckBox, QSpinBox, QStackedWidget, QListWidget, QListWidgetItem, QRadioButton,
                            QShortcut)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPixmap, QPainter, QLinearGradient, QTextCursor, QKeySequence

try:
    import keyboard as keyboard_hotkey
    KEYBOARD_HOTKEY_AVAILABLE = True
except ImportError:
    keyboard_hotkey = None
    KEYBOARD_HOTKEY_AVAILABLE = False
    print("⚠️ keyboard 模块不可用，F10全局热键功能将不可用")

try:
    from pynput import keyboard as pynput_keyboard
    PYNPUT_HOTKEY_AVAILABLE = True
except ImportError:
    pynput_keyboard = None
    PYNPUT_HOTKEY_AVAILABLE = False
    print("⚠️ pynput 模块不可用，备用全局热键监听将不可用")

# 导入OCR引擎模块（延迟初始化）
try:
    from rapid_ocr_engine import get_ocr_engine
    # 不在导入时立即初始化，而是在需要时才初始化
    ocr_engine = None
    RAPID_OCR_AVAILABLE = False
    print("✅ GUI环境：RapidOCR引擎模块已导入（延迟初始化）")
except ImportError as e:
    print(f"❌ GUI环境：RapidOCR引擎导入失败: {e}")
    ocr_engine = None
    RAPID_OCR_AVAILABLE = False

def _init_gui_ocr_engines():
    """GUI环境中的OCR引擎初始化函数"""
    global ocr_engine, RAPID_OCR_AVAILABLE
    if ocr_engine is None:
        try:
            ocr_engine = get_ocr_engine()
            RAPID_OCR_AVAILABLE = ocr_engine and ocr_engine.is_available()
            if RAPID_OCR_AVAILABLE:
                print("✅ GUI环境：RapidOCR核心引擎已加载")
            else:
                print("❌ GUI环境：RapidOCR核心引擎加载失败")
        except Exception as e:
            print(f"❌ GUI环境：RapidOCR引擎初始化失败: {e}")
            ocr_engine = None
            RAPID_OCR_AVAILABLE = False

# 只使用RapidOCR，不再导入其他OCR模块

# 直接导入微信自动化功能（不使用GUI包装器）
try:
    from wechat_core_engine import (
        search_contact, search_group, find_and_click_pengyouquan_with_dianzan,
        ensure_wechat_is_active, pengyouquan_dianzan_action, pengyouquan_multi_dianzan_action,
        find_and_click_pengyouquan, adjust_pengyouquan_window_size,
        optimized_pengyouquan_dianzan_action, pengyouquan_like_all_action
    )
    print("✅ GUI环境：微信核心引擎已加载")
except ImportError as e:
    print(f"❌ GUI环境：微信自动化引擎导入失败: {e}")

# 导入微信启动器
try:
    from wechat_launcher import WeChatLauncher
    wechat_launcher = WeChatLauncher()
    print("✅ GUI环境：微信启动器已加载")
except ImportError as e:
    print(f"❌ GUI环境：微信启动器导入失败: {e}")
    wechat_launcher = None
    # 如果导入失败，创建占位函数
    def search_contact(*args, **kwargs):
        return False
    def search_group(*args, **kwargs):
        return False
    def find_and_click_pengyouquan_with_dianzan(*args, **kwargs):
        return False
    def ensure_wechat_is_active(*args, **kwargs):
        return False
    def pengyouquan_dianzan_action(*args, **kwargs):
        return False
    def pengyouquan_multi_dianzan_action(*args, **kwargs):
        return False
    def find_and_click_pengyouquan(*args, **kwargs):
        return False
    
    def adjust_pengyouquan_window_size(*args, **kwargs):
        return False
    
    def optimized_pengyouquan_dianzan_action(*args, **kwargs):
        return False
    
    def pengyouquan_like_all_action(*args, **kwargs):
        return {'success': 0, 'failed': 0, 'skipped': 0}



class ModernButton(QPushButton):
    """二次元可爱按钮样式 ♡"""
    def __init__(self, text, color="primary"):
        super().__init__(text)
        self.color = color
        self.setMinimumHeight(50)
        self.setFont(QFont("微软雅黑", 11, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)
        self.apply_style()
    
    def apply_style(self):
        if self.color == "primary":
            style = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FF6B9D, stop:1 #FF85A1);
                    border: 3px solid #FFF;
                    border-radius: 18px;
                    color: white;
                    font-weight: bold;
                    padding: 12px 24px;
                    font-size: 12pt;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FF85A1, stop:1 #FF6B9D);
                    border: 3px solid #FFD700;
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FF4D82, stop:1 #FF6B9D);
                    border: 3px solid #FFA500;
                }
                QPushButton:disabled {
                    background: #FFE4E1;
                    color: #CCC;
                    border: 3px solid #FFB6C1;
                }
            """
        elif self.color == "secondary":
            style = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #E6E6FA, stop:1 #DDA0DD);
                    border: 3px solid #FFF;
                    border-radius: 18px;
                    color: white;
                    font-weight: bold;
                    padding: 12px 24px;
                    font-size: 12pt;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #F0E6FA, stop:1 #E0B0E0);
                    border: 3px solid #FFD700;
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #D0D0F0, stop:1 #D090D0);
                    border: 3px solid #FFA500;
                }
                QPushButton:disabled {
                    background: #F0F0F0;
                    color: #CCC;
                    border: 3px solid #E0E0E0;
                }
            """
        elif self.color == "warning":
            style = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FFB6C1, stop:1 #FFC0CB);
                    border: 3px solid #FFF;
                    border-radius: 18px;
                    color: white;
                    font-weight: bold;
                    padding: 12px 24px;
                    font-size: 12pt;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FFC0CB, stop:1 #FFD0D5);
                    border: 3px solid #FFD700;
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FFA0AA, stop:1 #FFB0B8);
                    border: 3px solid #FFA500;
                }
                QPushButton:disabled {
                    background: #FFE4E1;
                    color: #CCC;
                    border: 3px solid #FFD0D5;
                }
            """
        elif self.color == "danger":
            style = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FF69B4, stop:1 #FF1493);
                    border: 3px solid #FFF;
                    border-radius: 18px;
                    color: white;
                    font-weight: bold;
                    padding: 12px 24px;
                    font-size: 12pt;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FF85C1, stop:1 #FF4DB8);
                    border: 3px solid #FFD700;
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FF4D9D, stop:1 #FF0080);
                    border: 3px solid #FFA500;
                }
                QPushButton:disabled {
                    background: #FFE4E1;
                    color: #CCC;
                    border: 3px solid #FFB6C1;
                }
            """
        
        self.setStyleSheet(style)

class ModernLineEdit(QLineEdit):
    """现代化输入框样式"""
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder + " ♡")
        self.setMinimumHeight(40)
        self.setFont(QFont("Microsoft YaHei", 10))
        self.setStyleSheet("""
            QLineEdit {
                border: 3px solid #FFB6C1;
                border-radius: 15px;
                padding: 10px 18px;
                font-size: 10pt;
                font-family: "Microsoft YaHei";
                background-color: white;
                text-align: left;
                line-height: 24px;
            }
            QLineEdit:focus {
                border-color: #FF69B4;
                background-color: #f9f9f9;
            }
            QLineEdit:hover {
                border-color: #bdbdbd;
            }
        """)

class ModernTextEdit(QTextEdit):
    """二次元可爱文本框样式 ✿"""
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Microsoft YaHei", 10))
        self.setStyleSheet("""
            QTextEdit {
                border: 3px solid #FFB6C1;
                border-radius: 15px;
                padding: 12px;
                font-size: 10pt;
                font-family: "Microsoft YaHei";
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFF5F7, stop:1 #FFFFFF);
                selection-background-color: #FF69B4;
                line-height: 1.6;
            }
            QTextEdit:focus {
                border-color: #FF69B4;
            }
        """)
    
    def append(self, text):
        """重写append方法，添加文本后自动滚动到底部"""
        super().append(text)
        # 使用QTimer延迟执行滚动，确保UI更新完成后再滚动
        QTimer.singleShot(0, self._scroll_to_bottom)
    
    def _scroll_to_bottom(self):
        """滚动到底部的具体实现"""
        try:
            # 移动光标到文档末尾并确保可见
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
            # 同时设置滚动条到最大值作为备用方案
            scrollbar = self.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        except Exception as e:
            # 忽略任何发生的错误，确保不影响主程序执行
            pass

class WorkerThread(QThread):
    """工作线程，用于执行耗时操作"""
    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(str)
    
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        try:
            self.progress.emit("正在执行操作...")
            result = self.function(*self.args, **self.kwargs)
            if result:
                self.finished.emit(True, "操作成功完成！")
            else:
                self.finished.emit(False, "操作失败，请检查输入或重试")
        except Exception as e:
            self.finished.emit(False, f"操作出错: {str(e)}")

class WeChatAutomationGUI(QMainWindow):
    """微信自动化工具主界面"""
    # 定义信号，用于从worker线程安全地更新UI
    status_updated = pyqtSignal(str, str)  # (message, color)
    aux_like_triggered = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.worker_thread = None
        self._switching_type = False  # 初始化切换标志
        self._previous_mode = 'contact'  # 初始化为联系人模式
        self._stop_broadcast = False  # 停止群发消息标志
        self._stop_moments = False  # 停止朋友圈操作标志
        self._aux_like_hotkey_registered = False
        self._aux_like_hotkey_id = None
        self._aux_like_pynput_listener = None
        self._aux_like_pynput_registered = False
        self._aux_like_last_trigger_time = 0.0
        self._aux_like_lock = threading.Lock()
        self.init_ui()
        # 连接status_updated信号到update_status_impl方法（在主线程执行）
        self.status_updated.connect(self.update_status_impl)
        self.aux_like_triggered.connect(self.execute_aux_like_once)

        # 兜底：窗口内F10快捷键（当程序窗口有焦点时可用）
        self.aux_like_shortcut = QShortcut(QKeySequence("F10"), self)
        self.aux_like_shortcut.setContext(Qt.ApplicationShortcut)
        self.aux_like_shortcut.activated.connect(lambda: self.aux_like_triggered.emit(True))
        # 加载上次的输入内容（需要在UI创建后调用）
        self.load_last_inputs()
        # 连接实时保存信号（在加载输入内容之后连接）
        self.connect_auto_save_signals_except_radio()
        # 连接单选按钮的信号（在加载完成后连接）
        self.connect_radio_signals()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("♡ WeChat自动化工具 v2.2 - 二次元可爱版 ♡")
        self.setGeometry(80, 50, 1200, 950)
        self.setMinimumSize(1100, 900)
        
        # 设置应用程序图标（如果有的话）
        try:
            import sys
            import os
            # 获取资源文件路径的函数
            def get_resource_path(relative_path):
                try:
                    # PyInstaller打包后的临时目录
                    base_path = sys._MEIPASS
                except AttributeError:
                    # 开发环境，使用当前脚本所在目录
                    base_path = os.path.dirname(os.path.abspath(__file__))
                return os.path.join(base_path, relative_path)
            
            icon_path = get_resource_path("assets/pengyouquan.png")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            print(f"设置窗口图标失败: {e}")
        
        # 设置主题样式
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FFE4E1, stop:0.5 #FFF0F5, stop:1 #FFE4E1);
            }
            QTabWidget::pane {
                border: 3px solid #FFB6C1;
                background-color: white;
                border-radius: 15px;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFB6C1, stop:1 #FFC0CB);
                color: white;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #FF69B4;
            }
            QTabBar::tab:hover {
                background-color: #f0f0f0;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建标题
        self.create_header(main_layout)
        
        # 创建水平布局容器（左侧导航 + 右侧内容）
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # 创建左侧导航栏
        nav_widget = self.create_navigation_bar()
        content_layout.addWidget(nav_widget)
        
        # 创建右侧内容区域
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("""
            QStackedWidget {
                background-color: white;
                border: none;
            }
        """)
        
        # 添加各个功能页面
        self.content_stack.addWidget(self.create_moments_tab())
        self.content_stack.addWidget(self.create_message_broadcast_tab())
        self.content_stack.addWidget(self.create_settings_tab())
        
        content_layout.addWidget(self.content_stack, 1)  # 右侧内容区域占据剩余空间
        
        # 创建内容容器
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)
        
        # 创建状态栏
        self.create_status_bar(main_layout)
        
    def create_header(self, layout):
        """创建标题区域"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF69B4, stop:1 #FF1493);
                border-radius: 0px;
                padding: 20px;
            }
        """)
        header_frame.setFixedHeight(100)
        
        header_layout = QHBoxLayout(header_frame)
        
        # 标题文本
        title_label = QLabel("WeChat Bulk Message Assistant")
        title_label.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        title_label.setStyleSheet("color: white; background: transparent;")
        
        subtitle_label = QLabel("智能化微信操作，提升工作效率")
        subtitle_label.setFont(QFont("Microsoft YaHei", 9))
        subtitle_label.setStyleSheet("color: rgba(255,255,255,0.8); background: transparent;")
        
        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        title_layout.setSpacing(5)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # 微信启动按钮
        self.launch_btn = ModernButton("🚀 启动微信", "secondary")
        self.launch_btn.clicked.connect(self.launch_wechat)
        self.launch_btn.setFixedSize(120, 50)
        self.launch_btn.setToolTip("启动或激活微信窗口")
        
        header_layout.addWidget(self.launch_btn)
        
        layout.addWidget(header_frame)
    
    def create_navigation_bar(self):
        """创建左侧导航栏"""
        nav_widget = QWidget()
        nav_widget.setFixedWidth(200)
        nav_widget.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                border-right: 1px solid #34495e;
            }
        """)
        
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(0, 20, 0, 20)
        nav_layout.setSpacing(5)
        
        # 导航按钮列表
        nav_items = [
            ("💖 朋友圈", 0),
            ("📤 群发消息", 1),
            ("⚙️ 设置", 2)
        ]
        
        self.nav_buttons = []
        for text, index in nav_items:
            btn = QPushButton(text)
            btn.setFixedHeight(50)
            btn.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #ecf0f1;
                    border: none;
                    text-align: left;
                    padding-left: 20px;
                    border-radius: 0px;
                }
                QPushButton:hover {
                    background-color: #34495e;
                    color: #FF69B4;
                }
                QPushButton:checked {
                    background-color: #FF69B4;
                    color: white;
                    border-left: 4px solid #2ecc71;
                }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=index: self.switch_page(idx))
            
            self.nav_buttons.append(btn)
            nav_layout.addWidget(btn)
        
        # 默认选中第一个
        self.nav_buttons[0].setChecked(True)
        
        nav_layout.addStretch()
        return nav_widget
    
    def switch_page(self, index):
        """切换页面"""
        # 取消所有按钮的选中状态
        for btn in self.nav_buttons:
            btn.setChecked(False)
        
        # 选中当前按钮
        self.nav_buttons[index].setChecked(True)
        
        # 切换到对应页面
        self.content_stack.setCurrentIndex(index)
    
    def create_message_broadcast_tab(self):
        """创建群发消息页面（合并联系人和群聊搜索）"""
        broadcast_widget = QWidget()
        layout = QVBoxLayout(broadcast_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 搜索注意事项
        info_frame = self.create_info_frame(
            "🔍 注意事项",
            "⑴请确保微信已打开，并处于主界面\n⑵联系人名称需要完全匹配，请使用备注名\n⑶支持多个联系人/群聊，用英文逗号分隔，如：张三,李四"
        )
        layout.addWidget(info_frame)
        
        # 消息和搜索设置区域（左右结构）
        main_input_layout = QHBoxLayout()
        main_input_layout.setSpacing(20)
        
        # 左侧：消息设置
        message_group = QGroupBox("💬 消息设置")
        message_group.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        message_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 3px solid #FFB6C1;
                border-radius: 15px;
                margin-top: 10px;
                padding-top: 10px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFF5F7, stop:1 #FFFFFF);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #FF69B4;
            }
        """)
        
        message_layout = QVBoxLayout(message_group)
        message_layout.setSpacing(10)
        
        # 自定义消息输入
        message_label = QLabel("自定义消息:")
        message_label.setFont(QFont("Microsoft YaHei", 10))
        
        self.message_input = ModernTextEdit()
        self.message_input.setPlaceholderText("请输入要发送的消息内容...")
        self.message_input.setMaximumHeight(55)
        self.message_input.setFont(QFont("Microsoft YaHei", 10))
        
        message_layout.addWidget(message_label)
        message_layout.addWidget(self.message_input)
        
        # 等待时间设置
        wait_time_layout = QHBoxLayout()
        wait_time_label = QLabel("发送间隔:")
        wait_time_label.setFont(QFont("Microsoft YaHei", 10))
        
        self.wait_time_spinbox = QSpinBox()
        self.wait_time_spinbox.setRange(1, 10)  # 1-10分钟
        self.wait_time_spinbox.setValue(2)  # 默认2分钟
        self.wait_time_spinbox.setSuffix(" 分钟")
        self.wait_time_spinbox.setFont(QFont("Microsoft YaHei", 10))
        self.wait_time_spinbox.setStyleSheet("""
            QSpinBox {
                border: 3px solid #FFB6C1;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
                background-color: white;
                min-width: 80px;
            }
            QSpinBox:focus {
                border-color: #FF69B4;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                border: none;
                background-color: #f0f0f0;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f6f7fa, stop: 1 #dadbde);
            }
            QSpinBox::up-button:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #dadbde, stop: 1 #f6f7fa);
            }
            QSpinBox::up-arrow {
                image: none;
                width: 7px;
                height: 7px;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-bottom: 4px solid #666666;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-bottom-right-radius: 3px;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f6f7fa, stop: 1 #dadbde);
            }
            QSpinBox::down-button:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #dadbde, stop: 1 #f6f7fa);
            }
            QSpinBox::down-arrow {
                image: none;
                width: 7px;
                height: 7px;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-top: 4px solid #666666;
            }
            QSpinBox::up-button:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #FF69B4, stop: 1 #FF1493);
            }
            QSpinBox::down-button:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #FF69B4, stop: 1 #FF1493);
            }
            QSpinBox::up-arrow:hover {
                border-bottom-color: white;
            }
            QSpinBox::down-arrow:hover {
                border-top-color: white;
            }
        """)
        self.wait_time_spinbox.setToolTip("设置每个联系人/群聊之间的发送间隔时间")
        
        wait_time_info = QLabel("(等待时间)")
        wait_time_info.setFont(QFont("Microsoft YaHei", 9))
        wait_time_info.setStyleSheet("color: #666666;")
        
        wait_time_layout.addWidget(wait_time_label)
        wait_time_layout.addWidget(self.wait_time_spinbox)
        wait_time_layout.addWidget(wait_time_info)
        wait_time_layout.addStretch()
        
        message_layout.addLayout(wait_time_layout)
        
        # 右侧：搜索设置
        search_group = QGroupBox("🔍 搜索设置")
        search_group.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        search_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 3px solid #FFB6C1;
                border-radius: 15px;
                margin-top: 10px;
                padding-top: 10px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFF5F7, stop:1 #FFFFFF);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #FF69B4;
            }
        """)
        
        search_layout = QVBoxLayout(search_group)
        search_layout.setSpacing(10)
        
        # 类型选择
        type_layout = QHBoxLayout()
        type_label = QLabel("发送类型:")
        type_label.setFont(QFont("Microsoft YaHei", 10))
        
        self.contact_radio = QRadioButton("联系人")
        self.contact_radio.setFont(QFont("Microsoft YaHei", 10))
        self.contact_radio.setChecked(True)  # 默认选中联系人
        
        self.group_radio = QRadioButton("群聊")
        self.group_radio.setFont(QFont("Microsoft YaHei", 10))
        
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.contact_radio)
        type_layout.addWidget(self.group_radio)
        type_layout.addStretch()
        
        search_layout.addLayout(type_layout)
        
        # 名称输入
        self.name_input = ModernLineEdit("多个用英文逗号分隔")
        self.name_input.setMaximumHeight(80)  # 与自定义消息框高度一致
        
        search_layout.addWidget(self.name_input)
        
        # 添加到左右布局
        main_input_layout.addWidget(message_group)
        main_input_layout.addWidget(search_group)
        
        layout.addLayout(main_input_layout)
        
        # 操作按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(0, 20, 0, 0)
        
        # 操作按钮
        self.broadcast_btn = ModernButton("启动", "primary")
        self.broadcast_btn.clicked.connect(self.start_broadcast)
        self.broadcast_btn.setFixedSize(120, 50)
        self.broadcast_btn.setToolTip("启动群发消息功能")
        
        self.stop_broadcast_btn = ModernButton("停止", "danger")
        self.stop_broadcast_btn.clicked.connect(self.stop_broadcast_operation)
        self.stop_broadcast_btn.setFixedSize(100, 50)
        self.stop_broadcast_btn.setEnabled(False)
        self.stop_broadcast_btn.setToolTip("停止当前正在执行的操作")
        
        button_layout.addWidget(self.broadcast_btn)
        button_layout.addWidget(self.stop_broadcast_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        layout.addStretch()
        return broadcast_widget
    

    
    def create_moments_tab(self):
        """创建朋友圈功能页面"""
        moments_widget = QWidget()
        layout = QVBoxLayout(moments_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 功能说明
        info_frame = self.create_info_frame(
            "👍 点赞和评论",
            "⑴请先在微信中手动打开朋友圈窗口\n⑵可选择给所有人点赞或给特定人点赞\n⑶给特定人点赞时，支持多个用户英文逗号分隔如：张三,李四,王五\n⑷给所有人点赞时，可设置黑名单排除不想点赞的用户"
        )
        layout.addWidget(info_frame)
        
        # 点赞模式选择
        mode_group = QGroupBox("点赞模式")
        mode_group.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        mode_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 3px solid #FFB6C1;
                border-radius: 15px;
                margin-top: 15px;
                padding-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFF5F7, stop:1 #FFFFFF);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #FF69B4;
                font-family: "微软雅黑";
                font-size: 11pt;
            }
        """)
        
        mode_layout = QHBoxLayout(mode_group)
        mode_layout.setSpacing(20)
        
        self.specific_users_radio = QRadioButton("只给特定人点赞")
        self.specific_users_radio.setChecked(True)
        self.specific_users_radio.setFont(QFont("Microsoft YaHei", 10))
        self.specific_users_radio.toggled.connect(self.on_like_mode_changed)
        
        self.all_users_radio = QRadioButton("给所有人点赞（可设置黑名单）")
        self.all_users_radio.setFont(QFont("Microsoft YaHei", 10))
        
        mode_layout.addWidget(self.specific_users_radio)
        mode_layout.addWidget(self.all_users_radio)
        mode_layout.addStretch()
        
        layout.addWidget(mode_group)
        
        # 输入区域
        input_group = QGroupBox("点赞设置")
        input_group.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        input_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 3px solid #FFB6C1;
                border-radius: 15px;
                margin-top: 15px;
                padding-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFF5F7, stop:1 #FFFFFF);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #FF69B4;
                font-family: "微软雅黑";
                font-size: 11pt;
            }
        """)
        
        input_layout = QVBoxLayout(input_group)
        input_layout.setSpacing(15)
        
        # 用户名称输入
        name_layout = QHBoxLayout()
        name_label = QLabel("用户名称:")
        name_label.setFont(QFont("Microsoft YaHei", 10))
        name_label.setFixedWidth(100)
        
        self.moments_name_input = ModernLineEdit("请输入要点赞的用户名称，多个用英文逗号分隔")
        
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.moments_name_input)
        input_layout.addLayout(name_layout)
        
        # 黑名单输入（仅在给所有人点赞时显示）
        blacklist_layout = QHBoxLayout()
        blacklist_label = QLabel("黑名单:")
        blacklist_label.setFont(QFont("Microsoft YaHei", 10))
        blacklist_label.setFixedWidth(100)
        
        self.moments_blacklist_input = ModernLineEdit("输入不想点赞的用户名称，多个用英文逗号分隔")
        self.moments_blacklist_input.setEnabled(False)
        
        blacklist_layout.addWidget(blacklist_label)
        blacklist_layout.addWidget(self.moments_blacklist_input)
        input_layout.addLayout(blacklist_layout)
        
        # 等待时间设置（改为秒）
        wait_time_layout = QHBoxLayout()
        wait_time_label = QLabel("点赞间隔:")
        wait_time_label.setFont(QFont("Microsoft YaHei", 10))
        wait_time_label.setFixedWidth(100)
        
        self.moments_wait_time_spinbox = QSpinBox()
        self.moments_wait_time_spinbox.setRange(1, 600)  # 1-600秒（10分钟）
        self.moments_wait_time_spinbox.setValue(5)  # 默认5秒
        self.moments_wait_time_spinbox.setSuffix(" 秒")
        self.moments_wait_time_spinbox.setFont(QFont("Microsoft YaHei", 10))
        self.moments_wait_time_spinbox.setStyleSheet("""
            QSpinBox {
                border: 3px solid #FFB6C1;
                border-radius: 6px;
                padding: 1px;
                font-size: 10pt;
                background-color: white;
                min-width: 80px;
            }
            QSpinBox:focus {
                border-color: #FF69B4;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f6f7fa, stop: 1 #dadbde);
            }
            QSpinBox::up-button:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #dadbde, stop: 1 #f6f7fa);
            }
            QSpinBox::up-arrow {
                image: none;
                width: 7px;
                height: 7px;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-bottom: 4px solid #666666;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-bottom-right-radius: 3px;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f6f7fa, stop: 1 #dadbde);
            }
            QSpinBox::down-button:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #dadbde, stop: 1 #f6f7fa);
            }
            QSpinBox::down-arrow {
                image: none;
                width: 7px;
                height: 7px;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-top: 4px solid #666666;
            }
            QSpinBox::up-button:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #FF69B4, stop: 1 #FF1493);
            }
            QSpinBox::down-button:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #FF69B4, stop: 1 #FF1493);
            }
            QSpinBox::up-arrow:hover {
                border-bottom-color: white;
            }
            QSpinBox::down-arrow:hover {
                border-top-color: white;
            }
        """)
        self.moments_wait_time_spinbox.setToolTip("设置每个用户点赞之间的间隔时间（秒）")
        
        wait_time_info = QLabel("(每个用户之间的等待时间)")
        wait_time_info.setFont(QFont("Microsoft YaHei", 9))
        wait_time_info.setStyleSheet("color: #666666;")
        
        wait_time_layout.addWidget(wait_time_label)
        wait_time_layout.addWidget(self.moments_wait_time_spinbox)
        wait_time_layout.addWidget(wait_time_info)
        wait_time_layout.addStretch()
        
        input_layout.addLayout(wait_time_layout)
        
        # 点赞类型选择
        like_type_layout = QHBoxLayout()
        like_type_label = QLabel("点赞类型:")
        like_type_label.setFont(QFont("微软雅黑", 10))
        like_type_label.setFixedWidth(100)
        
        self.like_text_checkbox = QCheckBox("✿ 文字朋友圈")
        self.like_text_checkbox.setChecked(True)
        self.like_text_checkbox.setFont(QFont("微软雅黑", 10))
        self.like_text_checkbox.setStyleSheet("""
            QCheckBox {
                color: #FF1493;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 5px;
                border: 3px solid #FFB6C1;
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FF69B4, stop:1 #FF1493);
                border: 3px solid #FF1493;
            }
            QCheckBox::indicator:hover {
                border: 3px solid #FF69B4;
            }
        """)
        
        self.like_image_checkbox = QCheckBox("♡ 图片朋友圈")
        self.like_image_checkbox.setChecked(True)
        self.like_image_checkbox.setFont(QFont("微软雅黑", 10))
        self.like_image_checkbox.setStyleSheet("""
            QCheckBox {
                color: #FF1493;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 5px;
                border: 3px solid #FFB6C1;
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FF69B4, stop:1 #FF1493);
                border: 3px solid #FF1493;
            }
            QCheckBox::indicator:hover {
                border: 3px solid #FF69B4;
            }
        """)
        
        self.like_video_checkbox = QCheckBox("★ 视频朋友圈")
        self.like_video_checkbox.setChecked(True)
        self.like_video_checkbox.setFont(QFont("微软雅黑", 10))
        self.like_video_checkbox.setStyleSheet("""
            QCheckBox {
                color: #FF1493;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 5px;
                border: 3px solid #FFB6C1;
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FF69B4, stop:1 #FF1493);
                border: 3px solid #FF1493;
            }
            QCheckBox::indicator:hover {
                border: 3px solid #FF69B4;
            }
        """)
        
        like_type_layout.addWidget(like_type_label)
        like_type_layout.addWidget(self.like_text_checkbox)
        like_type_layout.addWidget(self.like_image_checkbox)
        like_type_layout.addWidget(self.like_video_checkbox)
        like_type_layout.addStretch()
        
        input_layout.addLayout(like_type_layout)
        
        layout.addWidget(input_group)
        
        # 评论功能设置（独立区域）
        comment_group = QGroupBox("评论设置")
        comment_group.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        comment_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 3px solid #FFB6C1;
                border-radius: 15px;
                margin-top: 15px;
                padding-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFF5F7, stop:1 #FFFFFF);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #FF69B4;
                font-family: "微软雅黑";
                font-size: 11pt;
            }
        """)
        
        comment_layout = QVBoxLayout(comment_group)
        comment_layout.setSpacing(15)
        
        # 是否评论勾选框
        checkbox_layout = QHBoxLayout()
        self.enable_comment_checkbox = QCheckBox("启用或关闭")
        self.enable_comment_checkbox.setFont(QFont("Microsoft YaHei", 10))
        # 动态生成样式表，处理资源文件路径
        try:
            import sys
            import os
            # 获取资源文件路径的函数
            def get_resource_path(relative_path):
                try:
                    # PyInstaller打包后的临时目录
                    base_path = sys._MEIPASS
                except AttributeError:
                    # 开发环境，使用当前脚本所在目录
                    base_path = os.path.dirname(os.path.abspath(__file__))
                return os.path.join(base_path, relative_path)
            
            checkmark_path = get_resource_path("assets/checkmark.svg")
            # 将路径转换为URL格式，处理Windows路径分隔符
            checkmark_url = checkmark_path.replace("\\", "/")
            
            checkbox_style = f"""
            QCheckBox {{
                font-size: 14px;
                color: #333;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 3px solid #FFB6C1;
                border-radius: 3px;
                background-color: white;
            }}
            QCheckBox::indicator:checked {{
                background-color: #FF69B4;
                border-color: #FF69B4;
                image: url({checkmark_url});
            }}
            QCheckBox::indicator:hover {{
                border-color: #FF69B4;
            }}
            """
            self.enable_comment_checkbox.setStyleSheet(checkbox_style)
        except Exception as e:
            print(f"设置复选框样式失败: {e}")
            # 使用不带图标的备用样式
            self.enable_comment_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #333;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 3px solid #FFB6C1;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #FF69B4;
                border-color: #FF69B4;
            }
            QCheckBox::indicator:hover {
                border-color: #FF69B4;
            }
            """)
        self.enable_comment_checkbox.setToolTip("勾选后将在点赞时同时进行评论")
        
        checkbox_layout.addWidget(self.enable_comment_checkbox)
        checkbox_layout.addStretch()
        comment_layout.addLayout(checkbox_layout)
        
        # 随机评论内容输入
        comment_text_layout = QHBoxLayout()
        comment_text_label = QLabel("评论内容:")
        comment_text_label.setFont(QFont("Microsoft YaHei", 10))
        comment_text_label.setFixedWidth(100)
        
        self.comment_text_input = ModernLineEdit("多条评论用英文逗号分隔，将随机选择")
        self.comment_text_input.setEnabled(False)  # 默认禁用
        
        # 连接勾选框状态变化事件
        self.enable_comment_checkbox.stateChanged.connect(self.on_comment_checkbox_changed)
        
        comment_text_layout.addWidget(comment_text_label)
        comment_text_layout.addWidget(self.comment_text_input)
        comment_layout.addLayout(comment_text_layout)
        
        layout.addWidget(comment_group)
        
        # 窗口设置区域已移动到设置页面
        
        # 操作按钮区域（移到点赞设置外面）
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(0, 20, 0, 0)
        
        # 启动按钮（与群发消息样式一致）
        self.start_moments_btn = ModernButton("▶ 开始点赞", "primary")
        self.start_moments_btn.clicked.connect(self.start_moments_function)
        self.start_moments_btn.setFixedSize(120, 50)
        self.start_moments_btn.setToolTip("请先在微信中手动打开朋友圈，然后点击此按钮开始点赞")
        
        # 停止按钮（与群发消息保持一致）
        self.stop_moments_btn = ModernButton("停止", "danger")
        self.stop_moments_btn.clicked.connect(self.stop_moments_operation)
        self.stop_moments_btn.setFixedSize(100, 50)
        self.stop_moments_btn.setEnabled(False)
        self.stop_moments_btn.setToolTip("停止当前正在执行的操作")
        
        button_layout.addWidget(self.start_moments_btn)
        button_layout.addWidget(self.stop_moments_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)

        # 辅助点赞（F10）
        helper_group = QGroupBox("辅助点赞")
        helper_group.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        helper_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 3px solid #FFB6C1;
                border-radius: 15px;
                margin-top: 15px;
                padding-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFF5F7, stop:1 #FFFFFF);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #FF69B4;
                font-family: "微软雅黑";
                font-size: 11pt;
            }
        """)

        helper_layout = QVBoxLayout(helper_group)
        helper_layout.setSpacing(12)

        self.aux_like_enable_checkbox = QCheckBox("启用F10辅助点赞（每按一次F10仅执行一次）")
        self.aux_like_enable_checkbox.setFont(QFont("Microsoft YaHei", 10))
        self.aux_like_enable_checkbox.setToolTip("启用后按F10会在当前鼠标位置点击一次，再在偏移位置点击一次")
        self.aux_like_enable_checkbox.stateChanged.connect(self.on_aux_like_hotkey_changed)
        helper_layout.addWidget(self.aux_like_enable_checkbox)

        helper_config_layout = QHBoxLayout()
        helper_config_layout.setSpacing(10)

        offset_x_label = QLabel("水平偏移:")
        offset_x_label.setFont(QFont("Microsoft YaHei", 10))
        self.aux_like_offset_x_spinbox = QSpinBox()
        self.aux_like_offset_x_spinbox.setRange(-500, 500)
        self.aux_like_offset_x_spinbox.setValue(120)
        self.aux_like_offset_x_spinbox.setSuffix(" px")
        self.aux_like_offset_x_spinbox.setFont(QFont("Microsoft YaHei", 10))

        offset_y_label = QLabel("垂直偏移:")
        offset_y_label.setFont(QFont("Microsoft YaHei", 10))
        self.aux_like_offset_y_spinbox = QSpinBox()
        self.aux_like_offset_y_spinbox.setRange(-500, 500)
        self.aux_like_offset_y_spinbox.setValue(0)
        self.aux_like_offset_y_spinbox.setSuffix(" px")
        self.aux_like_offset_y_spinbox.setFont(QFont("Microsoft YaHei", 10))

        delay_label = QLabel("两次点击间隔:")
        delay_label.setFont(QFont("Microsoft YaHei", 10))
        self.aux_like_delay_spinbox = QSpinBox()
        self.aux_like_delay_spinbox.setRange(0, 2000)
        self.aux_like_delay_spinbox.setValue(120)
        self.aux_like_delay_spinbox.setSuffix(" ms")
        self.aux_like_delay_spinbox.setFont(QFont("Microsoft YaHei", 10))

        scroll_label = QLabel("完成后下滚:")
        scroll_label.setFont(QFont("Microsoft YaHei", 10))
        self.aux_like_scroll_lines_spinbox = QSpinBox()
        self.aux_like_scroll_lines_spinbox.setRange(0, 500)
        self.aux_like_scroll_lines_spinbox.setValue(0)
        self.aux_like_scroll_lines_spinbox.setSuffix(" 行")
        self.aux_like_scroll_lines_spinbox.setFont(QFont("Microsoft YaHei", 10))
        
        scroll_delay_label = QLabel("下滚前延时:")
        scroll_delay_label.setFont(QFont("Microsoft YaHei", 10))
        self.aux_like_scroll_delay_spinbox = QSpinBox()
        self.aux_like_scroll_delay_spinbox.setRange(0, 5000)
        self.aux_like_scroll_delay_spinbox.setValue(0)
        self.aux_like_scroll_delay_spinbox.setSuffix(" ms")
        self.aux_like_scroll_delay_spinbox.setFont(QFont("Microsoft YaHei", 10))

        self.aux_like_test_btn = ModernButton("测试执行一次", "secondary")
        self.aux_like_test_btn.setFixedSize(130, 42)
        self.aux_like_test_btn.clicked.connect(self.execute_aux_like_once)
        self.aux_like_test_btn.setToolTip("立即执行一次辅助点赞动作（当前点 + 偏移点）")

        helper_config_layout.addWidget(offset_x_label)
        helper_config_layout.addWidget(self.aux_like_offset_x_spinbox)
        helper_config_layout.addWidget(offset_y_label)
        helper_config_layout.addWidget(self.aux_like_offset_y_spinbox)
        helper_config_layout.addWidget(delay_label)
        helper_config_layout.addWidget(self.aux_like_delay_spinbox)
        helper_config_layout.addWidget(scroll_label)
        helper_config_layout.addWidget(self.aux_like_scroll_lines_spinbox)
        helper_config_layout.addWidget(scroll_delay_label)
        helper_config_layout.addWidget(self.aux_like_scroll_delay_spinbox)
        helper_config_layout.addWidget(self.aux_like_test_btn)
        helper_config_layout.addStretch()

        helper_layout.addLayout(helper_config_layout)

        helper_hint = QLabel("说明：F10 触发后仅执行一次，先点击当前鼠标位置，再点击偏移位置，最后可自动下滚指定行数")
        helper_hint.setFont(QFont("Microsoft YaHei", 9))
        helper_hint.setStyleSheet("color: #666666;")
        helper_layout.addWidget(helper_hint)

        layout.addWidget(helper_group)
        
        layout.addStretch()
        return moments_widget
    
    def on_like_mode_changed(self):
        """处理点赞模式切换"""
        if self.specific_users_radio.isChecked():
            # 仅给特定人点赞模式
            self.moments_name_input.setEnabled(True)
            self.moments_name_input.setPlaceholderText("请输入要点赞的用户名称，多个用英文逗号分隔")
            self.moments_blacklist_input.setEnabled(False)
            self.moments_blacklist_input.setPlaceholderText("输入不想点赞的用户名称，多个用英文逗号分隔")
        else:
            # 给所有人点赞模式
            self.moments_name_input.setEnabled(False)
            self.moments_name_input.setPlaceholderText("给所有人点赞模式，此字段不需要")
            self.moments_blacklist_input.setEnabled(True)
            self.moments_blacklist_input.setPlaceholderText("输入不想点赞的用户名称，多个用英文逗号分隔（可留空）")
    
    def on_comment_checkbox_changed(self, state):
        """处理评论功能勾选框状态变化"""
        self.comment_text_input.setEnabled(state == 2)  # 2表示选中状态
        if state == 2:
            self.comment_text_input.setPlaceholderText("请输入评论内容，多条评论用英文逗号分隔，将随机选择")
        else:
            self.comment_text_input.setPlaceholderText("请先勾选启用评论功能")
    
    def create_settings_tab(self):
        """创建设置页面"""
        settings_widget = QWidget()
        layout = QVBoxLayout(settings_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 功能说明
        info_frame = self.create_info_frame(
            "⚙️ 系统设置",
            "配置自动化参数和系统选项"
        )
        layout.addWidget(info_frame)
        
        # 朋友圈窗口设置区域
        window_group = QGroupBox("朋友圈窗口设置")
        window_group.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        window_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 3px solid #FFB6C1;
                border-radius: 15px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #9C27B0;
            }
        """)
        
        window_layout = QVBoxLayout(window_group)
        window_layout.setSpacing(15)
        
        # 朋友圈窗口大小调整选项
        window_resize_layout = QHBoxLayout()
        self.enable_window_resize_checkbox = QCheckBox("自动调整朋友圈窗口大小")
        self.enable_window_resize_checkbox.setFont(QFont("Microsoft YaHei", 10))
        self.enable_window_resize_checkbox.setChecked(True)  # 默认启用
        self.enable_window_resize_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #333;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 3px solid #FFB6C1;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #9C27B0;
                border-color: #9C27B0;
            }
            QCheckBox::indicator:hover {
                border-color: #9C27B0;
            }
        """)
        self.enable_window_resize_checkbox.setToolTip("勾选后将自动调整朋友圈窗口高度为屏幕高度的100%，便于查看更多内容")
        
        window_resize_layout.addWidget(self.enable_window_resize_checkbox)
        window_resize_layout.addStretch()
        window_layout.addLayout(window_resize_layout)
        
        # 窗口大小说明
        window_info_label = QLabel("• 启用后朋友圈窗口将自动调整为屏幕高度的100%\n• 窗口将靠左显示，便于查看更多朋友圈内容")
        window_info_label.setFont(QFont("Microsoft YaHei", 9))
        window_info_label.setStyleSheet("color: #666666; padding-left: 25px;")
        window_layout.addWidget(window_info_label)
        
        layout.addWidget(window_group)
        
        # 设置区域
        settings_group = QGroupBox("说明")
        settings_group.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        settings_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 3px solid #FFB6C1;
                border-radius: 15px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #9C27B0;
            }
        """)
        
        settings_layout = QVBoxLayout(settings_group)
        settings_layout.setSpacing(15)
        
        # 设置说明
        settings_info = QLabel("请勿用于非法用途，否则自己承担责任！")
        settings_info.setFont(QFont("Microsoft YaHei", 10))
        settings_info.setStyleSheet("""
            QLabel {
                color: #666666;
                padding: 15px;
                text-align: center;
                background-color: #f9f9f9;
                border-radius: 5px;
            }
        """)
        settings_info.setAlignment(Qt.AlignCenter)
        settings_layout.addWidget(settings_info)
        
        layout.addWidget(settings_group)
        
        layout.addStretch()
        return settings_widget
    
    def create_info_frame(self, title, description):
        """创建信息展示框"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 15px;
                padding: 1px;
                margin: 1px;
            }
        """)
        # 移除固定高度限制，让内容自适应
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(8)
        layout.setContentsMargins(1, 1, 1, 1)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        title_label.setStyleSheet("color: #495057; background: transparent;")
        
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Microsoft YaHei", 10))
        desc_label.setStyleSheet("color: #6c757d; background: transparent; line-height: 1.5;")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignTop)
        # 设置最小高度以确保多行文本显示
        desc_label.setMinimumHeight(20)
        
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        
        return frame
    
    def create_status_bar(self, layout):
        """创建状态栏"""
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        status_frame.setFixedHeight(120)
        
        status_layout = QVBoxLayout(status_frame)
        status_layout.setSpacing(5)
        
        # 状态标签
        self.status_label = QLabel("🟢 就绪 - 请选择要执行的功能")
        self.status_label.setFont(QFont("Microsoft YaHei", 12))
        self.status_label.setStyleSheet("color: #FF69B4;")
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFont(QFont("Microsoft YaHei", 12))
        self.progress_bar.setFixedHeight(20)  # 设置固定高度
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 3px solid #FFB6C1;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
                font-size: 12pt;
                font-family: 'Microsoft YaHei';
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #FF69B4;
                border-radius: 3px;
            }
        """)
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        
        layout.addWidget(status_frame)
        
        # 日志输出区域
        self.log_output = ModernTextEdit()
        self.log_output.setMaximumHeight(150)
        self.log_output.setPlaceholderText("操作日志将在这里显示...")
        layout.addWidget(self.log_output)
    
    def update_status(self, message, color="#FF69B4"):
        """更新状态信息 - 使用信号-槽机制安全地从任何线程调用"""
        # 通过信号发送更新请求到主线程
        self.status_updated.emit(message, color)
    
    def update_status_impl(self, message, color="#FF69B4"):
        """实际执行的状态更新 - 在主线程中执行"""
        self.status_label.setText(message)
        # 保持字体设置，只更新颜色
        self.status_label.setStyleSheet(f"color: {color}; font-size: 12pt; font-family: 'Microsoft YaHei';")
        
        # 添加到日志
        self.log_output.append(f"[{time.strftime('%H:%M:%S')}] {message}")
        
        # 强制刷新GUI界面，防止白屏
        QApplication.processEvents()
    
    def show_progress(self, show=True):
        """显示/隐藏进度条"""
        self.progress_bar.setVisible(show)
        if show:
            self.progress_bar.setRange(0, 0)  # 无限进度条
    
    def launch_wechat(self):
        """启动微信 - 集成测试脚本中验证有效的启动逻辑"""
        self.update_status("🚀 正在启动微信...", "#FF69B4")
        self.show_progress(True)
        self.launch_btn.setEnabled(False)
        
        def launch_worker():
            try:
                # 使用测试脚本中验证有效的启动逻辑
                self.update_status("🔍 检查微信安装路径...", "#FF69B4")
                
                # 使用智能路径查找
                if wechat_launcher:
                    wechat_path = wechat_launcher.find_wechat_path()
                    if not wechat_path:
                        self.update_status("❌ 未找到微信安装路径，请手动安装微信", "#f44336")
                        return
                else:
                    self.update_status("❌ 微信启动器不可用，无法查找微信路径", "#f44336")
                    return
                
                # 1. 检查文件是否存在
                if not os.path.exists(wechat_path):
                    self.update_status("❌ 微信文件不存在，请检查安装路径", "#f44336")
                    return
                
                self.update_status("✅ 微信文件存在，检查权限...", "#FF69B4")
                
                # 2. 检查文件权限
                if not os.access(wechat_path, os.X_OK):
                    self.update_status("⚠️ 微信文件可能没有执行权限", "#FF69B4")
                
                # 3. 使用与测试脚本相同的直接启动方法
                self.update_status("🚀 直接启动微信进程...", "#FF69B4")
                
                try:
                    # 使用测试脚本中验证成功的启动方法
                    import subprocess
                    process = subprocess.Popen([wechat_path])
                    self.update_status(f"✅ 微信进程已启动，PID: {process.pid}", "#FF69B4")
                    
                    # 简单等待微信启动 - 使用更小的时间片来保持GUI响应
                    for _ in range(20):  # 将2秒分成20个0.1秒
                        time.sleep(0.1)
                        QApplication.processEvents()  # 处理GUI事件
                    self.update_status("✅ 微信启动命令已执行", "#FF69B4")
                    result = True
                        
                except FileNotFoundError:
                    self.update_status("❌ 文件未找到，无法启动微信", "#f44336")
                    result = False
                except PermissionError:
                    self.update_status("❌ 权限不足，无法启动微信", "#f44336")
                    result = False
                except Exception as launch_error:
                    self.update_status(f"❌ 启动微信时出错: {launch_error}", "#f44336")
                    result = False
                
                if not result:
                    self.update_status("❌ 微信启动失败", "#f44336")
                    
            except Exception as e:
                self.update_status(f"❌ 启动出错: {str(e)}", "#f44336")
                self.update_status("💡 请尝试手动启动微信后再使用工具", "#FF69B4")
            finally:
                self.show_progress(False)
                self.launch_btn.setEnabled(True)
        
        # 在新线程中执行
        threading.Thread(target=launch_worker, daemon=True).start()
    

    
    def start_broadcast(self):
        """启动群发消息功能 - 支持多个联系人/群聊"""
        # 重置停止标志
        self._stop_broadcast = False
        
        target_names_input = self.name_input.text().strip()
        if not target_names_input:
            QMessageBox.warning(self, "输入错误", "请输入联系人或群聊名称！")
            return
        
        message_content = self.message_input.toPlainText().strip()
        if not message_content:
            QMessageBox.warning(self, "输入错误", "请输入要发送的消息内容！")
            return
        
        # 解析多个名称（用英文逗号分隔）
        target_names = [name.strip() for name in target_names_input.split(',') if name.strip()]
        if not target_names:
            QMessageBox.warning(self, "输入错误", "请输入有效的联系人或群聊名称！")
            return
        
        # 获取用户设置的等待时间（分钟）
        wait_minutes = self.wait_time_spinbox.value()
        wait_seconds = wait_minutes * 60  # 转换为秒
        
        # 判断发送类型
        is_contact = self.contact_radio.isChecked()
        target_type = "联系人" if is_contact else "群聊"
        
        self.update_status(f"🔍 准备向 {len(target_names)} 个{target_type}发送消息", "#FF69B4")
        self.show_progress(True)
        self.broadcast_btn.setEnabled(False)
        self.stop_broadcast_btn.setEnabled(True)
        
        def broadcast_worker():
            # 在函数开始时立即检查停止标志
            if self._stop_broadcast:
                self.update_status("⏹️ 操作已停止", "#FF69B4")
                return
                
            success_count = 0
            failed_count = 0
            failed_names = []
            
            try:
                # 首先启动微信（联系人和群聊都需要）
                self.update_status("🚀 正在启动微信...", "#FF69B4")
                
                # 使用智能路径查找
                if wechat_launcher:
                    wechat_path = wechat_launcher.find_wechat_path()
                    if not wechat_path:
                        self.update_status("❌ 未找到微信安装路径，请手动安装微信", "#f44336")
                        return
                else:
                    self.update_status("❌ 微信启动器不可用，无法查找微信路径", "#f44336")
                    return
                
                try:
                    import subprocess
                    import time
                    
                    # 使用subprocess.Popen启动微信
                    process = subprocess.Popen([wechat_path])
                    self.update_status(f"✅ 微信进程已启动 (PID: {process.pid})", "#FF69B4")
                    
                    # 等待微信窗口出现
                    self.update_status("⏳ 等待微信窗口弹出...", "#FF69B4")
                    # 使用更小的时间片来保持GUI响应
                    for _ in range(30):  # 将3秒分成30个0.1秒
                        time.sleep(0.1)
                        QApplication.processEvents()  # 处理GUI事件
                        if self._stop_broadcast:  # 检查停止标志
                            return
                    
                    self.update_status("✅ 微信窗口已弹出", "#FF69B4")
                    
                except Exception as e:
                    self.update_status(f"❌ 启动微信失败: {str(e)}", "#f44336")
                    return
                
                # 激活微信窗口
                self.update_status("🎯 正在激活微信窗口...", "#FF69B4")
                ensure_wechat_is_active()
                
                # 根据类型选择搜索功能
                if is_contact:
                    from wechat_core_engine import search_contact as real_search_function
                else:
                    from wechat_core_engine import search_group as real_search_function
                
                # 逐个处理每个联系人/群聊
                for i, target_name in enumerate(target_names, 1):
                    # 检查是否需要停止
                    if self._stop_broadcast:
                        self.update_status("⏹️ 用户停止了群发操作", "#FF69B4")
                        break
                        
                    # 只在处理多个目标时，从第二个目标开始重新激活微信窗口
                    if i > 1:
                        self.update_status(f"🎯 ({i}/{len(target_names)}) 正在重新激活微信窗口...", "#FF69B4")
                        ensure_wechat_is_active()
                    
                    self.update_status(f"🔍 ({i}/{len(target_names)}) 正在搜索{target_type}: {target_name}", "#FF69B4")
                    
                    try:
                        # 临时重定向输入，使用GUI输入的名称和消息
                        import builtins
                        original_input = builtins.input
                        input_responses = [target_name, message_content]
                        input_index = 0
                        
                        def mock_input(prompt=""):
                            nonlocal input_index
                            if input_index < len(input_responses):
                                response = input_responses[input_index]
                                input_index += 1
                                return response
                            return ""
                        
                        builtins.input = mock_input
                        
                        try:
                            # 传递search_term、message、ensure_active=False和停止检查函数
                            result = real_search_function(search_term=target_name, message=message_content, ensure_active=False, stop_flag_func=lambda: self._stop_broadcast)
                            
                            # 检查是否在操作过程中被停止
                            if self._stop_broadcast:
                                self.update_status("⏹️ 操作已停止", "#FF69B4")
                                return
                            
                            if result:
                                success_count += 1
                                self.update_status(f"✅ ({i}/{len(target_names)}) 成功发送到{target_type}: {target_name}", "#FF69B4")
                            else:
                                failed_count += 1
                                failed_names.append(target_name)
                                self.update_status(f"❌ ({i}/{len(target_names)}) 未找到{target_type}: {target_name}", "#f44336")
                        finally:
                            # 恢复原始input函数
                            builtins.input = original_input
                        
                        # 在处理下一个之前等待用户设置的时间
                        if i < len(target_names):
                            self.update_status(f"⏳ 等待 {wait_minutes} 分钟后处理下一个{target_type}...", "#FF69B4")
                            
                            # 倒计时显示 - 使用更小的时间片来保持GUI响应
                            for remaining_seconds in range(wait_seconds, 0, -1):
                                # 检查是否需要停止
                                if self._stop_broadcast:
                                    self.update_status("⏹️ 用户在等待期间停止了群发操作", "#FF69B4")
                                    return
                                    
                                remaining_minutes = remaining_seconds // 60
                                remaining_secs = remaining_seconds % 60
                                if remaining_minutes > 0:
                                    time_str = f"{remaining_minutes}分{remaining_secs:02d}秒"
                                else:
                                    time_str = f"{remaining_secs}秒"
                                
                                self.update_status(f"⏳ 倒计时: {time_str} (下一个: {target_names[i] if i < len(target_names) else '无'})", "#FF69B4")
                                
                                # 使用更小的时间片来保持GUI响应
                                for _ in range(10):  # 将1秒分成10个0.1秒
                                    time.sleep(0.1)
                                    QApplication.processEvents()  # 处理GUI事件
                                    if self._stop_broadcast:  # 在每个时间片都检查停止标志
                                        return
                            
                    except Exception as e:
                        failed_count += 1
                        failed_names.append(target_name)
                        self.update_status(f"❌ ({i}/{len(target_names)}) 处理{target_name}时出错: {str(e)}", "#f44336")
                
                # 显示最终统计结果
                self.update_status(f"📊 群发完成！成功: {success_count}, 失败: {failed_count}", "#FF69B4" if failed_count == 0 else "#FF69B4")
                if failed_names:
                    self.update_status(f"❌ 失败的{target_type}: {', '.join(failed_names)}", "#f44336")
                    
            except Exception as e:
                self.update_status(f"❌ 群发出错: {str(e)}", "#f44336")
            finally:
                self.show_progress(False)
                self.broadcast_btn.setEnabled(True)
                self.stop_broadcast_btn.setEnabled(False)
        
        threading.Thread(target=broadcast_worker, daemon=True).start()
    
    def stop_broadcast_operation(self):
        """停止群发消息操作"""
        self._stop_broadcast = True  # 设置停止标志
        self.update_status("⏹️ 正在停止操作...", "#FF69B4")
        self.show_progress(False)
        self.broadcast_btn.setEnabled(True)
        self.stop_broadcast_btn.setEnabled(False)
        self.update_status("✅ 操作已停止", "#FF69B4")
    

    
    def start_moments_function(self):
        """启动朋友圈功能 - 打开朋友圈并进行点赞"""
        # 重置停止标志
        self._stop_moments = False
        
        # 判断点赞模式
        is_specific_mode = self.specific_users_radio.isChecked()
        
        if is_specific_mode:
            # 仅给特定人点赞模式
            user_names_input = self.moments_name_input.text().strip()
            if not user_names_input:
                QMessageBox.warning(self, "输入错误", "请输入要点赞的用户名称！")
                return
            
            # 解析多个用户名（用英文逗号分隔）
            user_names = [name.strip() for name in user_names_input.split(',') if name.strip()]
            if not user_names:
                QMessageBox.warning(self, "输入错误", "请输入有效的用户名称！")
                return
            
            blacklist = []
        else:
            # 给所有人点赞模式
            user_names = []  # 不需要指定用户
            blacklist_input = self.moments_blacklist_input.text().strip()
            blacklist = [name.strip() for name in blacklist_input.split(',') if name.strip()] if blacklist_input else []
        
        # 获取用户设置的等待时间（秒）
        wait_seconds = self.moments_wait_time_spinbox.value()
        
        # 获取评论设置
        enable_comment = self.enable_comment_checkbox.isChecked()
        comment_text = self.comment_text_input.text().strip() if enable_comment else ""
        
        # 获取点赞类型设置
        like_text = self.like_text_checkbox.isChecked()
        like_image = self.like_image_checkbox.isChecked()
        like_video = self.like_video_checkbox.isChecked()
        
        # 验证至少选择一种类型
        if not (like_text or like_image or like_video):
            QMessageBox.warning(self, "设置错误", "请至少选择一种点赞类型（文字/图片/视频）！")
            return
        
        # 获取窗口调整设置（从设置页面获取）
        enable_window_resize = self.enable_window_resize_checkbox.isChecked()
        
        # 验证评论设置
        if enable_comment and not comment_text:
            QMessageBox.warning(self, "设置错误", "已启用评论功能但未输入评论内容！")
            return
        
        # 显示启动信息
        if is_specific_mode:
            status_msg = f"🚀 启动朋友圈功能，准备为 {len(user_names)} 个用户点赞"
        else:
            status_msg = f"🚀 启动朋友圈功能，给所有人点赞"
            if blacklist:
                status_msg += f"（黑名单: {len(blacklist)} 人）"
        
        if enable_comment:
            status_msg += " + 评论"
        
        self.update_status(status_msg, "#FF69B4")
        self.show_progress(True)
        self.start_moments_btn.setEnabled(False)
        self.stop_moments_btn.setEnabled(True)
        
        def moments_worker():
            # 在函数开始时立即检查停止标志
            if self._stop_moments:
                self.update_status("⏹️ 操作已停止", "#FF69B4")
                return
                
            success_count = 0
            failed_count = 0
            failed_names = []
            
            try:
                # 朋友圈已由用户手动打开，直接开始点赞操作
                self.update_status("✅ 朋友圈已打开，准备开始点赞", "#FF69B4")
                self.update_status("👍 开始点赞操作", "#FF69B4")
                import time
                
                # 进行点赞操作 - 使用已导入的pengyouquan_multi_dianzan_action函数
                
                if is_specific_mode:
                    # 仅给特定人点赞
                    self.update_status(f"👍 开始同时搜索并点赞 {len(user_names)} 个用户: {', '.join(user_names)}", "#FF69B4")
                    
                    try:
                        # 定义状态回调函数
                        def status_update_callback(message):
                            self.update_status(message, "#FF69B4")
                        
                        # 调用多用户并发点赞功能，传递等待时间参数、回调函数、评论参数、点赞类型和停止检查函数
                        results = pengyouquan_multi_dianzan_action(
                            user_names, 
                            wait_seconds, 
                            status_update_callback, 
                            enable_comment, 
                            comment_text, 
                            stop_flag_func=lambda: self._stop_moments,
                            like_text=like_text,
                            like_image=like_image,
                            like_video=like_video
                        )
                        
                        # 检查是否在操作过程中被停止
                        if self._stop_moments:
                            self.update_status("⏹️ 操作已停止", "#FF69B4")
                            return
                        
                        # 处理结果
                        if results and isinstance(results, dict):
                             success_count = results.get('success_count', 0)
                             failed_count = results.get('failed_count', 0)
                             failed_names = results.get('failed_names', [])
                             found_users = results.get('found_users', [])
                             not_found_users = results.get('not_found_users', [])
                             
                             # 显示成功的用户
                             for user_name in found_users:
                                 self.update_status(f"✅ 成功给 {user_name} 点赞", "#FF69B4")
                             
                             # 显示失败的用户
                             for user_name in failed_names:
                                 self.update_status(f"❌ 未找到用户或点赞失败: {user_name}", "#f44336")
                        else:
                            # 如果多用户功能失败，回退到单用户模式
                            self.update_status("⚠️ 多用户模式失败，回退到单用户模式", "#FF69B4")
                            # 使用已导入的pengyouquan_dianzan_action函数
                            
                            # 逐个处理每个用户
                            for i, user_name in enumerate(user_names, 1):
                                # 检查是否需要停止
                                if self._stop_moments:
                                    self.update_status("⏹️ 用户停止了朋友圈操作", "#FF69B4")
                                    break
                                    
                                self.update_status(f"👍 ({i}/{len(user_names)}) 正在查找并点赞: {user_name}", "#FF69B4")
                                
                                try:
                                    result = pengyouquan_dianzan_action(
                                        user_name, 
                                        enable_comment, 
                                        comment_text, 
                                        stop_flag_func=lambda: self._stop_moments,
                                        like_text=like_text,
                                        like_image=like_image,
                                        like_video=like_video
                                    )
                                    
                                    # 检查是否在操作过程中被停止
                                    if self._stop_moments:
                                        self.update_status("⏹️ 操作已停止", "#FF69B4")
                                        return
                                    
                                    if result:
                                        success_count += 1
                                        self.update_status(f"✅ ({i}/{len(user_names)}) 成功给 {user_name} 点赞", "#FF69B4")
                                    else:
                                        failed_count += 1
                                        failed_names.append(user_name)
                                        self.update_status(f"❌ ({i}/{len(user_names)}) 未找到用户或点赞失败: {user_name}", "#f44336")
                                    
                                    # 在处理下一个用户之前等待用户设置的时间
                                    if i < len(user_names):
                                        wait_minutes = wait_seconds // 60
                                        wait_secs = wait_seconds % 60
                                        if wait_minutes > 0:
                                            wait_str = f"{wait_minutes}分{wait_secs}秒"
                                        else:
                                            wait_str = f"{wait_secs}秒"
                                        self.update_status(f"⏳ 等待 {wait_str} 后点赞下一个用户...", "#FF69B4")
                                        
                                        # 倒计时显示 - 使用更小的时间片来保持GUI响应
                                        for remaining_seconds in range(wait_seconds, 0, -1):
                                            # 检查是否需要停止
                                            if self._stop_moments:
                                                self.update_status("⏹️ 用户在等待期间停止了朋友圈操作", "#FF69B4")
                                                return
                                                
                                            remaining_minutes = remaining_seconds // 60
                                            remaining_secs = remaining_seconds % 60
                                            if remaining_minutes > 0:
                                                time_str = f"{remaining_minutes}分{remaining_secs:02d}秒"
                                            else:
                                                time_str = f"{remaining_secs}秒"
                                            
                                            self.update_status(f"⏳ 倒计时: {time_str} (下一个: {user_names[i] if i < len(user_names) else '无'})", "#FF69B4")
                                            
                                            # 使用更小的时间片来保持GUI响应
                                            for _ in range(10):  # 将1秒分成10个0.1秒
                                                time.sleep(0.1)
                                                QApplication.processEvents()  # 处理GUI事件
                                                if self._stop_moments:  # 在每个时间片都检查停止标志
                                                    return
                                    
                                except Exception as e:
                                    failed_count += 1
                                    failed_names.append(user_name)
                                    self.update_status(f"❌ ({i}/{len(user_names)}) 处理{user_name}时出错: {str(e)}", "#f44336")
                        
                    except Exception as e:
                        failed_count = len(user_names)
                        failed_names = user_names.copy()
                        self.update_status(f"❌ 多用户点赞功能出错: {str(e)}", "#f44336")
                else:
                    # 给所有人点赞（现在已实现！）
                    self.update_status("🌟 开始给所有人点赞功能...", "#FF69B4")
                    
                    try:
                        # 定义状态回调函数
                        def status_update_callback(message):
                            self.update_status(message, "#FF69B4")
                        
                        # 调用优化的给所有人点赞功能
                        results = pengyouquan_like_all_action(
                            status_callback=status_update_callback,
                            stop_flag_func=lambda: self._stop_moments,
                            max_posts=100,  # 最多点赞100个posts
                            max_retries_per_post=2
                        )
                        
                        # 检查是否在操作过程中被停止
                        if self._stop_moments:
                            self.update_status("⏹️ 操作已停止", "#FF69B4")
                            return
                        
                        # 处理结果
                        if results and isinstance(results, dict):
                            success_count = results.get('success', 0)
                            failed_count = results.get('failed', 0)
                            skipped_count = results.get('skipped', 0)
                            
                            # 显示统计结果
                            self.update_status(f"📊 给所有人点赞完成!", "#FF69B4")
                            self.update_status(f"✅ 成功点赞: {success_count} 个", "#FF69B4")
                            self.update_status(f"❌ 失败: {failed_count} 个", "#f44336")
                            if skipped_count > 0:
                                self.update_status(f"⏭️ 跳过: {skipped_count} 个", "#FF69B4")
                        else:
                            self.update_status("⚠️ 给所有人点赞功能返回异常结果", "#FF69B4")
                    
                    except Exception as e:
                        self.update_status(f"❌ 给所有人点赞功能出错: {str(e)}", "#f44336")
                
                # 显示最终统计结果
                self.update_status(f"📊 朋友圈功能完成！成功: {success_count}, 失败: {failed_count}", "#FF69B4" if failed_count == 0 else "#FF69B4")
                if failed_names:
                    self.update_status(f"❌ 失败的用户: {', '.join(failed_names)}", "#f44336")
                    
            except Exception as e:
                self.update_status(f"❌ 朋友圈功能出错: {str(e)}", "#f44336")
            finally:
                self.show_progress(False)
                self.start_moments_btn.setEnabled(True)
                self.stop_moments_btn.setEnabled(False)
        
        threading.Thread(target=moments_worker, daemon=True).start()
    
    def stop_moments_operation(self):
        """停止朋友圈操作"""
        self._stop_moments = True  # 设置停止标志
        self.update_status("⏹️ 正在停止朋友圈操作...", "#FF69B4")
        self.show_progress(False)
        self.start_moments_btn.setEnabled(True)
        self.stop_moments_btn.setEnabled(False)
        self.update_status("✅ 朋友圈操作已停止", "#FF69B4")
    
    def connect_auto_save_signals_except_radio(self):
        """连接除单选按钮外的所有输入框的实时保存信号"""
        try:
            # 连接文本输入框的变化信号
            if hasattr(self, 'message_input'):
                self.message_input.textChanged.connect(self.save_last_inputs)
            
            # 名称输入框不连接自动保存，改为失去焦点时保存
            if hasattr(self, 'name_input'):
                self.name_input.editingFinished.connect(self.save_name_input)
            
            if hasattr(self, 'moments_name_input'):
                self.moments_name_input.textChanged.connect(self.save_last_inputs)
            
            if hasattr(self, 'moments_blacklist_input'):
                self.moments_blacklist_input.textChanged.connect(self.save_last_inputs)
            
            if hasattr(self, 'comment_text_input'):
                self.comment_text_input.textChanged.connect(self.save_last_inputs)
            
            # 连接数值输入框的变化信号
            if hasattr(self, 'moments_wait_time_spinbox'):
                self.moments_wait_time_spinbox.valueChanged.connect(self.save_last_inputs)
            
            # 连接单选按钮的变化信号（点赞模式）
            if hasattr(self, 'specific_users_radio'):
                self.specific_users_radio.toggled.connect(self.save_last_inputs)
            
            # 连接复选框的变化信号
            if hasattr(self, 'enable_comment_checkbox'):
                self.enable_comment_checkbox.stateChanged.connect(self.save_last_inputs)
            
            if hasattr(self, 'like_text_checkbox'):
                self.like_text_checkbox.stateChanged.connect(self.save_last_inputs)
            
            if hasattr(self, 'like_image_checkbox'):
                self.like_image_checkbox.stateChanged.connect(self.save_last_inputs)
            
            if hasattr(self, 'like_video_checkbox'):
                self.like_video_checkbox.stateChanged.connect(self.save_last_inputs)
            
            if hasattr(self, 'enable_window_resize_checkbox'):
                self.enable_window_resize_checkbox.stateChanged.connect(self.save_last_inputs)

            if hasattr(self, 'aux_like_enable_checkbox'):
                self.aux_like_enable_checkbox.stateChanged.connect(self.save_last_inputs)

            if hasattr(self, 'aux_like_offset_x_spinbox'):
                self.aux_like_offset_x_spinbox.valueChanged.connect(self.save_last_inputs)

            if hasattr(self, 'aux_like_offset_y_spinbox'):
                self.aux_like_offset_y_spinbox.valueChanged.connect(self.save_last_inputs)

            if hasattr(self, 'aux_like_delay_spinbox'):
                self.aux_like_delay_spinbox.valueChanged.connect(self.save_last_inputs)

            if hasattr(self, 'aux_like_scroll_lines_spinbox'):
                self.aux_like_scroll_lines_spinbox.valueChanged.connect(self.save_last_inputs)
            
            if hasattr(self, 'aux_like_scroll_delay_spinbox'):
                self.aux_like_scroll_delay_spinbox.valueChanged.connect(self.save_last_inputs)
                
        except Exception as e:
            print(f"连接自动保存信号失败: {e}")
    
    def connect_radio_signals(self):
        """连接单选按钮的信号（在加载完成后调用）"""
        try:
            # 只连接类型切换信号，不连接自动保存信号
            if hasattr(self, 'contact_radio'):
                self.contact_radio.toggled.connect(self.on_type_changed)
            
            if hasattr(self, 'group_radio'):
                self.group_radio.toggled.connect(self.on_type_changed)
                
        except Exception as e:
            print(f"连接单选按钮信号失败: {e}")
    
    def save_last_inputs(self):
        """实时保存输入内容到配置文件"""
        try:
            # 如果正在切换类型，不保存输入框内容
            if hasattr(self, '_switching_type') and self._switching_type:
                return
                
            import json
            import os
            
            # 读取现有配置
            config_file = "wechat_config.json"
            config = {}
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            # 确保last_inputs存在，但不清空现有数据
            if 'last_inputs' not in config:
                config['last_inputs'] = {}
            
            if hasattr(self, 'message_input'):
                config['last_inputs']['message_content'] = self.message_input.toPlainText()
            
            # 分别保存联系人和群聊名称
            if hasattr(self, 'name_input') and hasattr(self, 'contact_radio'):
                current_names = self.name_input.text()
                
                # 初始化字段（如果不存在）
                if 'contact_names' not in config['last_inputs']:
                    config['last_inputs']['contact_names'] = ""
                if 'group_names' not in config['last_inputs']:
                    config['last_inputs']['group_names'] = ""
                
                # 根据当前选择的模式保存到对应字段
                if self.contact_radio.isChecked():
                    #print(f"💾 保存联系人名称: '{current_names}' (联系人模式选中)")
                    config['last_inputs']['contact_names'] = current_names
                else:
                    #print(f"💾 保存群聊名称: '{current_names}' (群聊模式选中)")
                    config['last_inputs']['group_names'] = current_names
                    
                # 调试信息：显示保存后的配置
                #print(f"📋 保存后配置: contact_names='{config['last_inputs'].get('contact_names', '')}', group_names='{config['last_inputs'].get('group_names', '')}'")
            
            if hasattr(self, 'contact_radio'):
                config['last_inputs']['is_contact'] = self.contact_radio.isChecked()
            
            if hasattr(self, 'moments_name_input'):
                config['last_inputs']['moments_names'] = self.moments_name_input.text()
            
            if hasattr(self, 'moments_blacklist_input'):
                config['last_inputs']['moments_blacklist'] = self.moments_blacklist_input.text()
            
            if hasattr(self, 'moments_wait_time_spinbox'):
                config['last_inputs']['wait_seconds'] = self.moments_wait_time_spinbox.value()
            
            if hasattr(self, 'specific_users_radio'):
                config['last_inputs']['specific_users_mode'] = self.specific_users_radio.isChecked()
            
            if hasattr(self, 'enable_comment_checkbox'):
                config['last_inputs']['enable_comment'] = self.enable_comment_checkbox.isChecked()
            
            if hasattr(self, 'comment_text_input'):
                config['last_inputs']['comment_text'] = self.comment_text_input.text()
            
            # 保存点赞类型选择
            if hasattr(self, 'like_text_checkbox'):
                config['last_inputs']['like_text'] = self.like_text_checkbox.isChecked()
            
            if hasattr(self, 'like_image_checkbox'):
                config['last_inputs']['like_image'] = self.like_image_checkbox.isChecked()
            
            if hasattr(self, 'like_video_checkbox'):
                config['last_inputs']['like_video'] = self.like_video_checkbox.isChecked()
            
            # 保存窗口大小调整选项
            if hasattr(self, 'enable_window_resize_checkbox'):
                config['last_inputs']['enable_window_resize'] = self.enable_window_resize_checkbox.isChecked()

            # 保存辅助点赞设置
            if hasattr(self, 'aux_like_enable_checkbox'):
                config['last_inputs']['aux_like_hotkey_enabled'] = self.aux_like_enable_checkbox.isChecked()

            if hasattr(self, 'aux_like_offset_x_spinbox'):
                config['last_inputs']['aux_like_offset_x'] = self.aux_like_offset_x_spinbox.value()

            if hasattr(self, 'aux_like_offset_y_spinbox'):
                config['last_inputs']['aux_like_offset_y'] = self.aux_like_offset_y_spinbox.value()

            if hasattr(self, 'aux_like_delay_spinbox'):
                config['last_inputs']['aux_like_delay_ms'] = self.aux_like_delay_spinbox.value()

            if hasattr(self, 'aux_like_scroll_lines_spinbox'):
                config['last_inputs']['aux_like_scroll_lines'] = self.aux_like_scroll_lines_spinbox.value()
            
            if hasattr(self, 'aux_like_scroll_delay_spinbox'):
                config['last_inputs']['aux_like_scroll_delay'] = self.aux_like_scroll_delay_spinbox.value()
            
            # 写入配置文件
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            # 静默处理错误，避免频繁的错误提示
            pass
    
    def save_name_input(self):
        """专门保存名称输入框的内容"""
        try:
            # 如果正在切换类型，不保存输入框内容
            if hasattr(self, '_switching_type') and self._switching_type:
                print("🚫 正在切换类型，跳过名称保存")
                return
                
            import json
            import os
            
            # 读取现有配置
            config_file = "wechat_config.json"
            config = {}
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            # 确保last_inputs存在
            if 'last_inputs' not in config:
                config['last_inputs'] = {}
            
            # 分别保存联系人和群聊名称
            if hasattr(self, 'name_input') and hasattr(self, 'contact_radio'):
                current_names = self.name_input.text().strip()
                
                # 如果输入为空，跳过保存
                if not current_names:
                    print("🚫 输入框为空，跳过名称保存")
                    return
                
                # 初始化字段（如果不存在）
                if 'contact_names' not in config['last_inputs']:
                    config['last_inputs']['contact_names'] = ""
                if 'group_names' not in config['last_inputs']:
                    config['last_inputs']['group_names'] = ""
                
                # 根据当前选择的模式保存到对应字段
                if self.contact_radio.isChecked():
                    print(f"💾 [焦点保存] 保存联系人名称: '{current_names}' (联系人模式选中)")
                    config['last_inputs']['contact_names'] = current_names
                else:
                    print(f"💾 [焦点保存] 保存群聊名称: '{current_names}' (群聊模式选中)")
                    config['last_inputs']['group_names'] = current_names
                    
                # 调试信息：显示保存后的配置
                #print(f"📋 [焦点保存] 保存后配置: contact_names='{config['last_inputs'].get('contact_names', '')}', group_names='{config['last_inputs'].get('group_names', '')}'")
            
            # 写入配置文件
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"❌ 保存名称输入时发生错误: {e}")
    
    def save_radio_state(self):
        """专门保存单选按钮的状态"""
        try:
            import json
            import os
            
            # 读取现有配置
            config_file = "wechat_config.json"
            config = {}
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            # 确保last_inputs存在
            if 'last_inputs' not in config:
                config['last_inputs'] = {}
            
            # 保存单选按钮状态
            if hasattr(self, 'contact_radio'):
                is_contact = self.contact_radio.isChecked()
                config['last_inputs']['is_contact'] = is_contact
                #print(f"💾 [切换保存] 保存单选按钮状态: is_contact={is_contact}")
            
            # 写入配置文件
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"❌ 保存单选按钮状态时发生错误: {e}")
     
    def load_last_inputs(self):
        """从配置文件加载最后一次的输入内容"""
        try:
            import json
            import os
            
            config_file = "wechat_config.json"
            if not os.path.exists(config_file):
                return
            
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            last_inputs = config.get('last_inputs', {})
            if not last_inputs:
                return
            
            # 恢复群发消息的输入
            if hasattr(self, 'message_input') and last_inputs.get('message_content'):
                self.message_input.setPlainText(last_inputs['message_content'])
            
            # 恢复单选按钮状态（临时设置标志避免触发保存）
            if hasattr(self, 'contact_radio') and hasattr(self, 'group_radio'):
                self._switching_type = True  # 设置标志避免触发保存
                
                is_contact = last_inputs.get('is_contact', True)
                self.contact_radio.setChecked(is_contact)
                self.group_radio.setChecked(not is_contact)
                
                # 根据选择的类型加载对应的名称
                if hasattr(self, 'name_input'):
                    if is_contact and last_inputs.get('contact_names'):
                        self.name_input.setText(last_inputs['contact_names'])
                    elif not is_contact and last_inputs.get('group_names'):
                        self.name_input.setText(last_inputs['group_names'])
                    else:
                        # 如果没有对应的名称数据，清空输入框
                        self.name_input.setText('')
                
                self._switching_type = False  # 清除标志
            
            # 恢复朋友圈的输入
            if hasattr(self, 'moments_name_input') and last_inputs.get('moments_names'):
                self.moments_name_input.setText(last_inputs['moments_names'])
            
            if hasattr(self, 'moments_blacklist_input') and last_inputs.get('moments_blacklist'):
                self.moments_blacklist_input.setText(last_inputs['moments_blacklist'])
            
            if hasattr(self, 'moments_wait_time_spinbox'):
                # 先尝试加载新的秒数配置，如果没有则转换旧的分钟配置
                if 'wait_seconds' in last_inputs:
                    self.moments_wait_time_spinbox.setValue(last_inputs['wait_seconds'])
                elif 'wait_minutes' in last_inputs:
                    # 将旧的分钟数转换为秒数
                    self.moments_wait_time_spinbox.setValue(last_inputs['wait_minutes'] * 60)
            
            # 恢复点赞模式选择
            if hasattr(self, 'specific_users_radio') and hasattr(self, 'all_users_radio'):
                specific_mode = last_inputs.get('specific_users_mode', True)
                self.specific_users_radio.setChecked(specific_mode)
                self.all_users_radio.setChecked(not specific_mode)
                # 触发模式切换处理
                self.on_like_mode_changed()
            
            if hasattr(self, 'enable_comment_checkbox') and 'enable_comment' in last_inputs:
                self.enable_comment_checkbox.setChecked(last_inputs['enable_comment'])
            
            if hasattr(self, 'comment_text_input') and last_inputs.get('comment_text'):
                self.comment_text_input.setText(last_inputs['comment_text'])
            
            # 恢复点赞类型选择
            if hasattr(self, 'like_text_checkbox'):
                self.like_text_checkbox.setChecked(last_inputs.get('like_text', True))
            
            if hasattr(self, 'like_image_checkbox'):
                self.like_image_checkbox.setChecked(last_inputs.get('like_image', True))
            
            if hasattr(self, 'like_video_checkbox'):
                self.like_video_checkbox.setChecked(last_inputs.get('like_video', True))
            
            # 恢复窗口大小调整选项
            if hasattr(self, 'enable_window_resize_checkbox') and 'enable_window_resize' in last_inputs:
                self.enable_window_resize_checkbox.setChecked(last_inputs['enable_window_resize'])

            # 恢复辅助点赞设置
            if hasattr(self, 'aux_like_offset_x_spinbox') and 'aux_like_offset_x' in last_inputs:
                self.aux_like_offset_x_spinbox.setValue(last_inputs['aux_like_offset_x'])

            if hasattr(self, 'aux_like_offset_y_spinbox') and 'aux_like_offset_y' in last_inputs:
                self.aux_like_offset_y_spinbox.setValue(last_inputs['aux_like_offset_y'])

            if hasattr(self, 'aux_like_delay_spinbox') and 'aux_like_delay_ms' in last_inputs:
                self.aux_like_delay_spinbox.setValue(last_inputs['aux_like_delay_ms'])

            if hasattr(self, 'aux_like_scroll_lines_spinbox') and 'aux_like_scroll_lines' in last_inputs:
                self.aux_like_scroll_lines_spinbox.setValue(last_inputs['aux_like_scroll_lines'])
            
            if hasattr(self, 'aux_like_scroll_delay_spinbox') and 'aux_like_scroll_delay' in last_inputs:
                self.aux_like_scroll_delay_spinbox.setValue(last_inputs['aux_like_scroll_delay'])

            if hasattr(self, 'aux_like_enable_checkbox'):
                enabled = last_inputs.get('aux_like_hotkey_enabled', False)
                self.aux_like_enable_checkbox.setChecked(enabled)
                # load阶段信号可能尚未连接，主动同步一次热键状态
                self.on_aux_like_hotkey_changed(2 if enabled else 0)
                
        except Exception as e:
            print(f"加载输入内容失败: {e}")
    
    def on_type_changed(self):
        """当联系人/群聊类型切换时，自动加载对应的名称"""
        try:
            import json
            import os
            
            config_file = "wechat_config.json"
            if not os.path.exists(config_file):
                print("⚠️ 配置文件不存在")
                return
            
            # 读取配置文件
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            last_inputs = config.get('last_inputs', {})
            if not last_inputs or not hasattr(self, 'name_input'):
                print("⚠️ 配置数据为空或输入框不存在")
                return
            
            # 设置标志，避免在切换时触发保存
            self._switching_type = True
            
            try:
                # 根据当前选择的类型加载对应的名称
                if hasattr(self, 'contact_radio') and self.contact_radio.isChecked():
                    # 切换到联系人，加载联系人名称
                    contact_names = last_inputs.get('contact_names', '')
                    #print(f"🔄 切换到联系人模式，加载名称: '{contact_names}'")
                    self.name_input.setText(contact_names)
                elif hasattr(self, 'group_radio') and self.group_radio.isChecked():
                    # 切换到群聊，加载群聊名称
                    group_names = last_inputs.get('group_names', '')
                    #print(f"🔄 切换到群聊模式，加载名称: '{group_names}'")
                    self.name_input.setText(group_names)
            finally:
                # 使用 QTimer 延迟清除标志，确保所有信号处理完成
                def clear_flag_and_save():
                    self._switching_type = False
                    # 切换完成后，保存单选按钮状态
                    self.save_radio_state()
                QTimer.singleShot(100, clear_flag_and_save)
                
        except Exception as e:
            print(f"❌ 类型切换时发生错误: {e}")
            self._switching_type = False

    def on_aux_like_hotkey_changed(self, state):
        """启用/禁用F10辅助点赞热键"""
        enabled = (state == 2)

        if enabled:
            keyboard_ok = False
            pynput_ok = False

            # 先尝试 keyboard 库
            try:
                if KEYBOARD_HOTKEY_AVAILABLE:
                    if self._aux_like_hotkey_registered and self._aux_like_hotkey_id is not None:
                        keyboard_hotkey.remove_hotkey(self._aux_like_hotkey_id)

                    self._aux_like_hotkey_id = keyboard_hotkey.add_hotkey(
                        'f10',
                        lambda: self.aux_like_triggered.emit(True),
                        suppress=False,
                        trigger_on_release=True
                    )
                    self._aux_like_hotkey_registered = True
                    keyboard_ok = True
            except Exception as e:
                self._aux_like_hotkey_registered = False
                self._aux_like_hotkey_id = None
                self.update_status(f"⚠️ keyboard热键注册失败: {e}", "#FF69B4")

            # 再尝试 pynput 备用监听
            try:
                if PYNPUT_HOTKEY_AVAILABLE:
                    if self._aux_like_pynput_listener:
                        try:
                            self._aux_like_pynput_listener.stop()
                        except Exception:
                            pass
                        self._aux_like_pynput_listener = None

                    def _on_press(key):
                        try:
                            if key == pynput_keyboard.Key.f10:
                                self.aux_like_triggered.emit(True)
                        except Exception:
                            pass

                    self._aux_like_pynput_listener = pynput_keyboard.Listener(on_press=_on_press)
                    self._aux_like_pynput_listener.daemon = True
                    self._aux_like_pynput_listener.start()
                    self._aux_like_pynput_registered = True
                    pynput_ok = True
            except Exception as e:
                self._aux_like_pynput_listener = None
                self._aux_like_pynput_registered = False
                self.update_status(f"⚠️ pynput热键注册失败: {e}", "#FF69B4")

            if keyboard_ok or pynput_ok:
                engines = []
                if keyboard_ok:
                    engines.append("keyboard")
                if pynput_ok:
                    engines.append("pynput")
                self.update_status(f"✅ 已启用辅助点赞热键：F10（引擎: {', '.join(engines)}）", "#FF69B4")
            else:
                self.update_status("❌ 启用F10热键失败：全局监听不可用", "#f44336")
                self.aux_like_enable_checkbox.blockSignals(True)
                self.aux_like_enable_checkbox.setChecked(False)
                self.aux_like_enable_checkbox.blockSignals(False)
        else:
            try:
                if self._aux_like_hotkey_registered and self._aux_like_hotkey_id is not None:
                    keyboard_hotkey.remove_hotkey(self._aux_like_hotkey_id)
                self._aux_like_hotkey_registered = False
                self._aux_like_hotkey_id = None

                if self._aux_like_pynput_listener is not None:
                    try:
                        self._aux_like_pynput_listener.stop()
                    except Exception:
                        pass
                self._aux_like_pynput_listener = None
                self._aux_like_pynput_registered = False

                self.update_status("⏹️ 已关闭辅助点赞热键", "#FF69B4")
            except Exception as e:
                self.update_status(f"⚠️ 关闭F10热键时出现问题: {e}", "#FF69B4")

    def execute_aux_like_once(self, from_hotkey=False):
        """执行一次辅助点赞动作：当前点 + 偏移点 + 可选向下滚动"""
        if from_hotkey and hasattr(self, 'aux_like_enable_checkbox') and not self.aux_like_enable_checkbox.isChecked():
            return

        with self._aux_like_lock:
            now = time.time()
            if now - self._aux_like_last_trigger_time < 0.25:
                return
            self._aux_like_last_trigger_time = now

        original_pause = pyautogui.PAUSE
        original_min_duration = getattr(pyautogui, 'MINIMUM_DURATION', 0.0)
        original_min_sleep = getattr(pyautogui, 'MINIMUM_SLEEP', 0.0)

        try:
            offset_x = self.aux_like_offset_x_spinbox.value()
            offset_y = self.aux_like_offset_y_spinbox.value()
            delay_ms = self.aux_like_delay_spinbox.value()
            scroll_lines = self.aux_like_scroll_lines_spinbox.value() if hasattr(self, 'aux_like_scroll_lines_spinbox') else 0
            scroll_delay_ms = self.aux_like_scroll_delay_spinbox.value() if hasattr(self, 'aux_like_scroll_delay_spinbox') else 0

            # 临时关闭PyAutoGUI全局延时，确保0ms场景也能极快执行
            pyautogui.PAUSE = 0
            pyautogui.MINIMUM_DURATION = 0
            pyautogui.MINIMUM_SLEEP = 0

            current_pos = pyautogui.position()
            target_x = current_pos.x + offset_x
            target_y = current_pos.y + offset_y

            trigger_source = "F10" if from_hotkey else "测试按钮"
            self.update_status(
                f"🖱️ 辅助点赞({trigger_source})：先点({current_pos.x},{current_pos.y})，再双击({target_x},{target_y})，下滚{scroll_lines}行({scroll_delay_ms}ms延时)",
                "#FF69B4"
            )

            pyautogui.click(current_pos.x, current_pos.y)
            if delay_ms > 0:
                time.sleep(delay_ms / 1000.0)
            pyautogui.doubleClick(target_x, target_y)

            # 执行完成后将鼠标移回原始位置，避免影响后续操作
            pyautogui.moveTo(current_pos.x, current_pos.y, duration=0)

            # 下滚前的延时
            if scroll_delay_ms > 0 and scroll_lines > 0:
                time.sleep(scroll_delay_ms / 1000.0)
            
            # 完成全部动作后，按设置向下滚动指定行数
            if scroll_lines > 0:
                pyautogui.scroll(-int(scroll_lines))

        except Exception as e:
            self.update_status(f"❌ 辅助点赞执行失败: {e}", "#f44336")
        finally:
            pyautogui.PAUSE = original_pause
            pyautogui.MINIMUM_DURATION = original_min_duration
            pyautogui.MINIMUM_SLEEP = original_min_sleep

    def closeEvent(self, event):
        """窗口关闭时清理全局热键"""
        try:
            if self._aux_like_hotkey_registered and self._aux_like_hotkey_id is not None and KEYBOARD_HOTKEY_AVAILABLE:
                keyboard_hotkey.remove_hotkey(self._aux_like_hotkey_id)
                self._aux_like_hotkey_registered = False
                self._aux_like_hotkey_id = None

            if self._aux_like_pynput_listener is not None:
                try:
                    self._aux_like_pynput_listener.stop()
                except Exception:
                    pass
            self._aux_like_pynput_listener = None
            self._aux_like_pynput_registered = False
        except Exception:
            pass

        super().closeEvent(event)
    
def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setApplicationName("WeChat自动化工具")
    app.setApplicationVersion("2.1")
    app.setOrganizationName("WeChatAutomation")
    
    # 设置全局字体
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)
    
    # 初始化OCR引擎
    print("🔧 正在初始化GUI环境的OCR引擎...")
    _init_gui_ocr_engines()
    
    # 创建主窗口
    window = WeChatAutomationGUI()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
