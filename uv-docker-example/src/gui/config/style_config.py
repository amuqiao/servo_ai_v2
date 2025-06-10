from ttkbootstrap import Style
from typing import Literal

# GUI主题配置（ttkbootstrap支持的主题）
THEME: Literal['flatly', 'darkly', 'litera'] = 'flatly'

def init_style() -> Style:
    """初始化ttkbootstrap样式"""
    return Style(theme=THEME)