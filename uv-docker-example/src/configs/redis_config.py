from fastapi import HTTPException
from redis import Redis, ConnectionPool
from src.configs import ApiConfig
import logging

logger = logging.getLogger(__name__)

# 全局连接池（单例模式）
_redis_pool = None

def get_redis_pool() -> ConnectionPool:
    """获取 Redis 连接池（单例）"""
    global _redis_pool
    if _redis_pool is None:
        config = ApiConfig()
        try:
            # 调整：通过 config.redis 获取 Redis 配置（与 config.py 新增的 RedisConfig 对应）
            _redis_pool = ConnectionPool(
                host=config.redis.host,  # 原 config.REDIS_HOST → config.redis.host
                port=config.redis.port,  # 原 config.REDIS_PORT → config.redis.port
                password=config.redis.password,  # 原 config.REDIS_PASSWORD → config.redis.password
                db=config.redis.db,  # 原 config.REDIS_DB → config.redis.db
                decode_responses=True  # 自动解码为字符串
            )
            logger.debug(f"Redis 连接池初始化成功（host={config.redis.host}:{config.redis.port}）")  # 同步日志信息
        except Exception as e:
            logger.error(f"Redis 连接池创建失败: {str(e)}")
            raise HTTPException(status_code=500, detail="Redis 连接池初始化失败")
    return _redis_pool

def get_redis_client() -> Redis:
    """依赖注入用的 Redis 客户端生成器（支持上下文管理器）"""
    pool = get_redis_pool()
    client = Redis(connection_pool=pool)
    try:
        yield client
    except Exception as e:
        logger.error(f"Redis 客户端异常: {str(e)}")
        raise HTTPException(status_code=500, detail="Redis 操作失败")
    finally:
        client.close()  # 归还连接到池（非真正关闭）