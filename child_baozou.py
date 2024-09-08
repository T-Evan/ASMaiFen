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
    功能开关['bossLastColor'] = ''
    功能开关['bossNumber0'] = ''
    功能开关['bossNumber1'] = ''
    功能开关['bossNumber2'] = ''
    功能开关['bossLastNumber0'] = ''
    功能开关['bossLastNumber1'] = ''
    功能开关['bossLastNumber2'] = ''
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
        else:
            break


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
