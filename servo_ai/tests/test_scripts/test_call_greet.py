import pytest
from scripts.call_greet import main
from unittest.mock import patch
import sys

def test_call_greet_output(capsys):
    """测试call_greet.py能否正确调用generate_greeting并输出"""
    # 修正patch路径：针对call_greet模块内导入的generate_greeting
    with patch("scripts.call_greet.generate_greeting") as mock_greet:
        # 模拟generate_greeting返回固定值
        mock_greet.return_value = "测试问候语"
        # 调用主逻辑
        main()
        # 捕获输出并验证
        captured = capsys.readouterr()
        assert "调用 greet_generator 生成的问候语： 测试问候语" in captured.out, "输出未包含预期问候语"