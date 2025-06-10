import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # api_key=os.getenv("DASHSCOPE_API_KEY"),
    # api_key="sk-a70ae9824ef44adba9b201126d743014",
    api_key="sk-9ec27f85396f41788a441841e6d4a718",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-vl-ocr-latest",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    # "image_url": "https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg",
                    "image_url": "https://xuntian-pv.tcl.com/group1/M00/5E/1B/rBAAOGg4P6SABizqAAXiFV_wwKU981.pdf",
                    # 输入图像的最小像素阈值，小于该值图像会按原比例放大，直到总像素大于min_pixels
                    "min_pixels": 28 * 28 * 4,
                    # 输入图像的最大像素阈值，超过该值图像会按原比例缩小，直到总像素低于max_pixels
                    "max_pixels": 28 * 28 * 8192
                },
                  # qwen-vl-ocr-latest支持在以下text字段中传入Prompt，若未传入，则会使用默认的Prompt：Please output only the text content from the image without any additional descriptions or formatting.
                 # 如调用qwen-vl-ocr-1028，模型会使用固定Prompt：Read all the text in the image.不支持用户在text中传入自定义Prompt
                {"type": "text",
                 "text": "请提取车票图像中的发票号码、车次、起始站、终点站、发车日期和时间点、座位号、席别类型、票价、身份证号码、购票人姓名。要求准确无误的提取上述关键信息、不要遗漏和捏造虚假信息，模糊或者强光遮挡的单个文字可以用英文问号?代替。返回数据格式以json方式输出，格式为：{'发票号码'：'xxx', '车次'：'xxx', '起始站'：'xxx', '终点站'：'xxx', '发车日期和时间点'：'xxx', '座位号'：'xxx', '席别类型'：'xxx','票价':'xxx', '身份证号码'：'xxx', '购票人姓名'：'xxx'"},
            ]
        }
    ])

print(completion.choices[0].message.content)