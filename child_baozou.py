# 导包
from time import sleep
from collections import Counter
from ascript.android import system
from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .baseUtils import *
# 导包
from ascript.android.screen import FindImages
# 导入上下文环境包,方便导入图片地址
from ascript.android.system import R
from ascript.android.screen import FindColors
from ascript.android.screen import YoLov5

yolo = ''


# 实例方法
def main():
    功能开关['bossColor'] = ''
    功能开关['bossColor1'] = ''
    功能开关['bossColor2'] = ''
    功能开关['bossLastColor'] = ''
    功能开关['bossLastColor1'] = ''
    功能开关['bossLastColor2'] = ''
    功能开关['bossNumber0'] = ''
    功能开关['bossNumber1'] = ''
    功能开关['bossNumber2'] = ''
    功能开关['bossLastNumber0'] = ''
    功能开关['bossLastNumber1'] = ''
    功能开关['bossLastNumber2'] = ''
    功能开关['当前职业'] = ''
    while True:
        if 功能开关["大暴走开关"] == 1 and 功能开关["史莱姆选择"] == "暴走烈焰大王":
            global yolo
            yolo = YoLov5("麦芬-火焰大暴走:0.4")
            # print(R.res("/yolo_baozou_lieyan/"))
            # yolo = YoLov5(path=R.res("/yolo_baozou_lieyan/"))

            # while 1:
            #     ts = yolo.find_all()
            #     for r in ts:
            #         print(r)
            #     sleep(0.5)

            while 1:
                if 功能开关["fighting"] == 1:
                    # 检测战斗状态
                    # 异步识别boss状态
                    daBaoZouLieYanBoss()
                else:
                    sleep(3)
        elif 功能开关["大暴走开关"] == 1 and 功能开关["史莱姆选择"] == "暴走水波大王":
            # yolo = YoLov5("麦芬-水波大暴走:0.1")
            # while 1:
            #     ts = yolo.find_all()
            #     for r in ts:
            #         print(r)
            #     sleep(0.5)

            while 1:
                if 功能开关["fighting"] == 1:
                    # 检测战斗状态
                    # 异步识别boss状态
                    daBaoZouShuiBoBoss()
                else:
                    sleep(3)
        else:
            break


