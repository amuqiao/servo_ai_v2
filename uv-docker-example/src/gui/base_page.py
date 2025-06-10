from ttkbootstrap.scrolled import ScrolledFrame
from src.gui.config.api_config import API_BASE_URL
import requests
from ttkbootstrap.dialogs import Messagebox

class BasePage(ScrolledFrame):
    """页面基类（提供通用布局和接口调用方法）"""
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.api_url = API_BASE_URL

    def call_api(self, method: str, endpoint: str, json_data: dict = None) -> dict:
        """通用API调用方法"""
        url = f"{self.api_url}{endpoint}"
        try:
            response = requests.request(method, url, json=json_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            Messagebox.show_error(f"接口调用失败：{str(e)}")
            return {"status": "error", "message": str(e)}