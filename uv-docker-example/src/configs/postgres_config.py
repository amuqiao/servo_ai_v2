from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.configs.config import get_config  # 直接获取全局配置
import logging

logger = logging.getLogger(__name__)

# 获取全局配置实例（包含PostgreSQL配置）
config = get_config()

# 构建 PostgreSQL 连接 URL（使用 psycopg 3 驱动）
DATABASE_URL = f"postgresql+psycopg://{config.postgres.user}:{config.postgres.password}@{config.postgres.host}:{config.postgres.port}/{config.postgres.db_name}"

# 创建数据库引擎（连接池配置保持生产级标准）
engine = create_engine(
    DATABASE_URL,
    pool_size=10,         # 连接池初始大小
    max_overflow=5,       # 连接池超出初始大小后可创建的额外连接数
    pool_timeout=30,      # 从连接池获取连接的超时时间（秒）
    pool_recycle=3600,    # 连接回收时间（秒，避免长连接导致的问题）
    pool_pre_ping=True,   # 连接前检查有效性（防止僵尸连接）
    echo=False            # 生产环境关闭SQL日志输出
)

# 创建会话工厂（用于依赖注入）
SessionLocal = sessionmaker(
    autocommit=False,     # 关闭自动提交（需手动commit）
    autoflush=False,      # 关闭自动刷新（提升批量操作性能）
    bind=engine,          # 绑定数据库引擎
    class_=Session        # 明确会话类
)

def get_postgres_db() -> Session:
    """依赖注入：获取 PostgreSQL 数据库会话（自动管理连接生命周期）"""
    db = SessionLocal()
    try:
        yield db  # 提供给路由/服务层使用
    except Exception as e:
        logger.error(f"PostgreSQL 会话异常: {str(e)}")
        db.rollback()  # 异常时回滚事务
        raise  # 向上传递异常，由全局中间件处理
    finally:
        db.close()  # 确保连接归还连接池