def daBaoZouShuiBoBoss():
    功能开关['bossColor'] = ''
    功能开关['bossColor1'] = ''
    功能开关['bossColor2'] = ''

    # 进入二阶段后，识别基础和目标颜色
    bossColor = ''
    bossColor1 = ''
    bossColor2 = ''

    # prob = 0.8
    # for _ in range(3):
    #     if bossColor == '' and (bossColor1 == '' and bossColor2 == ''):
    #         prob = prob - 0.1
    #     bossColor = ''
    #     bossColor1 = ''
    #     bossColor2 = ''
    #
    #     results2 = []

    # ts = yolo.find_all(rect=[105,291,620,452])
    # print(ts)
    # for r in ts:
    #     # print(r)
    #     if r.prob > prob:
    #         if '单-木' in r.label:
    #             bossColor = "木"
    #         if '单-水' in r.label:
    #             bossColor = "水"
    #         if '单-火' in r.label:
    #             bossColor = "火"
    #
    #         if '双-水' in r.label:
    #             bossColor1 = "水"
    #         if '双-火' in r.label:
    #             bossColor1 = "火"
    #         if '双-木' in r.label:
    #             bossColor1 = "木"
    #
    #         if '双-目标-火' in r.label:
    #             bossColor2 = "火"
    #         if '双-目标-木' in r.label:
    #             bossColor2 = "木"
    #         if '双-目标-水' in r.label:
    #             bossColor2 = "水"
    #         if '双-目标-蒸汽' in r.label:
    #             bossColor2 = "蒸汽"
    #         if '双-目标-花' in r.label:
    #             bossColor2 = "花"
    #
    # if bossColor != '' or bossColor1 != '' or bossColor2 != '':
    #     results2.append((bossColor, bossColor1, bossColor2))

    # 单-水；兜底
    if bossColor == '' and bossColor1 == '' and bossColor2 == '':
        res = CompareColors.compare("360,378,#A0E4F3", diff=0.9)
        if res:
            bossColor = '水'
        if not res:
            res = CompareColors.compare("360,380,#FEB390", diff=0.93)
            if res:
                bossColor = '火'
        if not res:
            res = CompareColors.compare("356,387,#9CDD72", diff=0.9)
            if res:
                bossColor = '木'

        # 识别双色
        if bossColor == '':
            # res1 = CompareColors.compare("240,361,#FEFEFE|241,370,#FEFEFE|247,370,#C0ECF6|251,374,#FEFEFE|246,381,#9EE3F3|243,381,#94E2F1",diff=0.9)
            # if res1:
            #     bossColor1 = '水'

            res2, _, _ = imageFind('火焰大王-蒸汽', 0.9, 434, 328, 516, 416)
            if res2:
                bossColor2 = '蒸汽'
            if not res2:
                res2, _, _ = imageFind('火焰大王-花', confidence1=0.87)
                if res2:
                    bossColor2 = '花'
            if not res2:
                res2, _, _ = imageFind('火焰大王-水', confidence1=0.92)
                if res2:
                    bossColor2 = '水'

            if bossColor2 != '':
                # 游戏简化后，基础状态仅有水
                bossColor1 = '水'

            # res2 = CompareColors.compare("468,363,#BEF6FD|475,364,#C6F9FE|473,377,#93D9FB|464,380,#66ABF4|472,380,#87CEFA|473,383,#8BCAFA",diff=0.8)
            # if res2:
            #     bossColor2 = '水'
            # if not res2:
            #     res2 = CompareColors.compare("468,366,#B567BE|473,366,#B7EBFC|481,366,#B469C0|464,377,#B671BD|472,375,#D5F6FB|478,372,#A07FD5",diff=0.8)
            #     if res2:
            #         bossColor2 = '蒸汽'
            # if not res2:
            #     res2 = CompareColors.compare("465,367,#C2FAFD|475,367,#8DEFDB|484,369,#CEFAFD|486,375,#77DBB2|487,385,#ECFAFA|468,388,#51B97E",diff=0.8)
            #     if res2:
            #         bossColor2 = '花'

    if bossColor == '':
        # boss状态刷新
        功能开关['bossLastColor'] = ''
    if bossColor1 == '' and bossColor2 == '':
        功能开关['bossLastColor1'] = ''
        功能开关['bossLastColor2'] = ''

    # 统计结果
    # counter = Counter(results2)
    # 取最多出现的结果
    # if len(counter.most_common(1)) > 0:
    # print(counter.most_common(1))
    # bossColor, bossColor1, bossColor2 = counter.most_common(1)[0][0]

    if bossColor != '':
        功能开关['bossColor'] = bossColor
    if bossColor1 != '':
        功能开关['bossColor1'] = bossColor1
    if bossColor2 != '':
        功能开关['bossColor2'] = bossColor2

    print(功能开关['bossColor'], '|', 功能开关['bossColor1'], '|', 功能开关['bossColor2'], '|')
    if 功能开关['bossColor'] != '' or (功能开关['bossColor1'] != '' and 功能开关['bossColor2'] != ''):
        sleep(0.5)
    sleep(0.3)


