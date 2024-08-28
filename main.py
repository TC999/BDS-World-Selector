import os
import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QCheckBox, QFormLayout, QMessageBox, QSpacerItem, QSizePolicy,
    QMenuBar, QAction, QMenu
)

class ConfigSwitcherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config_file_path = "server.properties"  # 假设配置文件路径
        self.worlds_dir = "worlds"  # 假设存档文件夹路径

        # 初始化配置
        self.server_name = self.read_server_name()
        self.gamemode = self.read_gamemode()
        self.force_gamemode = self.read_force_gamemode()
        self.difficulty = self.read_difficulty()
        self.allow_cheats = self.read_allow_cheats()
        self.max_players = self.read_max_players()
        self.online_mode = self.read_online_mode()
        self.allow_list = self.read_allow_list()
        self.level_name = self.read_level_name()
        self.server_port = ""  # 初始化为默认值或从配置中读取
        self.server_portv6 = ""  # 初始化为默认值或从配置中读取

        self.init_ui()
        self.init_menu()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        form_layout = QFormLayout()

        # 服务器名称
        self.server_name_edit = QLineEdit()
        self.server_name_edit.setText(self.server_name)
        self.server_name_save_button = QPushButton("保存")
        self.server_name_save_button.clicked.connect(self.save_server_name)
        form_layout.addRow(QLabel("服务器名称:"), self.server_name_edit)
        form_layout.addWidget(self.server_name_save_button)

        # 存档切换
        self.world_combo = QComboBox()
        self.load_worlds()  # Load worlds to populate combo box
        self.world_save_button = QPushButton("保存")
        self.world_save_button.clicked.connect(self.save_level_name)
        form_layout.addRow(QLabel("存档切换:"), self.world_combo)
        form_layout.addWidget(self.world_save_button)

        layout.addLayout(form_layout)

        # 游戏模式
        self.gamemode_combo = QComboBox()
        self.gamemode_combo.addItems(["创造", "生存", "冒险"])
        self.gamemode_combo.setCurrentText(self.gamemode)
        self.gamemode_save_button = QPushButton("保存")
        self.gamemode_save_button.clicked.connect(self.save_gamemode)
        form_layout.addRow(QLabel("游戏模式:"), self.gamemode_combo)
        form_layout.addWidget(self.gamemode_save_button)

        # 强制游戏模式
        self.force_gamemode_checkbox = QCheckBox()
        self.force_gamemode_checkbox.setChecked(self.force_gamemode == "true")
        self.force_gamemode_save_button = QPushButton("保存")
        self.force_gamemode_save_button.clicked.connect(self.save_force_gamemode)
        form_layout.addRow(QLabel("强制游戏模式:"), self.force_gamemode_checkbox)
        form_layout.addWidget(self.force_gamemode_save_button)

        # 难度
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["困难", "普通", "简单", "和平"])
        self.difficulty_combo.setCurrentText(self.difficulty)
        self.difficulty_save_button = QPushButton("保存")
        self.difficulty_save_button.clicked.connect(self.save_difficulty)
        form_layout.addRow(QLabel("难度:"), self.difficulty_combo)
        form_layout.addWidget(self.difficulty_save_button)

        # 允许作弊
        self.allow_cheats_checkbox = QCheckBox()
        self.allow_cheats_checkbox.setChecked(self.allow_cheats == "true")
        self.allow_cheats_save_button = QPushButton("保存")
        self.allow_cheats_save_button.clicked.connect(self.save_allow_cheats)
        form_layout.addRow(QLabel("允许作弊:"), self.allow_cheats_checkbox)
        form_layout.addWidget(self.allow_cheats_save_button)

        # 人数上限
        self.max_players_edit = QLineEdit()
        self.max_players_edit.setText(self.max_players)
        self.max_players_save_button = QPushButton("保存")
        self.max_players_save_button.clicked.connect(self.save_max_players)
        form_layout.addRow(QLabel("人数上限:"), self.max_players_edit)
        form_layout.addWidget(self.max_players_save_button)

        # 正版验证
        self.online_mode_checkbox = QCheckBox()
        self.online_mode_checkbox.setChecked(self.online_mode == "true")
        self.online_mode_save_button = QPushButton("保存")
        self.online_mode_save_button.clicked.connect(self.save_online_mode)
        form_layout.addRow(QLabel("正版验证:"), self.online_mode_checkbox)
        form_layout.addWidget(self.online_mode_save_button)

        # 白名单
        self.allow_list_checkbox = QCheckBox()
        self.allow_list_checkbox.setChecked(self.allow_list == "true")
        self.allow_list_save_button = QPushButton("保存")
        self.allow_list_save_button.clicked.connect(self.save_allow_list)
        form_layout.addRow(QLabel("白名单:"), self.allow_list_checkbox)
        form_layout.addWidget(self.allow_list_save_button)

        # IPV4 地址(有 BUG)
        self.ipv4_edit = QLineEdit()
        self.ipv4_edit.setPlaceholderText("输入 1 至 65535 的正整数")
        self.ipv4_edit.setText(self.server_port)
        self.ipv4_save_button = QPushButton("保存")
        self.ipv4_save_button.clicked.connect(self.save_server_port)
        form_layout.addRow(QLabel("IPV4 地址:"), self.ipv4_edit)
        form_layout.addWidget(self.ipv4_save_button)

        # IPV6 地址(有 BUG)
        self.ipv6_edit = QLineEdit()
        self.ipv6_edit.setPlaceholderText("输入 1 至 65535 的正整数")
        self.ipv6_edit.setText(self.server_portv6)
        self.ipv6_save_button = QPushButton("保存")
        self.ipv6_save_button.clicked.connect(self.save_server_portv6)
        form_layout.addRow(QLabel("IPV6 地址:"), self.ipv6_edit)
        form_layout.addWidget(self.ipv6_save_button)

        self.setWindowTitle("基岩版服务端存档切换器")
        self.setGeometry(100, 100, 600, 600)  # 设置初始窗口大小

    def init_menu(self):
        menu_bar = QMenuBar(self)

        # Switch Menu 切换
        switch_menu = QMenu(self.tr("切换"), self)
        menu_bar.addMenu(switch_menu)

        # Language Menu 语言（暂未实现）
        language_menu = QMenu(self.tr("语言"), self)
        menu_bar.addMenu(language_menu)

        # About Menu 关于
        about_menu = QMenu(self.tr("关于"), self)

        feedback_action = QAction(self.tr("反馈BUG"), self)
        feedback_action.triggered.connect(self.open_bug_report_url)
        about_menu.addAction(feedback_action)

        donate_action = QAction(self.tr("赞助作者"), self)
        about_menu.addAction(donate_action)

        about_action = QAction(self.tr("关于此软件"), self)
        about_action.triggered.connect(self.show_about_dialog)
        about_menu.addAction(about_action)

        menu_bar.addMenu(about_menu)

        self.setMenuBar(menu_bar)

    def open_bug_report_url(self): # 反馈BUG
        url = QUrl("https://github.com/TC999/BDS-World-Selector/issues")
        QDesktopServices.openUrl(url)

    # 关于此软件
    def show_about_dialog(self):
        """显示关于软件的对话框"""
        about_message = (
            "基岩版服务端存档切换器\n"
            "作者：TC999\n"
            "源码页面：https://github.com/TC999/BDS-World-Selector\n"
            "许可证：GPL3\n"
            "使用项目：\n"
            "PyQt5 - 窗口框架\n"
            "贡献者：\n"
            "TC999 - 所有者\n"
            "ChatGPT4o - 代码编写 & 修 BUG"
        )

        QMessageBox.information(self, "关于此软件", about_message)

    # 读取
    def read_server_name(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("server-name="):
                        return line.split("=", 1)[1].strip()
        return ""

    def save_server_name(self):
        server_name_value = self.server_name_edit.text().strip()

        with open(self.config_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open(self.config_file_path, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.startswith("server-name="):
                    f.write(f"server-name={server_name_value}\n")
                else:
                    f.write(line)

        QMessageBox.information(self, self.tr("保存成功"), self.tr("服务器名称已更新。"))

    def read_gamemode(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("gamemode="):
                        return line.split("=", 1)[1].strip()
        return "creative"

    def save_gamemode(self):
        selected_gamemode = self.gamemode_combo.currentText()
        gamemode_value = self.get_gamemode_value(selected_gamemode)

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
        return self.tr("生存")

    def get_gamemode_value(self, display_name):
        if display_name == self.tr("创造"):
            return "creative"
        elif display_name == self.tr("生存"):
            return "survival"
        elif display_name == self.tr("冒险"):
            return "adventure"
        return "survival"

    def read_force_gamemode(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("force-gamemode="):
                        return line.split("=", 1)[1].strip()
        return "false"

    def save_force_gamemode(self):
        force_gamemode_value = "true" if self.force_gamemode_checkbox.isChecked() else "false"

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
        return "normal"

    def save_difficulty(self):
        selected_difficulty = self.difficulty_combo.currentText()
        difficulty_value = self.get_difficulty_value(selected_difficulty)

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
        return self.tr("普通")

    def get_difficulty_value(self, display_name):
        if display_name == self.tr("困难"):
            return "hard"
        elif display_name == self.tr("普通"):
            return "normal"
        elif display_name == self.tr("简单"):
            return "easy"
        elif display_name == self.tr("和平"):
            return "peaceful"
        return "normal"

    def read_allow_cheats(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("allow-cheats="):
                        return line.split("=", 1)[1].strip()
        return "false"

    def save_allow_cheats(self):
        allow_cheats_value = "true" if self.allow_cheats_checkbox.isChecked() else "false"

        with open(self.config_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open(self.config_file_path, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.startswith("allow-cheats="):
                    f.write(f"allow-cheats={allow_cheats_value}\n")
                else:
                    f.write(line)

        QMessageBox.information(self, self.tr("保存成功"), self.tr("允许作弊已更新。"))

    def read_max_players(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("max-players="):
                        return line.split("=", 1)[1].strip()
        return "0"

    def save_max_players(self):
        max_players_value = self.max_players_edit.text().strip()

        if max_players_value.isdigit() and int(max_players_value) > 0:
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.startswith("max-players="):
                        f.write(f"max-players={max_players_value}\n")
                    else:
                        f.write(line)

            QMessageBox.information(self, self.tr("保存成功"), self.tr("人数上限已更新。"))
        else:
            QMessageBox.warning(self, self.tr("保存失败"), self.tr("人数上限必须是正整数。"))

    def read_online_mode(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("online-mode="):
                        return line.split("=", 1)[1].strip()
        return "false"

    def save_online_mode(self):
        online_mode_value = "true" if self.online_mode_checkbox.isChecked() else "false"

        with open(self.config_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open(self.config_file_path, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.startswith("online-mode="):
                    f.write(f"online-mode={online_mode_value}\n")
                else:
                    f.write(line)

        QMessageBox.information(self, self.tr("保存成功"), self.tr("正版验证已更新。"))

    def read_allow_list(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("allow-list="):
                        return line.split("=", 1)[1].strip()
        return "false"

    def save_allow_list(self):
        allow_list_value = "true" if self.allow_list_checkbox.isChecked() else "false"

        with open(self.config_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open(self.config_file_path, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.startswith("allow-list="):
                    f.write(f"allow-list={allow_list_value}\n")
                else:
                    f.write(line)

        QMessageBox.information(self, self.tr("保存成功"), self.tr("白名单已更新。"))

    def read_level_name(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("level-name="):
                        return line.split("=", 1)[1].strip()
        return ""

    def save_level_name(self):
        level_name_value = self.world_combo.currentText()

        with open(self.config_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open(self.config_file_path, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.startswith("level-name="):
                    f.write(f"level-name={level_name_value}\n")
                else:
                    f.write(line)

        QMessageBox.information(self, self.tr("保存成功"), self.tr("存档已更新。"))

    def load_worlds(self):
        if os.path.isdir(self.worlds_dir):
            self.world_folders = [name for name in os.listdir(self.worlds_dir) if os.path.isdir(os.path.join(self.worlds_dir, name))]
            self.world_combo.clear()
            self.world_combo.addItems(self.world_folders)
        else:
            self.world_folders = []
            self.world_combo.addItem(self.tr("存档文件夹不存在"))

        # 保存 IPV4 地址

    def read_server_port(self):
        """读取 'server-port=' 配置项"""
        with open(self.config_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("server-port="):
                    return line.split("=")[1].strip()
        return ""

    def read_server_portv6(self):
        """读取 'server-portv6=' 配置项"""
        with open(self.config_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("server-portv6="):
                    return line.split("=")[1].strip()
        return ""

    def save_server_port(self):
        """保存 'server-port=' 配置项"""
        new_port = self.server_port_edit.text()
        self.save_config("server-port=", new_port)

    def save_server_portv6(self):
        """保存 'server-portv6=' 配置项"""
        new_portv6 = self.server_portv6_edit.text()
        self.save_config("server-portv6=", new_portv6)

    def save_config(self, key, value):
        """保存配置项到文件"""
        lines = []
        with open(self.config_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open(self.config_file_path, 'w', encoding='utf-8') as f:
            found = False
            for line in lines:
                if line.startswith(key):
                    f.write(f"{key}{value}\n")
                    found = True
                else:
                    f.write(line)
            if not found:
                f.write(f"{key}{value}\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ConfigSwitcherApp()
    main_window.show()
    sys.exit(app.exec_())
