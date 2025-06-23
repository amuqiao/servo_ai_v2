from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class DatabaseConfig(BaseSettings):
    """数据库模块配置（映射.env中DB_前缀的环境变量）"""

    host: str = Field("localhost", alias="DB_HOST")
    port: int = Field(3306, alias="DB_PORT")
    user: str = Field("root", alias="DB_USER")
    password: str = Field("root", alias="DB_PASSWORD")
    db_name: str = Field("servo_ai", alias="DB_NAME")


# 新增：参考DatabaseConfig的Redis独立配置类
class RedisConfig(BaseSettings):
    """Redis模块配置（映射.env中REDIS_前缀的环境变量）"""

    host: str = Field(
        "localhost",
        alias="REDIS_HOST",
        description="Redis 服务主机名（Docker网络中为服务名）",
    )
    port: int = Field(6379, alias="REDIS_PORT", description="Redis 服务端口")
    password: str = Field(
        "123456", alias="REDIS_PASSWORD", description="Redis 访问密码"
    )
    db: int = Field(0, alias="REDIS_DB", description="Redis 数据库编号")


# 新增：PostgreSQL 独立配置类（映射.env中POSTGRES_前缀的环境变量）
class PostgresConfig(BaseSettings):
    """PostgreSQL模块配置（映射.env中POSTGRES_前缀的环境变量）"""
    host: str = Field("localhost", alias="POSTGRES_HOST")
    port: int = Field(5432, alias="POSTGRES_PORT")  # PostgreSQL默认端口5432
    user: str = Field("postgres", alias="POSTGRES_USER")
    password: str = Field("123456", alias="POSTGRES_PASSWORD")
    db_name: str = Field("servo_ai_pg", alias="POSTGRES_DB_NAME")

class ApiConfig(BaseSettings):
    """项目全局配置类（整合各模块配置）"""
    project_name: str = Field("servo_ai", alias="COMPOSE_PROJECT_NAME")
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)  # MySQL配置
    redis: RedisConfig = Field(default_factory=RedisConfig)          # Redis配置
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)  # 新增：PostgreSQL配置
    api_base_url: str = Field("http://localhost:8000", alias="API_BASE_URL", description="API服务基础URL")  # 新增字段

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )


def get_config() -> ApiConfig:
    """依赖项：返回全局配置实例（每次调用生成新实例）"""
    return ApiConfig()


if __name__ == "__main__":
    # 测试配置加载（验证是否正确读取.env中的最新值）
    config = ApiConfig()
    print(f"项目名称: {config.project_name}")
    print(f"数据库主机: {config.database.host}")  # 预期输出.env中的DB_HOST值
    print(f"Redis主机: {config.redis.host}")  # 新增：验证Redis配置加载
