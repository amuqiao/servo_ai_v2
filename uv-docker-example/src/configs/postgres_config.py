from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.configs import ApiConfig
from src.configs.database import Base  # 共享MySQL的声明式基类（关键优化）
import logging

logger = logging.getLogger(__name__)

# 获取全局配置
config = ApiConfig()

# 构建 PostgreSQL 连接 URL（复用ApiConfig的database配置）
DATABASE_URL = f"postgresql://{config.database.user}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.db_name}"

# 创建数据库引擎（连接池配置与MySQL保持一致）
engine = create_engine(
    DATABASE_URL,
    pool_size=10,          # 与database.py的pool_config一致
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,    # 预检查连接有效性
    echo=False             # 生产环境关闭SQL日志
)

# 创建会话工厂（依赖注入使用）
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session
)

def get_postgres_db() -> Session:
    """依赖项：获取PostgreSQL数据库会话"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"PostgreSQL会话异常: {str(e)}")
        db.rollback()
        raise  # 保持与database.py的异常处理一致
    finally:
        db.close()