# 导包
from time import sleep

from ascript.android import system
from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .baseUtils import *
# 导包
from ascript.android.screen import FindImages
# 导入上下文环境包,方便导入图片地址
from ascript.android.system import R


# 实例方法
def main():
    while True:
        功能开关['bossColor'] = ''
        功能开关['bossLastColor'] = ''
        功能开关['bossNumber0'] = ''
        功能开关['bossNumber1'] = ''
        功能开关['bossNumber2'] = ''
        功能开关['bossLastNumber0'] = ''
        功能开关['bossLastNumber1'] = ''
        功能开关['bossLastNumber2'] = ''
        if 功能开关["大暴走开关"] == 1 and 功能开关["史莱姆选择"] == "暴走烈焰大王":
            elapsed = 0
            while 1:
                if 功能开关["fighting"] == 1:
                    # 检测战斗状态
                    # 异步识别boss状态
                    daBaoZouLieYanBoss(elapsed)
                else:
                    ldE.sleep(3)
                elapsed = elapsed + 5

def daBaoZouLieYanBoss(elapsed):
    功能开关['bossColor'] = ''
    功能开关['bossNumber0'] = ''
    功能开关['bossNumber1'] = ''
    功能开关['bossNumber2'] = ''

    # 匹配中间数字的颜色
    # 进入二阶段（左右数字）后，无需识别颜色
    if 功能开关['bossLastNumber1'] == '' and 功能开关['bossLastNumber2'] == '' and elapsed <  120:
        re1 = ldE.element_exist('暴走-烈焰-橙色')
        if re1:
            功能开关['bossColor'] = "橙"
        re2 = ldE.element_exist('暴走-烈焰-紫色')
        if re2:
            功能开关['bossColor'] = "紫"
        if not re2:
            re2 = ldE.element_exist('暴走-烈焰-紫色2')
            if re2:
                功能开关['bossColor'] = "紫"
        if not re1 and not re2:
            # boss状态刷新
            功能开关['bossLastNumber0'] = ''
            功能开关['bossLastColor'] = ''

    中间数字 = ''
    左1数字 = ''
    右1数字 = ''
    for i in range(1, 6):
        if 功能开关['bossColor'] != '':  # 优先识别中间颜色
            res, 中间数字 = TomatoOcrText(333, 337, 380, 397, "中间数字")
            if 中间数字 == '':
                res, 中间数字 = TomatoOcrText(344, 344, 377, 391, "中间数字")
                if 中间数字 == '':
                    res, 中间数字 = TomatoOcrText(345, 347, 375, 396, "中间数字")
                    if 中间数字 == '':
                        res, 中间数字 = TomatoOcrText(339,339,380,397, "中间数字")

        # if 中间数字 != '':
        #     中间数字 = safe_int(中间数字)
        # if 中间数字 != '':
        #     path = R.res("/img/黄-" + str(中间数字) + ".png")
        #     res = FindImages.find_template(path,rect=[331, 337, 386, 394],confidence=0.8)
        #     if res:
        #         功能开关['bossColor'] = "橙"
        #     if not res:
        #         path = R.res("/img/紫-" + str(中间数字) + ".png")
        #         res = FindImages.find_template(path,rect=[331, 337, 386, 394],confidence=0.8)
        #         if res:
        #             功能开关['bossColor'] = "紫"
        #         if not res:
        #             # ocr + 图片均满足时
        #             中间数字 = ''

        if 中间数字 == '':
            res, 左1数字 = TomatoOcrText(281, 344, 320, 394, "左1数字")
            if 左1数字 == '':
                res, 左1数字 = TomatoOcrText(273, 333, 331, 397, "左1数字")
                if 左1数字 == '':
                    res, 左1数字 = TomatoOcrText(345, 347, 375, 396, "左1数字")

            if 左1数字 != '':
                for i in range(1, 3):
                    res, 右1数字 = TomatoOcrText(401, 345, 438, 392, "右1数字")
                    if 右1数字 == '':
                        res, 右1数字 = TomatoOcrText(393, 337, 446, 400, "右1数字")
                        if 右1数字 == '':
                            res, 右1数字 = TomatoOcrText(345, 347, 375, 396, "右1数字")
                    if 右1数字 != '':
                        break
        if 中间数字 != '' or (左1数字 != '' and 右1数字 != ''):
            break

    if 中间数字 != '':
        功能开关['bossNumber0'] = safe_int(中间数字)
        if 功能开关['bossNumber0'] == '':
            功能开关['bossNumber0'] = 0
    if 左1数字 != '':
        功能开关['bossNumber1'] = safe_int(左1数字)
        if 功能开关['bossNumber1'] == '':
            功能开关['bossNumber1'] = 0
    if 右1数字 != '':
        功能开关['bossNumber2'] = safe_int(右1数字)
        if 功能开关['bossNumber2'] == '':
            功能开关['bossNumber2'] = 0
    if 左1数字 == '' and 右1数字 == '':
        功能开关['bossLastNumber1'] = ''
        功能开关['bossLastNumber2'] = ''

    print(功能开关['bossColor'], 功能开关['bossNumber0'], 功能开关['bossNumber1'], 功能开关['bossNumber2'])

    if 功能开关['bossNumber0'] != '' or 功能开关['bossNumber1'] != '' or 功能开关['bossNumber2'] != '':
        sleep(1)
