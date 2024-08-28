import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu, QAction, QVBoxLayout,
                             QWidget, QLineEdit, QLabel, QPushButton, QMessageBox, QComboBox, QCheckBox, QTextEdit, QHBoxLayout)
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

class ConfigSwitcherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config_file_path = "server.properties"  # 假设配置文件路径
        self.server_name = self.read_server_name()
        self.gamemode = self.read_gamemode()
        self.force_gamemode = self.read_force_gamemode()
        self.difficulty = self.read_difficulty()
        self.allow_cheats = self.read_allow_cheats()

        self.init_ui()
        self.init_menu()

    def init_ui(self):
        self.setWindowTitle(self.tr("基岩版服务端存档切换器"))

        # 设置窗口初始大小
        self.resize(800, 600)

        layout = QVBoxLayout()

        # Server Name
        server_name_layout = QHBoxLayout()
        server_name_label = QLabel(self.tr("服务器名称"), self)
        server_name_layout.addWidget(server_name_label)

        self.server_name_edit = QLineEdit(self)
        self.server_name_edit.setText(self.server_name)
        server_name_layout.addWidget(self.server_name_edit)

        save_button = QPushButton(self.tr("保存"), self)
        save_button.clicked.connect(self.save_server_name)
        server_name_layout.addWidget(save_button)

        layout.addLayout(server_name_layout)

        # Gamemode
        gamemode_layout = QHBoxLayout()
        gamemode_label = QLabel(self.tr("游戏模式"), self)
        gamemode_layout.addWidget(gamemode_label)

        self.gamemode_combo = QComboBox(self)
        self.gamemode_combo.addItems([self.tr("创造"), self.tr("生存"), self.tr("冒险")])
        self.gamemode_combo.setCurrentText(self.get_gamemode_display_name(self.gamemode))
        gamemode_layout.addWidget(self.gamemode_combo)

        save_gamemode_button = QPushButton(self.tr("保存游戏模式"), self)
        save_gamemode_button.clicked.connect(self.save_gamemode)
        gamemode_layout.addWidget(save_gamemode_button)

        layout.addLayout(gamemode_layout)

        # Difficulty
        difficulty_layout = QHBoxLayout()
        difficulty_label = QLabel(self.tr("难度"), self)
        difficulty_layout.addWidget(difficulty_label)

        self.difficulty_combo = QComboBox(self)
        self.difficulty_combo.addItems([self.tr("困难"), self.tr("普通"), self.tr("简单"), self.tr("和平")])
        self.difficulty_combo.setCurrentText(self.get_difficulty_display_name(self.difficulty))
        difficulty_layout.addWidget(self.difficulty_combo)

        save_difficulty_button = QPushButton(self.tr("保存难度"), self)
        save_difficulty_button.clicked.connect(self.save_difficulty)
        difficulty_layout.addWidget(save_difficulty_button)

        layout.addLayout(difficulty_layout)

        # Force Gamemode
        force_gamemode_layout = QHBoxLayout()
        force_gamemode_label = QLabel(self.tr("强制游戏模式"), self)
        force_gamemode_layout.addWidget(force_gamemode_label)

        self.force_gamemode_checkbox = QCheckBox(self.tr("启用"), self)
        self.force_gamemode_checkbox.setChecked(self.force_gamemode == "true")
        self.force_gamemode_checkbox.stateChanged.connect(self.save_force_gamemode)
        force_gamemode_layout.addWidget(self.force_gamemode_checkbox)

        layout.addLayout(force_gamemode_layout)

        force_gamemode_info = QTextEdit(self)
        force_gamemode_info.setReadOnly(True)
        force_gamemode_info.setHtml(self.tr(
            "<p>若关闭会防止服务器向客户端发送游戏模式值，而不是在创建世界时服务器保存的游戏模式值，即使这些值是在服务器中设置的。创建世界之后的属性。</p>"
            "<p>若开启强制服务器向客户端发送游戏模式值，而不是服务器在创建世界时保存的游戏模式值，如果这些值是服务器设置的。创建世界之后的属性。</p>"
        ))
        layout.addWidget(force_gamemode_info)

        # Allow Cheats
        allow_cheats_layout = QHBoxLayout()
        allow_cheats_label = QLabel(self.tr("允许作弊"), self)
        allow_cheats_layout.addWidget(allow_cheats_label)

        self.allow_cheats_checkbox = QCheckBox(self.tr("启用"), self)
        self.allow_cheats_checkbox.setChecked(self.allow_cheats == "true")
        self.allow_cheats_checkbox.stateChanged.connect(self.save_allow_cheats)
        allow_cheats_layout.addWidget(self.allow_cheats_checkbox)

        layout.addLayout(allow_cheats_layout)

        # Central widget
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def init_menu(self):
        menu_bar = QMenuBar(self)

        # Switch Menu
        switch_menu = QMenu(self.tr("切换"), self)
        menu_bar.addMenu(switch_menu)

        # Language Menu
        language_menu = QMenu(self.tr("语言"), self)
        menu_bar.addMenu(language_menu)

        # About Menu
        about_menu = QMenu(self.tr("关于"), self)

        feedback_action = QAction(self.tr("反馈BUG"), self)
        feedback_action.triggered.connect(self.open_bug_report_url)
        about_menu.addAction(feedback_action)

        donate_action = QAction(self.tr("赞助作者"), self)
        about_menu.addAction(donate_action)

        about_action = QAction(self.tr("关于此软件"), self)
        about_menu.addAction(about_action)

        menu_bar.addMenu(about_menu)

        self.setMenuBar(menu_bar)

    def open_bug_report_url(self):
        url = QUrl("https://github.com/TC999/BDS-World-Selector/issues")
        QDesktopServices.openUrl(url)

    def read_server_name(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("server-name="):
                        return line.split("=", 1)[1].strip()
        return ""

    def save_server_name(self):
        new_server_name = self.server_name_edit.text().strip()
        if new_server_name:
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.startswith("server-name="):
                        f.write(f"server-name={new_server_name}\n")
                    else:
                        f.write(line)

            QMessageBox.information(self, self.tr("保存成功"), self.tr("服务器名称已更新。"))
        else:
            QMessageBox.warning(self, self.tr("保存失败"), self.tr("服务器名称不能为空。"))

    def read_gamemode(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("gamemode="):
                        return line.split("=", 1)[1].strip()
        return "survival"  # 默认值

    def save_gamemode(self):
        selected_gamemode = self.gamemode_combo.currentText()
        gamemode_value = self.get_gamemode_value(selected_gamemode)

        if gamemode_value:
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.startswith("gamemode="):
                        f.write(f"gamemode={gamemode_value}\n")
                    else:
                        f.write(line)

            QMessageBox.information(self, self.tr("保存成功"), self.tr("游戏模式已更新。"))

    def get_gamemode_display_name(self, gamemode_value):
        if gamemode_value == "creative":
            return self.tr("创造")
        elif gamemode_value == "survival":
            return self.tr("生存")
        elif gamemode_value == "adventure":
            return self.tr("冒险")
        return self.tr("生存")  # 默认显示为“生存”

    def get_gamemode_value(self, display_name):
        if display_name == self.tr("创造"):
            return "creative"
        elif display_name == self.tr("生存"):
            return "survival"
        elif display_name == self.tr("冒险"):
            return "adventure"
        return "survival"  # 默认值

    def read_force_gamemode(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("force-gamemode="):
                        return line.split("=", 1)[1].strip()
        return "false"  # 默认值

    def save_force_gamemode(self):
        force_gamemode_value = "true" if self.force_gamemode_checkbox.isChecked() else "false"

        if force_gamemode_value:
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.startswith("force-gamemode="):
                        f.write(f"force-gamemode={force_gamemode_value}\n")
                    else:
                        f.write(line)

            QMessageBox.information(self, self.tr("保存成功"), self.tr("强制游戏模式已更新。"))

    def read_difficulty(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("difficulty="):
                        difficulty = line.split("=", 1)[1].strip()
                        if difficulty in ["hard", "normal", "easy", "peaceful"]:
                            return difficulty
        return "normal"  # 默认值

    def save_difficulty(self):
        selected_difficulty = self.difficulty_combo.currentText()
        difficulty_value = self.get_difficulty_value(selected_difficulty)

        if difficulty_value:
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.startswith("difficulty="):
                        f.write(f"difficulty={difficulty_value}\n")
                    else:
                        f.write(line)

            QMessageBox.information(self, self.tr("保存成功"), self.tr("难度已更新。"))

    def get_difficulty_display_name(self, difficulty_value):
        if difficulty_value == "hard":
            return self.tr("困难")
        elif difficulty_value == "normal":
            return self.tr("普通")
        elif difficulty_value == "easy":
            return self.tr("简单")
        elif difficulty_value == "peaceful":
            return self.tr("和平")
        return self.tr("普通")  # 默认显示为“普通”

    def get_difficulty_value(self, display_name):
        if display_name == self.tr("困难"):
            return "hard"
        elif display_name == self.tr("普通"):
            return "normal"
        elif display_name == self.tr("简单"):
            return "easy"
        elif display_name == self.tr("和平"):
            return "peaceful"
        return "normal"  # 默认值

    def read_allow_cheats(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("allow-cheats="):
                        return line.split("=", 1)[1].strip()
        return "false"  # 默认值

    def save_allow_cheats(self):
        allow_cheats_value = "true" if self.allow_cheats_checkbox.isChecked() else "false"

        if allow_cheats_value:
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.startswith("allow-cheats="):
                        f.write(f"allow-cheats={allow_cheats_value}\n")
                    else:
                        f.write(line)

            QMessageBox.information(self, self.tr("保存成功"), self.tr("允许作弊已更新。"))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = ConfigSwitcherApp()
    main_window.show()

    sys.exit(app.exec_())
