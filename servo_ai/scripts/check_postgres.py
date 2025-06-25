import os
import psycopg
from psycopg import OperationalError
import traceback  # 新增：打印完整堆栈

def check_postgres_connection():
    db_config = {
        "host": "localhost",
        "port": 5432,
        "user": "postgres",
        "password": "123456",
        "dbname": "iot_platform",
        "options": "-c client_encoding=UTF8"
    }

    print("===== 调试：当前连接参数的字节编码 =====")
    for key, value in db_config.items():
        if isinstance(value, str):
            print(f"{key}: {value} (UTF-8字节: {value.encode('utf-8')})")
        else:
            print(f"{key}: {value}")
    print("=====================================")

    try:
        conn = psycopg.connect(**db_config)
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"PostgreSQL连接成功！版本信息：{version}")
        conn.close()
        return True
    except OperationalError as e:
        # 打印完整异常堆栈（关键优化）
        print(f"PostgreSQL连接失败：{str(e)}")
        traceback.print_exc()  # 新增：输出详细错误堆栈
        return False

if __name__ == "__main__":
    # python e:/github_project/servo_ai_v2_project/servo_ai_v2/uv-docker-example/scripts/check_postgres.py
    check_postgres_connection()