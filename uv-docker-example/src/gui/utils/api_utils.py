import requests
# 错误导入：from ttkbootstrap import Messagebox
# 修正后
from ttkbootstrap.dialogs import Messagebox
from src.gui.config.api_config import API_BASE_URL  # 新增：导入配置（修改点）

class APIUtils:
    @staticmethod
    def call_api(method: str, endpoint: str, json_data: dict = None, api_url: str = API_BASE_URL) -> dict:  # 修改点：添加默认值
        url = f"{api_url}{endpoint}"
        try:
            response = requests.request(method, url, json=json_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            Messagebox.show_error(f"接口调用失败：{str(e)}")
            return {"status": "error", "message": str(e)}