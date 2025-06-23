import requests
import logging
from src.configs.config import get_config
from requests.exceptions import RequestException
from json import JSONDecodeError

class UserGuiService:
    def __init__(self):
        self.base_url = get_config().api_base_url  # 从配置获取API地址
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def _handle_request(self, request_func, success_msg, action_name, success_data=lambda r: {}):
        try:
            response = request_func()
            response.raise_for_status()
            self.logger.info(f"[{action_name}]成功 | 错误码: {UserErrorCode.SUCCESS.value} | {success_msg}")
            return {"status": "success", "code": UserErrorCode.SUCCESS.value, **success_data(response)}
        except RequestException as e:
            error_code = UserErrorCode.UNKNOWN_ERROR.value
            error_message = f"[{action_name}]失败: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    response_data = e.response.json()
                    # 显式匹配后端错误码
                    error_code = response_data.get('code', UserErrorCode.UNKNOWN_ERROR.value)
                    error_message = response_data.get('message', error_message)
                except (JSONDecodeError, ValueError):
                    pass  # 响应非JSON格式
            self.logger.error(f"[{action_name}]失败 | 错误码: {error_code} | {error_message}")
            return {"status": "error", "code": error_code, "message": error_message}
        except Exception as e:
            error_msg = f"[{action_name}]发生未知异常: {str(e)}"
            self.logger.error(f"[{action_name}]未知异常 | 错误码: {UserErrorCode.UNKNOWN_ERROR.value} | {error_msg}")
            return {"status": "error", "code": UserErrorCode.UNKNOWN_ERROR.value, "message": error_msg}

    def get_all_users(self):
        self.logger.info(f"开始获取用户列表，请求地址：{self.base_url}/users")
        return self._handle_request(
            lambda: requests.get(f"{self.base_url}/users"),
            success_msg="用户列表获取成功",
            action_name="获取用户列表",
            success_data=lambda r: {"data": r.json().get("data")}
        )

    # 关键代码片段（接口调用实现）
    def create_user(self, username: str, email: str):
        self.logger.info(f"开始创建用户，用户名：{username}，邮箱：{email}")
        return self._handle_request(
            lambda: requests.post(f"{self.base_url}/users", json={"username": username, "email": email}),
            success_msg="用户创建成功",
            action_name="创建用户",
            success_data=lambda r: {"data": r.json().get("data")}
        )

    def get_user(self, user_id: int):
        self.logger.info(f"开始获取单个用户，用户ID：{user_id}")
        return self._handle_request(
            lambda: requests.get(f"{self.base_url}/users/{user_id}"),
            success_msg="单个用户获取成功",
            action_name="获取单个用户",
            success_data=lambda r: {"data": r.json().get("data")}
        )

    def update_user(self, user_id: int, new_username: str, new_email: str):
        self.logger.info(f"开始更新用户，用户ID：{user_id}，新用户名：{new_username if new_username else '无'}，新邮箱：{new_email if new_email else '无'}")
        return self._handle_request(
            lambda: requests.put(
                f"{self.base_url}/users/{user_id}",
                json={k: v for k, v in {"username": new_username, "email": new_email}.items() if v}
            ),
            success_msg="用户更新成功",
            action_name="更新用户",
            success_data=lambda r: {"message": "用户更新成功"}
        )

    def delete_user(self, user_id: int):
        self.logger.info(f"开始删除用户，用户ID：{user_id}")
        return self._handle_request(
            lambda: requests.delete(f"{self.base_url}/users/{user_id}"),
            success_msg="用户删除成功",
            action_name="删除用户",
            success_data=lambda r: {"message": "用户删除成功"}
        )