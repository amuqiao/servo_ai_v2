import os
import redis
from redis import RedisError

def check_redis_connection():
    # 从环境变量获取配置（与docker-compose保持一致）
    redis_config = {
        "host": "localhost",  # docker-compose服务名（同一网络内）
        "port": 6379,
        "password": os.getenv("REDIS_PASSWORD", "123456"),
        "decode_responses": True
    }

    try:
        r = redis.Redis(**redis_config)
        if r.ping():
            print("Redis连接成功！")
            return True
        else:
            print("Redis连接失败：ping未返回成功")
            return False
    except RedisError as e:
        print(f"Redis连接失败：{str(e)}")
        return False

if __name__ == "__main__":
    check_redis_connection()