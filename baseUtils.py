# 导包
from .特征库 import *
from ascript.android.ui import Dialog
from .tomato_ocr import tomatoOcr
from ascript.android import screen
from .res.ui.ui import switch_lock

# 速度慢、精度高、适合极小区域（单个字/数字）识别精准匹配
def TomatoOcrText(x1, y1, x2, y2, keyword):

    # 传入图片路径或者Bitmap
    # res = ocr.ocrFile(R.img("logo.png"))
    bitmap = screen.capture(x1, y1, x2, y2)
    with switch_lock:
        ocrText = tomatoOcr.ocrBitmap(bitmap, 3)

    # 所有识别运行完成后，可释放插件
    # tomatoOcr.end()
    if ocrText != "" and ocrText == keyword:
        log.info(f"o识别成功-{keyword}|{ocrText}")
        return True, ocrText
    else:
        # log.info(f"o识别失败-不匹配-{keyword}|{ocrText}")
        return False, ocrText

def TomatoOcrTap(x1, y1, x2, y2, keyword, offsetX=0, offsetY=0):
    bitmap = screen.capture(x1, y1, x2, y2)
    with switch_lock:
        ocrText = tomatoOcr.ocrBitmap(bitmap, 3)

    # 所有识别运行完成后，可释放插件
    # tomatoOcr.end()
    if ocrText != "" and ocrText == keyword:
        tapSleep(x1 + offsetX, y1 + offsetY)
        log.info(f"o识别成功-{keyword}|{ocrText}")
        return True
    else:
        # log.info(f"o识别失败-不匹配-{keyword}|{ocrText}")
        return False

# 速度快、精度低、适合全屏识别模糊匹配
def OCRText(x1, y1, x2, y2, keyword):
    ocrText = ldE.ocr_mlkit_v2(rect=[x1, y1, x2, y2])
    if ocrText != "" and ocrText == keyword:
        log.info(f"o识别成功-{keyword}|{ocrText}")
        return True, ocrText
    else:
        log.info(f"o识别失败-不匹配-{keyword}|{ocrText}")
        return False, ocrText

# 速度慢、精度高、适合区域识别精准匹配
def OCRTextV2(x1, y1, x2, y2, keyword):
    ocrText = ldE.ocr_paddleocr_v3(rect=[x1, y1, x2, y2])
    if ocrText != "" and ocrText == keyword:
        log.info(f"o识别成功-{keyword}|{ocrText}")
        return True, ocrText
    else:
        log.info(f"o识别失败-不匹配-{keyword}|{ocrText}")
        return False, ocrText


def OCRTap(x1, y1, x2, y2, keyword, offsetX=0, offsetY=0):
    ocrText = ldE.ocr_mlkit_v2(rect=[x1, y1, x2, y2])
    if ocrText != "" and ocrText == keyword:
        log.info(f"o识别成功-{keyword}|{ocrText}")
        tapSleep(x1 + offsetX, y1 + offsetY)
        return True
    else:
        log.info(f"o识别失败-不匹配-{keyword}|{ocrText}")
        return False


def OCRTapV2(x1, y1, x2, y2, keyword, offsetX=0, offsetY=0):
    ocrText = ldE.ocr_paddleocr_v3(rect=[x1, y1, x2, y2])
    if ocrText != "" and ocrText == keyword:
        log.info(f"o识别成功-{keyword}|{ocrText}")
        tapSleep(x1 + offsetX, y1 + offsetY)
        return True
    else:
        log.info(f"o识别失败-不匹配-{keyword}|{ocrText}")
        return False


def Toast(content, tim=1000):
    Dialog.toast(content, tim, 3 | 48, 200, 0)


def tapSleep(x, y, ms=1.7):
    ldE.click(x, y)
    ldE.sleep(ms)


def safe_int(value):
    """
    尝试将给定的值转换为整数，如果失败则返回默认值 0。
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return ""
