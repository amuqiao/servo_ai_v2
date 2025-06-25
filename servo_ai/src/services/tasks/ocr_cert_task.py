import logging
from typing import Dict, Any
from src.tools.pdf2image import PdfToImageConverter
from src.tools.ocr_cert import OCRCertInfoExtractor
from io import BytesIO
from src.services.tasks.base_task import BaseTask

# 初始化任务专用日志器
logger = logging.getLogger("celery")

class OCRCertTask(BaseTask):
    task_type = "ocr_cert"

    def __init__(self, task_id: str, content: Dict[str, Any]):
        super().__init__(task_id, content)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OCRCertTask':
        return cls(
            task_id=data["task_id"],
            content=data["content"]
        )

    def parse_content(self) -> Dict[str, Any]:
        # 解析逻辑实现
        return self.content

    def pdf_urls_to_ocr_results(self, pdf_urls: list, scale_factor: float = 2.0, workers: int = 2):
        """
        从 PDF URL 列表获取 OCR 识别结果

        :param pdf_urls: PDF 文件 URL 列表
        :param scale_factor: 缩放倍数，默认为初始化时的设置
        :param workers: 并行工作线程数，默认为初始化时的设置
        :return: OCR 识别结果的字典列表
        """
        # 初始化 PDF 转图片转换器
        pdf_converter = PdfToImageConverter(scale_factor=scale_factor, workers=workers)
        # 初始化 OCR 信息提取器
        ocr_extractor = OCRCertInfoExtractor()

        # 将 PDF URL 列表转换为图片文件流列表
        image_streams = pdf_converter.urls_to_image_streams(pdf_urls, scale_factor, workers)

        ocr_results = []
        # 对每个图片文件流进行 OCR 识别
        for image_stream in image_streams:
            try:
                # 将字节流转换为文件流对象
                with BytesIO(image_stream) as img_buffer:
                    # 进行 OCR 识别
                    result = ocr_extractor.from_file(img_buffer)
                ocr_results.append(result)
            except Exception as e:
                print(f"OCR 识别出错: {str(e)}")

        return ocr_results

    def process(self) -> Dict[str, Any]:
        # 添加任务处理日志
        logger.info(f"开始处理通知任务，ID: {self.task_id}，内容: {self.content}")

        # 假设 content 中有 pdf_urls 字段
        pdf_urls = self.content.get("pdf_urls", [])
        ocr_results = self.pdf_urls_to_ocr_results(pdf_urls)

        # 实际业务处理逻辑
        processed_result = {"status": "notified", "content": self.content, "ocr_results": ocr_results}

        # 添加处理结果日志
        logger.info(f"通知任务处理完成，ID: {self.task_id}")

        return {
            "status": "success",
            "task_id": self.task_id,
            "result": processed_result
        }