def daBaoZouLieYanBoss():
    功能开关['bossColor'] = ''
    功能开关['bossNumber0'] = ''
    功能开关['bossNumber1'] = ''
    功能开关['bossNumber2'] = ''

    # 匹配中间数字的颜色
    # 进入二阶段（左右数字）后，无需识别颜色
    results = []
    results2 = []

    bossColor = ''
    bossColor2 = ''
    bossNumber = ''
    bossNumber2 = ''

    中间数字 = ''
    左1数字 = ''
    右1数字 = ''

    # if 功能开关['bossLastNumber1'] == '' and 功能开关['bossLastNumber2'] == '':
    prob = 0.8
    for _ in range(5):
        if bossColor == '' and (左1数字 == '' and 右1数字 == ''):
            prob = prob - 0.1
        bossColor = ''
        bossColor2 = ''
        中间数字 = ''
        左1数字 = ''
        右1数字 = ''

        ts = yolo.find_all()
        for r in ts:
            print(r)
            if r.prob > prob:
                if '紫' in r.label:
                    bossColor = "紫"
                if '黄' in r.label:
                    if bossColor != '':
                        bossColor = ''
                        bossColor2 = "橙"
                    else:
                        bossColor = "橙"

                if any(c in r.label for c in "123456789"):
                    if 中间数字 != '':
                        中间数字 = ''
                        if '黄' in r.label:
                            左1数字 = r.label[1]
                        if '紫' in r.label:
                            右1数字 = r.label[1]
                    else:
                        中间数字 = r.label[1]
                        if '黄' in r.label:
                            左1数字 = r.label[1]
                        if '紫' in r.label:
                            右1数字 = r.label[1]

        if 中间数字 != '' or 左1数字 != '' or 右1数字 != '':
            results2.append((中间数字, 左1数字, 右1数字))
        # 将结果存储到 results 列表中
        if bossColor != '':
            results.append(bossColor)

    # 统计结果
    counter = Counter(results)
    # 取最多出现的结果
    if len(counter.most_common(1)) > 0:
        # print(counter.most_common(1))
        bossColor = counter.most_common(1)[0][0]

    功能开关['bossColor'] = bossColor
    if bossColor == '':
        # boss状态刷新
        功能开关['bossLastNumber0'] = ''
        功能开关['bossLastColor'] = ''

    # 重复识别 10 次
    中间数字 = ''
    左1数字 = ''
    右1数字 = ''
    # for _ in range(3):
    #     中间数字 = ''
    #     左1数字 = ''
    #     右1数字 = ''
    #     if bossColor != '':
    #         res, 中间数字 = CustomOcrText(333, 337, 380, 397, '中间数字', '123456789')
    #     res, 左1数字 = CustomOcrText(281, 344, 320, 394, "左1数字", '123456789')
    #     res, 右1数字 = CustomOcrText(401, 345, 438, 392, "右1数字", '123456789')
    #     if 中间数字 != '' or (左1数字  != '' and 右1数字 != ''):
    #         results2.append((中间数字, 左1数字, 右1数字))

    # 统计结果
    counter = Counter(results2)
    # 取最多出现的结果
    if len(counter.most_common(1)) > 0:
        # print(counter.most_common(1))
        中间数字, 左1数字, 右1数字 = counter.most_common(1)[0][0]

    # for i in range(1, 6):
    # if 功能开关['bossColor'] != '':  # 优先识别中间颜色
    # res, 中间数字 = TomatoOcrText(333, 337, 380, 397, "中间数字")
    # if 中间数字 == '':
    #     res, 中间数字 = TomatoOcrText(344, 344, 377, 391, "中间数字")
    #     if 中间数字 == '':
    #         res, 中间数字 = TomatoOcrText(345, 347, 375, 396, "中间数字")
    #         if 中间数字 == '':
    #             res, 中间数字 = TomatoOcrText(339,339,380,397, "中间数字")

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

    # if 中间数字 == '':
    # res, 左1数字 = TomatoOcrText(281, 344, 320, 394, "左1数字")
    # if 左1数字 == '':
    #     res, 左1数字 = TomatoOcrText(273, 333, 331, 397, "左1数字")
    #     if 左1数字 == '':
    #         res, 左1数字 = TomatoOcrText(345, 347, 375, 396, "左1数字")
    #
    # if 左1数字 != '':
    #     for i in range(1, 3):
    #         res, 右1数字 = TomatoOcrText(401, 345, 438, 392, "右1数字")
    #         if 右1数字 == '':
    #             res, 右1数字 = TomatoOcrText(393, 337, 446, 400, "右1数字")
    #             if 右1数字 == '':
    #                 res, 右1数字 = TomatoOcrText(345, 347, 375, 396, "右1数字")
    #         if 右1数字 != '':
    #             break
    # if 中间数字 != '' or (左1数字 != '' and 右1数字 != ''):
    #     break

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

    print(功能开关['bossColor'], '|', 功能开关['bossNumber0'], '|', 功能开关['bossNumber1'], '|',
          功能开关['bossNumber2'])

    if 功能开关['bossNumber0'] != '' or 功能开关['bossNumber1'] != '' or 功能开关['bossNumber2'] != '':
        sleep(1)
