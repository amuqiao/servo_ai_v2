from pathlib import Path
import sys

# 添加项目根目录到Python路径
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
from src.scripts.greet_generator import generate_greeting

def main():
    # 调用 greet_generator.py 中的函数并输出结果
    greeting = generate_greeting()
    print("调用 greet_generator 生成的问候语：", greeting)

if __name__ == "__main__":
    main()  # 仅保留入口调用
