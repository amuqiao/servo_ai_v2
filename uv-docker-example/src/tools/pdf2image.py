import fitz  # PyMuPDF
import requests
import os
from pathlib import Path

def pdf_local_to_images(pdf_path: str, output_dir: str = "output") -> list:
    """
    本地PDF文件转图片
    :param pdf_path: 本地PDF文件路径
    :param output_dir: 输出图片目录
    :return: 生成的图片路径列表
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")

    doc = fitz.open(pdf_path)
    image_paths = []

    # 将输出目录转换为绝对路径
    output_dir = os.path.abspath(output_dir)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # 设置2倍缩放矩阵提高清晰度（可根据需要调整缩放因子）
        matrix = fitz.Matrix(2, 2)  # 水平和垂直各放大2倍
        pix = page.get_pixmap(matrix=matrix)
        image_path = os.path.join(output_dir, f"page_{page_num+1}.png")
        pix.save(image_path)
        image_paths.append(image_path)

    doc.close()
    return image_paths

def pdf_url_to_images(pdf_url: str, output_dir: str = "output") -> list:
    """
    PDF URL转图片
    :param pdf_url: PDF文件URL
    :param output_dir: 输出图片目录
    :return: 生成的图片路径列表
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        response = requests.get(pdf_url, headers=headers, stream=True, timeout=10)
        response.raise_for_status()  # 自动检查HTTP错误状态码
    except requests.exceptions.ConnectionError:
        raise RuntimeError("连接失败，请检查URL或网络连接")
    except requests.exceptions.Timeout:
        raise RuntimeError("请求超时，请检查网络或尝试延长超时时间")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"HTTP请求错误: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"下载PDF时发生未知错误: {str(e)}")

    # 临时保存PDF内容
    temp_pdf = Path("temp_pdf.pdf")
    with open(temp_pdf, "wb") as f:
        f.write(response.content)

    try:
        return pdf_local_to_images(str(temp_pdf), output_dir)
    finally:
        if temp_pdf.exists():
            temp_pdf.unlink()

def pdf_urls_to_images(pdf_urls: list, output_dir: str = "output") -> list:
    """
    批量处理多个PDF URL转图片（顺序执行）
    :param pdf_urls: PDF文件URL列表
    :param output_dir: 输出图片根目录
    :return: 生成的所有图片路径列表（按URL顺序排列）
    """
    all_image_paths = []
    for idx, url in enumerate(pdf_urls):
        # 为每个URL创建独立子目录避免文件名冲突
        url_output_dir = os.path.join(output_dir, f"pdf_{idx+1}")
        Path(url_output_dir).mkdir(parents=True, exist_ok=True)
        try:
            image_paths = pdf_url_to_images(url, url_output_dir)
            all_image_paths.extend(image_paths)
        except Exception as e:
            print(f"处理URL {url} 时出错: {str(e)}")
    return all_image_paths


def pdf_urls_to_images_parallel(pdf_urls: list, output_dir: str = "output", workers: int = 4) -> list:
    """
    批量处理多个PDF URL转图片（并行执行）
    :param pdf_urls: PDF文件URL列表
    :param output_dir: 输出图片根目录
    :param workers: 并行工作线程数
    :return: 生成的所有图片路径列表
    """
    from concurrent.futures import ThreadPoolExecutor
    all_image_paths = []

    def process_url(url, idx):
        url_output_dir = os.path.join(output_dir, f"pdf_{idx+1}")
        Path(url_output_dir).mkdir(parents=True, exist_ok=True)
        try:
            return pdf_url_to_images(url, url_output_dir)
        except Exception as e:
            print(f"处理URL {url} 时出错: {str(e)}")
            return []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(process_url, url, idx) for idx, url in enumerate(pdf_urls)]
        for future in futures:
            all_image_paths.extend(future.result())

    return all_image_paths


if __name__ == "__main__":
    # 示例：本地PDF转换
    # local_pdf_path = "test.pdf"  # 替换为实际本地PDF路径
    # print("本地PDF转换结果:", pdf_local_to_images(local_pdf_path))

    # 示例：URL PDF转换
    pdf_url = "https://xuntian-pv.tcl.com/group1/M00/5E/1B/rBAAOGg4P6SABizqAAXiFV_wwKU981.pdf"  # 替换为实际PDF URL
    pdf_urls = [
        "https://xuntian-pv.tcl.com/group1/M00/2C/72/rBAAOGdzuwGATMSIAAJAsZYWXKI601.pdf",
        "https://xuntian-pv.tcl.com/group1/M00/2C/64/rBAAOGdzkjmAeKrxAAJAsZYWXKI702.pdf",
        "https://xuntian-pv.tcl.com/group1/M00/2C/DE/rBAAOGd3jNCAZvetAAJAsZYWXKI229.pdf",
        "https://xuntian-pv.tcl.com/group1/M00/2C/45/rBAAOGdyexSAeFajAAJAsZYWXKI485.pdf"
    ]
    
    # print("URL PDF转换结果:", pdf_url_to_images(pdf_url))
    print("URLs PDF转换结果:", pdf_urls_to_images(pdf_urls))
    # print("并行URLs PDF转换结果:", pdf_urls_to_images_parallel(pdf_urls))
    
    
    
    