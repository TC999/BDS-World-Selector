import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QVBoxLayout, QWidget, QLineEdit, QLabel, QPushButton, QMessageBox

class ConfigSwitcherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config_file_path = "server.properties"  # 假设配置文件路径
        self.server_name = self.read_server_name()

        self.init_ui()
        self.init_menu()

    def init_ui(self):
        self.setWindowTitle(self.tr("基岩版服务端存档切换器"))

        layout = QVBoxLayout()

        # Server Name
        server_name_label = QLabel(self.tr("服务器名称"), self)
        layout.addWidget(server_name_label)

        self.server_name_edit = QLineEdit(self)
        self.server_name_edit.setText(self.server_name)
        layout.addWidget(self.server_name_edit)

        save_button = QPushButton(self.tr("保存"), self)
        save_button.clicked.connect(self.save_server_name)
        layout.addWidget(save_button)

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
        about_menu.addAction(feedback_action)

        donate_action = QAction(self.tr("赞助作者"), self)
        about_menu.addAction(donate_action)

        about_action = QAction(self.tr("关于此软件"), self)
        about_menu.addAction(about_action)

        menu_bar.addMenu(about_menu)

        self.setMenuBar(menu_bar)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = ConfigSwitcherApp()
    main_window.show()

    sys.exit(app.exec_())
