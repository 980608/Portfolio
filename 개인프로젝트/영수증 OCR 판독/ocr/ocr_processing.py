import cv2
from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang="korean",
    use_angle_cls=False,
    show_log=False   # 🔥 로그 제거
)

def run_ocr(img):
    result = ocr.ocr(img, cls=False)[0]

    ocr_text = []

    for item in result:
        text = item[1][0]
        ocr_text.append(text)

    return {
        "raw_result": result,
        "ocr_text": "\n".join(ocr_text)
    }



















