import os
import psycopg
from psycopg import OperationalError
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# 数据库配置（与项目默认值一致，可通过环境变量覆盖）
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "123456"),
    "target_db": os.getenv("POSTGRES_DB_NAME", "servo_ai_pg"),  # 目标数据库名（与项目配置一致）
    "default_db": "postgres"  # PostgreSQL默认系统数据库（用于创建目标库）
}

def create_database_if_not_exists():
    """连接默认数据库，创建目标数据库（幂等操作）"""
    try:
        # 连接默认数据库（确保目标库不存在时也能连接）
        with psycopg.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            dbname=DB_CONFIG["default_db"]
        ) as conn:
            conn.autocommit = True  # 创建数据库需要自动提交
            with conn.cursor() as cursor:
                # 检查数据库是否已存在
                cursor.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s",
                    (DB_CONFIG["target_db"],)
                )
                if not cursor.fetchone():
                    cursor.execute(f"CREATE DATABASE {DB_CONFIG['target_db']}")
                    logger.info(f"数据库 {DB_CONFIG['target_db']} 创建成功")
                else:
                    logger.info(f"数据库 {DB_CONFIG['target_db']} 已存在，跳过创建")
    except OperationalError as e:
        logger.error(f"创建数据库失败：{str(e)}")
        raise

def create_tables_if_not_exists():
    """连接目标数据库，创建业务表（幂等操作）"""
    try:
        with psycopg.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            dbname=DB_CONFIG["target_db"]
        ) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                # 创建用户表（新增 created_at 和 updated_at 字段）
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,  -- 新增：创建时间（带时区）
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP   -- 新增：更新时间（初始为创建时间）
                    )
                """)
                logger.info("用户表 users 创建成功（或已存在）")
    except OperationalError as e:
        logger.error(f"创建表失败：{str(e)}")
        raise

def insert_default_data():
    """插入默认测试数据（幂等操作，冲突时跳过）"""
    try:
        with psycopg.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            dbname=DB_CONFIG["target_db"]
        ) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                # 插入示例用户（如果不存在）
                cursor.execute("""
                    INSERT INTO users (username, email)
                    VALUES ('admin', 'admin@example.com')
                    ON CONFLICT (username) DO NOTHING
                """)
                if cursor.rowcount > 0:
                    logger.info("默认用户 admin 插入成功")
                else:
                    logger.info("默认用户 admin 已存在，跳过插入")
    except OperationalError as e:
        logger.error(f"插入默认数据失败：{str(e)}")
        raise

if __name__ == "__main__":
    # python e:/github_project/servo_ai_v2_project/servo_ai_v2/uv-docker-example/scripts/initialize_postgres.py
    logger.info("开始执行数据库初始化流程...")
    create_database_if_not_exists()
    create_tables_if_not_exists()
    insert_default_data()
    logger.info("数据库初始化完成！")