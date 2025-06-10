from ttkbootstrap import ttk
from src.gui.utils.api_utils import APIUtils
from src.gui.config.api_config import API_BASE_URL
# 移除原循环导入，改为从独立文件导入
from src.gui.base_page import BasePage

class UserManagementPage(BasePage):
    def __init__(self, master):
        super().__init__(master)
        self.init_ui()
        self.load_users()  # 初始化时加载用户列表

    def init_ui(self):
        # 标题（优化字体样式）
        ttk.Label(
            self, text="用户管理", font=("微软雅黑", 16, "bold"), bootstyle="primary"
        ).grid(row=0, column=0, columnspan=4, pady=15)

        # 输入框（添加提示文本）
        ttk.Label(self, text="用户名").grid(row=1, column=0, padx=8, pady=8)
        self.username_entry = ttk.Entry(self, width=25)
        self.username_entry.grid(row=1, column=1, padx=8, pady=8)
        self.username_entry.insert(0, "请输入3-50位用户名")

        ttk.Label(self, text="邮箱").grid(row=1, column=2, padx=8, pady=8)
        self.email_entry = ttk.Entry(self, width=30)
        self.email_entry.grid(row=1, column=3, padx=8, pady=8)
        self.email_entry.insert(0, "请输入有效邮箱地址")

        # 按钮（使用主题样式）
        ttk.Button(
            self, text="新增用户", command=self.create_user, bootstyle="success"
        ).grid(row=2, column=0, pady=12, padx=5)
        ttk.Button(
            self, text="刷新列表", command=self.load_users, bootstyle="info"
        ).grid(row=2, column=1, pady=12, padx=5)
        ttk.Button(
            self, text="删除选中", command=self.delete_user, bootstyle="danger"
        ).grid(row=2, column=2, pady=12, padx=5)

        # 表格（添加滚动条）
        self.tree = ttk.Treeview(
            self,
            columns=("id", "username", "email"),
            show="headings",
            selectmode="browse",
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="用户名")
        self.tree.heading("email", text="邮箱")
        self.tree.grid(row=3, column=0, columnspan=4, sticky="nsew")
        ttk.Scrollbar(self, orient="vertical", command=self.tree.yview).grid(
            row=3, column=4, sticky="ns"
        )
        self.tree.configure(yscrollcommand=ttk.Scrollbar.set)

    def load_users(self):
        response = APIUtils.call_api("GET", "/users", api_url=self.api_url)
        if response.get("status") == "success":
            for item in self.tree.get_children():
                self.tree.delete(item)
            for user in response["data"]:
                self.tree.insert(
                    "", "end", values=(user["id"], user["username"], user["email"])
                )

    def create_user(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        if not (username and email):
            ttk.Messagebox.show_warning("请填写完整用户名和邮箱")
            return
        response = APIUtils.call_api(
            "POST",
            "/users",
            json_data={"username": username, "email": email},
            api_url=self.api_url,
        )
        if response.get("status") == "success":
            ttk.Messagebox.show_info("用户创建成功")
            self.load_users()
            self.username_entry.delete(0, "end")
            self.email_entry.delete(0, "end")

    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            ttk.Messagebox.show_warning("请选择要删除的用户")
            return
        user_id = self.tree.item(selected[0], "values")[0]
        response = APIUtils.call_api(
            "DELETE", f"/users/{user_id}", api_url=self.api_url
        )
        if response.get("status") == "success":
            ttk.Messagebox.show_info("用户删除成功")
            self.load_users()
