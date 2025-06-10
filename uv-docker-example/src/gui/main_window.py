import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
# 从拆分后的配置文件导入（修改点）
from src.gui.config.style_config import init_style
from src.gui.config.window_config import WINDOW_SIZE
from src.gui.config.api_config import API_BASE_URL
import threading
from src.uv_docker_example.main import app
import uvicorn
# 新增：从pages目录导入正确的UserManagementPage
from src.gui.pages.user_management import UserManagementPage
# 新增：从独立文件导入BasePage
from src.gui.base_page import BasePage

class MainWindow:
    def __init__(self):
        # 初始化样式
        self.style = init_style()
        # 创建主窗口
        self.root = ttk.Window(title="Servo AI V2 管理工具", size=WINDOW_SIZE)
        # 初始化子页面（用户管理页）
        self.user_management_page = UserManagementPage(self.root)
        # 布局
        self.user_management_page.pack(fill='both', expand=True)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    # 启动FastAPI服务到子线程
    def run_fastapi():
        uvicorn.run(app, host="0.0.0.0", port=8000)
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    # 启动GUI主循环（主线程）
    app = MainWindow()
    app.run()