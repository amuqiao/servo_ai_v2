import datetime
import random

def generate_greeting() -> str:
    """生成随机问候语（仅依赖标准库）"""
    greetings = [
        "你好，今天是美好的一天！",
        "欢迎使用本脚本，当前时间是：",
        "今天的运气指数：",
        "祝您工作顺利，当前时间为："
    ]
    # 随机选择问候语模板
    selected = random.choice(greetings)
    # 添加时间或随机数增强随机性
    if "时间" in selected:
        return f"{selected}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    elif "运气" in selected:
        return f"{selected}{random.randint(1, 100)}%"
    else:
        return selected

if __name__ == "__main__":
    # 直接运行时输出问候语
    print(generate_greeting())