from fastapi import Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from src.configs import ApiConfig
from src.configs.logging_config import setup_logging
from urllib.parse import quote_plus
from sqlalchemy.engine import URL
import logging
from functools import lru_cache

# 初始化日志配置（确保日志生效）
setup_logging()

logger = logging.getLogger(__name__)

Base = declarative_base()

# 使用 lru_cache 缓存引擎实例（单例）
@lru_cache(maxsize=1)
def get_db_engine():
    """创建带连接池配置的数据库引擎（单例）"""
    config = ApiConfig()
    db_config = config.database  # 从 ApiConfig 中获取嵌套的 DatabaseConfig 实例
    try:
        connection_dict = {
            "drivername": "mysql+pymysql",
            "username": db_config.user,  # 修正为 db_config.user
            "password": quote_plus(db_config.password),  # 修正为 db_config.password
            "host": db_config.host,  # 修正为 db_config.host
            "port": db_config.port,  # 修正为 db_config.port
            "database": db_config.db_name  # 修正为 db_config.db_name
        }
        
        logger.info(
            "正在初始化数据库连接，驱动：%s, 主机：%s, 端口：%s, 数据库：%s, 用户：%s",
            connection_dict["drivername"],
            connection_dict["host"],
            connection_dict["port"],
            connection_dict["database"],
            connection_dict["username"]
        )

        # 连接池配置
        pool_config = {
            "pool_size": 10,          # 连接池保持的连接数
            "max_overflow": 5,        # 允许临时增加的连接数
            "pool_timeout": 30,       # 获取连接的超时时间（秒）
            "pool_recycle": 3600      # 连接重置周期（秒）
        }
        
        connection_url = URL.create(**connection_dict)
        return create_engine(
            connection_url, 
            pool_pre_ping=True,       # 预检查连接有效性
            echo=False,               # 关闭 SQL 日志（生产环境建议关闭）
            **pool_config
        )
    except Exception as e:
        logger.error(f"数据库引擎创建失败: {str(e)}")
        raise HTTPException(status_code=500, detail="数据库引擎初始化失败")

# 重命名为更清晰的变量名
db_session_factory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_db_engine(),
    class_=Session
)

def get_db_session() -> Session:  # 重命名函数
    """依赖注入用的数据库会话生成器"""
    db = db_session_factory()
    try:
        yield db
    except Exception as e:
        logger.error(f"数据库会话异常: {str(e)}")
        db.rollback()  # 异常时回滚事务
        raise HTTPException(status_code=500, detail="数据库操作失败")
    finally:
        db.close()  # 确保会话关闭（归还连接池）
