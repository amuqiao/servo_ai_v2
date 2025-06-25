import pytest
from src.scripts.greet_generator import generate_greeting
from datetime import datetime
import re

def test_generate_greeting_time_template(monkeypatch):
    # 强制选择"时间"模板
    monkeypatch.setattr("random.choice", lambda x: "欢迎使用本脚本，当前时间是：")
    result = generate_greeting()
    # 验证时间格式（YYYY-MM-DD HH:MM:SS）
    assert re.match(r"欢迎使用本脚本，当前时间是：\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", result), "时间格式不符合要求"

def test_generate_greeting_luck_template(monkeypatch):
    # 强制选择"运气"模板
    monkeypatch.setattr("random.choice", lambda x: "今天的运气指数：")
    result = generate_greeting()
    # 验证随机数范围（1-100%）
    assert re.match(r"今天的运气指数：\d{1,2}%|100%", result), "运气值格式不符合要求"
    luck_num = int(result.split("：")[1].replace("%", ""))
    assert 1 <= luck_num <= 100, "运气值超出1-100范围"

def test_generate_greeting_normal_template(monkeypatch):
    # 强制选择普通模板
    monkeypatch.setattr("random.choice", lambda x: "你好，今天是美好的一天！")
    result = generate_greeting()
    assert result == "你好，今天是美好的一天！", "普通模板返回值错误"