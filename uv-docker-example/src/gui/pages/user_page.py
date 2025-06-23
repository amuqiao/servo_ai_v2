from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QDialog, QInputDialog, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from src.gui.services.user_service import UserGuiService

class UserPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.user_service = UserGuiService()
        self.load_users()

    def init_ui(self):
        layout = QVBoxLayout()
        self.table = QTableWidget()
        # 添加功能按钮
        self.btn_refresh = QPushButton("刷新用户列表")
        self.btn_create = QPushButton("创建用户")
        self.btn_get = QPushButton("获取单个用户")
        self.btn_update = QPushButton("更新用户")
        self.btn_delete = QPushButton("删除用户")

        # 绑定按钮事件
        self.btn_refresh.clicked.connect(self.load_users)
        # 关键代码片段（按钮绑定与弹窗逻辑）
        self.btn_create.clicked.connect(self.show_create_dialog)
        self.btn_get.clicked.connect(self.show_get_dialog)
        self.btn_update.clicked.connect(self.show_update_dialog)
        self.btn_delete.clicked.connect(self.show_delete_dialog)

        # 添加控件到布局
        layout.addWidget(self.table)
        layout.addWidget(self.btn_refresh)
        layout.addWidget(self.btn_create)
        layout.addWidget(self.btn_get)
        layout.addWidget(self.btn_update)
        layout.addWidget(self.btn_delete)
        self.setLayout(layout)

    def load_users(self):
        # 调用接口获取用户数据并更新表格
        result = self.user_service.get_all_users()
        if isinstance(result, dict) and result.get("status") == "success":
            users = result.get("data", [])
            self.table.setRowCount(len(users))
            # 填充表格逻辑（示例：假设用户有id、username、email字段）
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["ID", "用户名", "邮箱"])
            for row, user in enumerate(users):
                self.table.setItem(row, 0, QTableWidgetItem(str(user.get("id"))))
                self.table.setItem(row, 1, QTableWidgetItem(user.get("username")))
                self.table.setItem(row, 2, QTableWidgetItem(user.get("email")))
        else:
            # 处理获取用户列表失败的情况
            self.table.setRowCount(0)
            error_msg = result.get("message", "获取用户列表失败") if isinstance(result, dict) else "获取用户列表失败"
            QMessageBox.warning(self, "错误", error_msg)

    def show_create_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("创建用户")
        layout = QVBoxLayout()
        
        username_label = QLabel("用户名：")
        self.username_input = QLineEdit()
        email_label = QLabel("邮箱：")
        self.email_input = QLineEdit()
        confirm_btn = QPushButton("确认创建")

        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(confirm_btn)

        confirm_btn.clicked.connect(lambda: self.create_user(dialog))
        dialog.setLayout(layout)
        dialog.exec_()

    def create_user(self, dialog):
        username = self.username_input.text()
        email = self.email_input.text()
        if not username or not email:
            QMessageBox.warning(self, "错误", "用户名和邮箱不能为空")
            return
        result = self.user_service.create_user(username, email)
        if isinstance(result, dict):
            if result.get("status") == "success":
                QMessageBox.information(self, "成功", "用户创建成功")
                self.load_users()  # 刷新列表
            else:
                error_msg = result.get("message", "创建失败")
                error_code = result.get("code")
                if error_code is not None:
                    error_msg += f"（错误码：{error_code}）"
                QMessageBox.critical(self, "错误", error_msg)
        else:
            QMessageBox.critical(self, "错误", "创建用户失败：无效的响应格式")
        dialog.close()

    def show_get_dialog(self):
        user_id, ok = QInputDialog.getInt(self, "获取用户", "请输入用户ID：")
        if ok and user_id > 0:
            result = self.user_service.get_user(user_id)
            if isinstance(result, dict) and result.get("status") == "success":
                user_data = result.get("data")
                if user_data:
                    QMessageBox.information(self, "用户详情", f"ID: {user_data['id']}\n用户名: {user_data['username']}\n邮箱: {user_data['email']}")
                else:
                    QMessageBox.warning(self, "错误", "用户数据为空")
            else:
                error_msg = result.get("message", "获取用户失败") if isinstance(result, dict) else "获取用户失败"
                QMessageBox.critical(self, "错误", error_msg)

    def show_update_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("更新用户")
        layout = QVBoxLayout()

        user_id_label = QLabel("用户ID：")
        self.user_id_input = QLineEdit()
        username_label = QLabel("新用户名（可选）：")
        self.new_username_input = QLineEdit()
        email_label = QLabel("新邮箱（可选）：")
        self.new_email_input = QLineEdit()
        confirm_btn = QPushButton("确认更新")

        layout.addWidget(user_id_label)
        layout.addWidget(self.user_id_input)
        layout.addWidget(email_label)
        layout.addWidget(self.new_email_input)
        layout.addWidget(confirm_btn)

        confirm_btn.clicked.connect(lambda: self.update_user(dialog))
        dialog.setLayout(layout)
        dialog.exec_()

    def update_user(self, dialog):
        user_id = self.user_id_input.text()
        new_username = self.new_username_input.text().strip()
        new_email = self.new_email_input.text().strip()
        if not user_id.isdigit():
            QMessageBox.warning(self, "错误", "请输入有效的用户ID")
            return
        result = self.user_service.update_user(int(user_id), new_username, new_email)
        if isinstance(result, dict):
            if result.get("status") == "success":
                QMessageBox.information(self, "成功", "用户更新成功")
                self.load_users()  # 刷新列表
            else:
                error_msg = result.get("message", "更新失败")
                error_code = result.get("code")
                if error_code is not None:
                    error_msg += f"（错误码：{error_code}）"
                QMessageBox.critical(self, "错误", error_msg)
        else:
            QMessageBox.critical(self, "错误", "更新用户失败：无效的响应格式")
        dialog.close()

    def show_delete_dialog(self):
        user_id, ok = QInputDialog.getInt(self, "删除用户", "请输入要删除的用户ID：")
        if ok and user_id > 0:
            reply = QMessageBox.question(self, "确认删除", f"确定要删除用户ID {user_id} 吗？",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    result = self.user_service.delete_user(user_id)
                except Exception as e:
                    # 捕获服务层未处理的异常，避免程序中断
                    result = {"status": "error", "message": f"删除操作发生异常: {str(e)}", "code": None}
                if isinstance(result, dict):
                    if result.get("status") == "success":
                        QMessageBox.information(self, "成功", "用户删除成功")
                        self.load_users()  # 刷新列表
                    else:
                        error_msg = result.get("message", "删除失败")
                        error_code = result.get("code")
                        if error_code is not None:
                            error_msg += f"（错误码：{error_code}）"
                        QMessageBox.critical(self, "错误", error_msg)
                else:
                    QMessageBox.critical(self, "错误", "删除用户失败：无效的响应格式")