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


class ApiConfig(BaseSettings):
    """项目全局配置类（整合各模块配置，从.env文件加载环境变量）"""

    project_name: str = Field("servo_ai", alias="COMPOSE_PROJECT_NAME")
    # 使用default_factory动态创建实例（每次ApiConfig实例化时重新加载.env）
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    # 新增：整合Redis配置（与database字段结构一致）
    redis: RedisConfig = Field(default_factory=RedisConfig)

    model_config = SettingsConfigDict(
        env_file=".env",  # 环境变量文件路径（项目根目录下的.env）
        env_file_encoding="utf-8",  # 环境文件编码格式
        extra="allow",  # 允许未显式定义的环境变量（保留扩展性）
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
