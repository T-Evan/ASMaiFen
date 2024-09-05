# 导包
from .特征库 import *
from ascript.android.ui import Dialog
from .tomato_ocr import tomatoOcr
from ascript.android import screen
from .res.ui.ui import switch_lock
from .res.ui.ui import switch_ocr_apk_lock
from ascript.android.system import R
from ascript.android import plug
from .res.ui.ui import TimeoutLock

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
    if TimeoutLock(switch_lock).acquire_lock():
        ocrRe = ocr.ocr_result([[x1, y1, x2, y2]])
        TimeoutLock(switch_lock).release_lock()
    else:
        print(f"ocrFind获取锁超时-{keyword}")
        return False
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
            print(f"ocrFind识别成功-{keyword}|{center_x}|{center_y}")
            return True
    print(f"ocrFind识别失败-{keyword}")
    return False


def ocrFindRange(keyword, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280, whiteList=''):
    try:
        if TimeoutLock(switch_lock).acquire_lock():
            ocrRe = ocr.ocr_result([], whiteList, x1, y1, x2, y2)
            TimeoutLock(switch_lock).release_lock()
        else:
            print(f"ocrFindRange获取锁超时-{keyword}")
            return False
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
            print(f"ocrFindRange识别成功-{keyword}|{center_x}|{center_y}")
            return True
        print(f"ocrFindRange识别失败-{keyword}|{ocrRe}")
        return False
    except Exception as e:
        print(f"ocrFindRange发生异常: {e}")
        return False

def ocrFindRangeClick(keyword, sleep1=1, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280, whiteList=''):
    try:
        if TimeoutLock(switch_lock).acquire_lock():
            ocrRe = ocr.ocr_result([], whiteList, x1, y1, x2, y2)
            TimeoutLock(switch_lock).release_lock()
        else:
            print(f"ocrFindRangeClick获取锁超时-{keyword}")
            return False
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
            print(f"ocrFindRangeClick识别成功-{keyword}|{center_x}|{center_y}")
            return True
        print(f"ocrFindRangeClick识别失败-{keyword}|{ocrRe}")
        return False
    except Exception as e:
        print(f"ocrFindRangeClick发生异常: {e}")
        return False

def ocrFindClick(keyword, sleep1=1, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280):
    try:
        if TimeoutLock(switch_lock).acquire_lock():
            ocrRe = ocr.ocr_result([[x1, y1, x2, y2]])
            TimeoutLock(switch_lock).release_lock()
        else:
            print(f"ocrFindClick获取锁超时-{keyword}")
            return False
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
            print(f"ocrFindClick识别成功-{keyword}|{center_x}|{center_y}")
            return True
        print(f"ocrFindClick识别失败-{keyword}|{ocrRe}")
        return False
    except Exception as e:
        print(f"ocrFindClick发生异常: {e}")
        return False

def CustomOcrText(x1, y1, x2, y2, keyword, whiteList=''):
    if TimeoutLock(switch_lock).acquire_lock():
        ocrRe = ocr.ocr_result([[x1, y1, x2, y2]], whiteList)
        TimeoutLock(switch_lock).release_lock()
    else:
        print(f"CustomOcrText获取锁超时-{keyword}")
        return False, ''
    ocrRe2 = [line.get('text', '') for line in ocrRe['lines']]
    ocrText = ''
    if len(ocrRe2) > 0:
        ocrText = ocrRe2[0]
    if ocrText != "" and ocrText == keyword:
        print(f"CustomOcrText-{keyword}")
        return True, ocrText
    else:
        print(f"CustomOcrText-{keyword}|{ocrRe}")
        return False, ocrText


# 范围识别
def CustomOcrTextRange(x1, y1, x2, y2, whiteList=''):
    if TimeoutLock(switch_lock).acquire_lock():
        ocrText = ocr.ocr_result([], whiteList, x1, y1, x2, y2)
        TimeoutLock(switch_lock).release_lock()
    else:
        print(f"CustomOcrTextRange获取锁超时")
        return False, ''
    # print(ocrText)
    return True, ocrText


# 速度慢、精度高、适合极小区域（单个字/数字）识别精准匹配
def TomatoOcrText(x1, y1, x2, y2, keyword):
    try:
        # 传入图片路径或者Bitmap
        # res = ocr.ocrFile(R.img("logo.png"))
        if TimeoutLock(switch_lock).acquire_lock():
            bitmap = screen.capture(x1, y1, x2, y2)
            ocrText = tomatoOcr.ocrBitmap(bitmap, 3)
            TimeoutLock(switch_lock).release_lock()
        else:
            print(f"TomatoOcrText获取锁超时")
            return False, ''
        if ocrText != "" and ocrText == keyword:
            print(f"o识别成功-{keyword}|{ocrText}")
            return True, ocrText
        else:
            # print(f"o识别失败-不匹配-{keyword}|{ocrText}")
            return False, ocrText
    except Exception as e:
        print(f"toOcr发生异常: {e}")
        return False, ''

def TomatoOcrTap(x1, y1, x2, y2, keyword, offsetX=0, offsetY=0):
    try:
        if TimeoutLock(switch_lock).acquire_lock():
            bitmap = screen.capture(x1, y1, x2, y2)
            ocrText = tomatoOcr.ocrBitmap(bitmap, 3)
            TimeoutLock(switch_lock).release_lock()
        else:
            print(f"TomatoOcrTap获取锁超时")
            return False
        # 所有识别运行完成后，可释放插件
        # tomatoOcr.end()
        if ocrText != "" and ocrText == keyword:
            tapSleep(x1 + offsetX, y1 + offsetY)
            print(f"o识别成功-{keyword}|{ocrText}|{x1}|{y1}")
            return True
        else:
            print(f"o识别失败-不匹配-{keyword}|{ocrText}")
            return False
    except Exception as e:
        print(f"toOcrTap发生异常: {e}")
        return False

def Toast(content, tim=1000):
    print(f"提示-{content}")
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