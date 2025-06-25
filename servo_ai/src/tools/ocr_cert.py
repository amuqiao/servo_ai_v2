import os
import json
import base64
from openai import OpenAI
from typing import Union, IO, Dict, Any

class OCRCertInfoExtractor:
    """
    证件OCR信息提取器，支持从URL或本地文件提取证件信息
    """
    
    def __init__(self, 
                 api_key: str = os.getenv("DASHSCOPE_API_KEY", "sk-9ec27f85396f41788a441841e6d4a718"),
                 base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1",
                 model: str = "qwen-vl-ocr-latest",
                 prompt_config_path: str = "prompts/cert_ocr_prompt.json",
                 prompt_key: str = "prompt"):
        """
        初始化OCR提取器
        
        :param api_key: OpenAI兼容API Key
        :param base_url: API基础URL
        :param model: 使用的OCR模型
        :param prompt_config_path: 提示词配置文件路径
        :param prompt_key: 提示词在配置文件中的键名
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.prompt_config_path = prompt_config_path
        self.prompt_key = prompt_key
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.prompt = self._load_prompt()
    
    def _load_prompt(self) -> str:
        """加载并验证提示词配置"""
        full_prompt_path = os.path.join(os.path.dirname(__file__), self.prompt_config_path)
        if not os.path.exists(full_prompt_path):
            raise FileNotFoundError(f"提示词配置文件不存在: {full_prompt_path}")
        with open(full_prompt_path, 'r', encoding='utf-8') as f:
            prompt_config = json.load(f)
            if self.prompt_key not in prompt_config:
                raise KeyError(f"配置文件{full_prompt_path}中未找到key: {self.prompt_key}")
            return prompt_config[self.prompt_key]
    
    def _encode_image(self, image_source: Union[str, IO]) -> str:
        """
        将图像文件（路径或文件流）编码为base64字符串
        
        :param image_source: 图像文件路径或文件流对象
        :return: base64编码字符串
        """
        if isinstance(image_source, str):
            # 处理文件路径
            with open(image_source, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        else:
            # 处理文件流
            return base64.b64encode(image_source.read()).decode("utf-8")
    
    def _parse_response(self, response_content: str) -> Dict[str, Any]:
        """
        解析API响应内容，提取JSON数据
        
        :param response_content: API返回的原始内容
        :return: 解析后的JSON字典
        """
        cleaned_response = response_content.strip('```json').strip()
        return json.loads(cleaned_response)
    
    def from_url(self, image_url: str) -> Dict[str, Any]:
        """
        从图像URL提取证件信息
        
        :param image_url: 图像URL
        :return: 提取的关键信息
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
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
                            {"type": "text", "text": self.prompt}
                        ]
                    }
                ])
            
            return self._parse_response(completion.choices[0].message.content)
        except Exception as e:
            raise RuntimeError(f"OCR提取失败: {str(e)}")
    
    def from_file(self, image_source: Union[str, IO], image_format: str = "jpeg") -> Dict[str, Any]:
        """
        从本地图像文件提取证件信息
        
        :param image_source: 图像文件路径或文件流对象
        :param image_format: 图像格式
        :return: 提取的关键信息
        """
        try:
            base64_image = self._encode_image(image_source)
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{image_format};base64,{base64_image}"
                                },
                                "min_pixels": 28 * 28 * 4,
                                "max_pixels": 28 * 28 * 8192
                            },
                            {"type": "text", "text": self.prompt}
                        ]
                    }
                ])
            
            return self._parse_response(completion.choices[0].message.content)
        except Exception as e:
            raise RuntimeError(f"OCR提取失败: {str(e)}")


if __name__ == "__main__":
    # 初始化OCR提取器
    extractor = OCRCertInfoExtractor()
    
    # URL测试用例
    test_image_url = "https://xuntian-pv.tcl.com/group1/M00/1A/19/rBAAOGchjDeAZli9AAFfY8v0R18553.jpg"
    try:
        url_result = extractor.from_url(image_url=test_image_url)
        print("URL测试结果:", json.dumps(url_result, ensure_ascii=False, indent=2))
    except RuntimeError as e:
        print(f"URL测试错误: {e}")

    # 文件路径测试用例
    test_file_path = "/Users/wangqiao/Downloads/github_project/servo_ai_v2_project/servo_ai_v2/uv-docker-example/src/tools/output/pdf_1/page_1.png"  # 替换为实际文件路径
    try:
        file_path_result = extractor.from_file(image_source=test_file_path)
        print("文件路径测试结果:", json.dumps(file_path_result, ensure_ascii=False, indent=2))
    except RuntimeError as e:
        print(f"文件路径测试错误: {e}")

    # 文件流测试用例
    try:
        with open(test_file_path, "rb") as f:
            file_stream_result = extractor.from_file(image_source=f)
            print("文件流测试结果:", json.dumps(file_stream_result, ensure_ascii=False, indent=2))
    except RuntimeError as e:
        print(f"文件流测试错误: {e}")
    except FileNotFoundError:
        print(f"文件流测试错误: 文件{test_file_path}不存在")    