from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class DatabaseConfig(BaseSettings):
    """数据库模块配置（映射.env中DB_前缀的环境变量）"""

    host: str = Field("localhost", alias="DB_HOST")
    port: int = Field(3306, alias="DB_PORT")
    user: str = Field("root", alias="DB_USER")
    password: str = Field("root", alias="DB_PASSWORD")
    db_name: str = Field("servo_ai", alias="DB_NAME")


class ApiConfig(BaseSettings):
    """项目全局配置类（整合各模块配置，从.env文件加载环境变量）"""

    project_name: str = Field("servo_ai", alias="COMPOSE_PROJECT_NAME")
    # 使用default_factory动态创建实例（每次ApiConfig实例化时重新加载.env）
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)

    model_config = SettingsConfigDict(
        env_file=".env",          # 环境变量文件路径（项目根目录下的.env）
        env_file_encoding="utf-8", # 环境文件编码格式
        extra="allow"             # 允许未显式定义的环境变量（保留扩展性）
    )


def get_config() -> ApiConfig:
    """依赖项：返回全局配置实例（每次调用生成新实例）"""
    return ApiConfig()


if __name__ == "__main__":
    # 测试配置加载（验证是否正确读取.env中的最新值）
    config = ApiConfig()
    print(f"项目名称: {config.project_name}")
    print(f"数据库主机: {config.database.host}")  # 预期输出.env中的DB_HOST值
