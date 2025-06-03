from redis import Redis
from src.exceptions.redis_exceptions import RedisException, RedisErrorCode  # 新增导入

class RedisCRUDService:
    @staticmethod
    def create_key(redis_client: Redis, key: str, value: str) -> bool:
        """创建键值对"""
        try:
            return redis_client.set(key, value)  # 成功返回True，失败返回False
        except Exception as e:
            # 直接抛出业务异常（替代原RuntimeError）
            raise RedisException(RedisErrorCode.OPERATION_FAILED, f"创建键失败: {str(e)}")

    @staticmethod
    def get_key(redis_client: Redis, key: str) -> str:
        """获取键值"""
        try:
            value = redis_client.get(key)
            return value if value is not None else ""
        except Exception as e:
            raise RedisException(RedisErrorCode.OPERATION_FAILED, f"获取键失败: {str(e)}")

    @staticmethod
    def update_key(redis_client: Redis, key: str, new_value: str) -> bool:
        """更新键值"""
        try:
            return redis_client.set(key, new_value)
        except Exception as e:
            raise RedisException(RedisErrorCode.OPERATION_FAILED, f"更新键失败: {str(e)}")

    @staticmethod
    def delete_key(redis_client: Redis, key: str) -> int:
        """删除键（返回删除数量）"""
        try:
            return redis_client.delete(key)  # 0（未删除）或1（已删除）
        except Exception as e:
            raise RedisException(RedisErrorCode.OPERATION_FAILED, f"删除键失败: {str(e)}")