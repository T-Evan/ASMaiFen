# 导包
from .特征库 import *
from ascript.android.ui import Dialog
from .tomato_ocr import tomatoOcr
from ascript.android import screen
from .res.ui.ui import switch_lock
from ascript.android.system import R
from ascript.android import plug

plug.load("BDS_OcrText")
from BDS_OcrText import *

# # 导入http模块
# import requests
#
# # 指定下载文件的地址
# url = 'https://www.baidu.com/img/flexible/logo/pc/result@2.png' # 目标下载链接
# # 通过get获取数据
# r = requests.get(url)
#
# # 保存文件至sd卡下的1.png
# with open (R.res("/OcrText.apk"), 'wb') as f:
#     f.write(r.content)

ocr = BDS_OcrText('rcgd5ncvb5ywtge2mzqqzte6kcf9qbyt', R.res("/OcrText.apk"), 2)
def ocrFind(keyword, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280):
    ocrRe = ocr.ocr_result([[x1, y1, x2, y2]])
    center_x = 0
    center_y = 0
    # 遍历 data['lines'] 列表
    for line in ocrRe['lines']:
        # 检查每行的 text 是否等于 '4'
        if line['text'] == keyword:
            box = line['box']
            x1, y1, x2, y2 = box
            # 计算中心位置
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            print(f"o识别成功-{keyword}|{center_x}|{center_y}")
            return True
    print(f"o识别失败-{keyword}")
    return False

def ocrFindRange(keyword, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280):
    ocrRe = ocr.ocr_result([], '', x1, y1, x2, y2)
    print(ocrRe)
    center_x = 0
    center_y = 0
    # 遍历 data['lines'] 列表
    for line in ocrRe['lines']:
        # 检查每行的 text 是否等于 '4'
        if line['text'] == keyword:
            box = line['box']
            rx1, ry1, rx2, ry2 = box
            # 计算中心位置
            center_x = (rx1 + rx2) / 2
            center_y = (ry1 + ry2) / 2
    if center_x > 0 and center_y > 0:
        return True
    return False

def ocrFindRangeClick(keyword, sleep1=1, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280,whiteList=''):
    ocrRe = ocr.ocr_result([], whiteList, x1, y1, x2, y2)
    print(ocrRe)
    center_x = 0
    center_y = 0
    # 遍历 data['lines'] 列表
    for line in ocrRe['lines']:
        # 检查每行的 text 是否等于 '4'
        if line['text'] == keyword:
            box = line['box']
            rx1, ry1, rx2, ry2 = box
            # 计算中心位置
            center_x = (rx1 + rx2) / 2
            center_y = (ry1 + ry2) / 2
    if center_x > 0 and center_y > 0:
        tapSleep(center_x + x1, center_y + y1)
        sleep(sleep1)
        return True
    return False

def ocrFindClick(keyword, sleep1=1, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280):
    ocrRe = ocr.ocr_result([[x1, y1, x2, y2]])
    # print(ocrRe)
    center_x = 0
    center_y = 0
    # 遍历 data['lines'] 列表
    for line in ocrRe['lines']:
        # 检查每行的 text 是否等于 '4'
        if line['text'] == keyword:
            box = line['box']
            x1, y1, x2, y2 = box
            # 计算中心位置
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
    if center_x > 0 and center_y > 0:
        tapSleep(center_x, center_y)
        sleep(sleep1)
        return True
    return False


def CustomOcrText(x1, y1, x2, y2, keyword, whiteList=''):
    ocrRe = ocr.ocr_result([[x1, y1, x2, y2]], whiteList)
    ocrRe2 = [line.get('text', '') for line in ocrRe['lines']]
    ocrText = ''
    if len(ocrRe2) > 0:
        ocrText = ocrRe2[0]
    if ocrText != "" and ocrText == keyword:
        print(f"o识别成功-{keyword}|{ocrText}")
        return True, ocrText
    else:
        # print(f"o识别失败-不匹配-{keyword}|{ocrText}")
        return False, ocrText


# 范围识别
def CustomOcrTextRange(x1, y1, x2, y2, whiteList=''):
    ocrText = ocr.ocr_result([], whiteList, x1, y1, x2, y2)
    # print(ocrText)
    return True, ocrText


# 速度慢、精度高、适合极小区域（单个字/数字）识别精准匹配
def TomatoOcrText(x1, y1, x2, y2, keyword):

    # 传入图片路径或者Bitmap
    # res = ocr.ocrFile(R.img("logo.png"))
    bitmap = screen.capture(x1, y1, x2, y2)
    with switch_lock:
        ocrText = tomatoOcr.ocrBitmap(bitmap, 3)

    if ocrText != "" and ocrText == keyword:
        print(f"o识别成功-{keyword}|{ocrText}")
        return True, ocrText
    else:
        # print(f"o识别失败-不匹配-{keyword}|{ocrText}")
        return False, ocrText

def TomatoOcrTap(x1, y1, x2, y2, keyword, offsetX=0, offsetY=0):
    bitmap = screen.capture(x1, y1, x2, y2)
    with switch_lock:
        ocrText = tomatoOcr.ocrBitmap(bitmap, 3)
    # 所有识别运行完成后，可释放插件
    # tomatoOcr.end()
    if ocrText != "" and ocrText == keyword:
        tapSleep(x1 + offsetX, y1 + offsetY)
        print(f"o识别成功-{keyword}|{ocrText}|{x1}|{y1}")
        return True
    else:
        print(f"o识别失败-不匹配-{keyword}|{ocrText}")
        return False


def Toast(content, tim=1000):
    Dialog.toast(content, tim, 3 | 48, 200, 0)


def tapSleep(x, y, ms=1.7):
    click(x, y)
    sleep(ms)


def safe_int(value):
    """
    尝试将给定的值转换为整数，如果失败则返回默认值 0。
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return ""
