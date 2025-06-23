import os
import json
from openai import OpenAI


def ocr_cert_info(
    image_url: str,
    api_key: str = os.getenv("DASHSCOPE_API_KEY", "sk-9ec27f85396f41788a441841e6d4a718"),
    base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    model: str = "qwen-vl-ocr-latest",
    prompt_config_path: str = "prompts/ticket_ocr_prompt.json",  
    prompt_key: str = "prompt"
) -> dict:
    """
    提取车票图像中的关键信息
    :param image_url: 车票图像URL（必选）
    :param api_key: OpenAI兼容API Key（默认从环境变量获取）
    :param base_url: API基础URL（默认使用百炼兼容模式）
    :param model: 使用的OCR模型（默认qwen-vl-ocr-latest）
    :param prompt_config_path: 提示词配置文件路径（默认使用车票OCR配置）
    :param prompt_key: 提示词在配置文件中的键名（默认使用'prompt'键）
    :return: 提取的关键信息JSON字典
    """
    prompt = load_prompt(prompt_config_path, prompt_key)
    """
    提取车票图像中的关键信息
    :param image_url: 车票图像URL
    :param api_key: OpenAI兼容API Key（默认从环境变量获取）
    :param base_url: API基础URL（默认使用百炼兼容模式）
    :param model: 使用的OCR模型（默认qwen-vl-ocr-latest）
    :param prompt: 自定义提取提示词
    :return: 提取的关键信息JSON字典
    """
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": image_url,
                            "min_pixels": 28 * 28 * 4,
                            "max_pixels": 28 * 28 * 8192
                        },
                        {"type": "text", 
                         "text": prompt
                            }
                    ]
                }
            ])

        ret = completion.choices[0].message.content
        cleaned_ret = ret.strip('```json').strip()  # 清理可能的Markdown包裹标记
        return json.loads(cleaned_ret)
    except Exception as e:
        raise RuntimeError(f"OCR提取失败: {str(e)}")


def load_prompt(prompt_config_path: str, prompt_key: str = "prompt") -> str:
    """
    加载并验证提示词配置
    :param prompt_config_path: 提示词配置文件路径
    :param prompt_key: 提示词在配置文件中的键名
    :return: 提取的提示词内容
    """
    full_prompt_path = os.path.join(os.path.dirname(__file__), prompt_config_path)
    if not os.path.exists(full_prompt_path):
        raise FileNotFoundError(f"提示词配置文件不存在: {full_prompt_path}")
    with open(full_prompt_path, 'r', encoding='utf-8') as f:
        prompt_config = json.load(f)
        if prompt_key not in prompt_config:
            raise KeyError(f"配置文件{full_prompt_path}中未找到key: {prompt_key}")
        return prompt_config[prompt_key]

if __name__ == "__main__":
    # 示例调用
    test_image_url = "https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg"  # 示例车票图片1
    test_image_url2 = "https://xuntian-pv.tcl.com/group1/M00/1A/19/rBAAOGchjDeAZli9AAFfY8v0R18553.jpg"  # 示例车票图片2
    
    try:
        # cert_info = ocr_cert_info(image_url=test_image_url, prompt_config_path="prompts/ticket_ocr_prompt.json", prompt_key="prompt")
        cert_info = ocr_cert_info(image_url=test_image_url2, prompt_config_path="prompts/cert_ocr_prompt.json", prompt_key="prompt")
        print(json.dumps(cert_info, ensure_ascii=False, indent=2))
    except RuntimeError as e:
        print(f"错误: {e}")