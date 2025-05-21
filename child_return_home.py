# 导包
from time import sleep

from ascript.android import system
from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .res.ui.ui import switch_lock
from .baseUtils import *
from threading import Lock
from ascript.android.screen import FindColors


# 实例方法
def main():
    while True:
        # print(功能开关["needHome"],功能开关["noHomeMust"],功能开关["fighting"])
        if 功能开关["needHome"] == 1 and 功能开关["noHomeMust"] == 0 and 功能开关["fighting"] == 0:
            print("返回首页处理线程 - 运行中")
            returnHome()
            sleep(1)  # 等待 1 秒
        else:
            sleep(1)  # 等待 5 秒


def returnHome():
    for i in range(6):
        return1 = False
        return2 = False
        return3 = False

        # print(i, 功能开关["needHome"], 功能开关["noHomeMust"])
        if i > 3 and 功能开关["noHomeMust"] == 0:
            # 返回上级页面时二次确认入口通用处理
            res = openTreasure(noNeedOpen=1)
            res = TomatoOcrTap(454, 727, 508, 758, "确定")

        if 功能开关["needHome"] == 1 and 功能开关["noHomeMust"] == 0:
            return1 = TomatoOcrTap(67, 1182, 121, 1221, '返回', 10, 10)
            if not return1:
                return2 = TomatoOcrTap(91, 1185, 127, 1221, '回', 10, 10)
            if not return2:
                return2 = TomatoOcrTap(102, 1202, 132, 1229, '回', 10, 10)
            if return1 or return2:
                Toast('线程-返回首页1')

        if i > 3 and not return1 and not return2 and 功能开关["needHome"] == 1 and 功能开关["noHomeMust"] == 0:
            return3 = TomatoOcrTap(76, 1161, 126, 1190, '返回', 10, 10)
            if not return3:
                return3 = TomatoOcrTap(93, 1190, 143, 1220, '返回', 10, 10)
                if not return3:
                    return3 = TomatoOcrFindRangeClick('', 0.9, 0.9, 6, 1084, 127, 1267, timeLock=5,
                                                      offsetX=20, offsetY=20,
                                                      keywords=[{'keyword': '返回', 'match_mode': 'fuzzy'},
                                                                {'keyword': '营地', 'match_mode': 'fuzzy'},
                                                                {'keyword': '退出', 'match_mode': 'fuzzy'}])
                    re = CompareColors.compare("650,58,#FFFFFF|663,58,#373737|667,58,#333333|675,61,#FFFFFF")
                    if re:
                        tapSleep(666, 58)  # tap社区页面退出
            # return3 = TomatoOcrTap(89, 1197, 136, 1220, '返回', 10, 10)
            # if not return3:
            #     return3 = TomatoOcrTap(77, 1161, 127, 1191, '营地', 10, 10)
            #     if not return3:
            #         return3 = TomatoOcrTap(69, 1182, 127, 1220, '营地', 10, 10)
            #         if not return3:
            #             # return2 = imageFindClick('返回_1')
            #             return3 = TomatoOcrTap(86, 1193, 140, 1224, '返回', 10, 10)
            if return3:
                Toast('线程-返回首页2')

            # if not res:
            #     re = TomatoOcrFindRangeClick(x1=39, y1=250, x2=674, y2=1205,
            #                                  keywords=[{'keyword': '确定', 'match_mode': 'exact'},
            #                                            {'keyword': '确认', 'match_mode': 'exact'}])
            #     if re:
            #         Toast('线程-返回首页-确定')

        # if i > 4:
        #     点击首页-冒险
        re = TomatoOcrTap(330, 1201, 389, 1238, '冒险')

        if 1:
            # 识别是否进入首页
            # 判断底部冒险图标
            res2, _ = TomatoOcrText(625, 363, 709, 388, "冒险手册")
            shou_ye1 = False
            shou_ye2 = False
            if not res2:
                shou_ye2, _ = TomatoOcrText(545, 381, 628, 404, "新手试炼")
                if not shou_ye2:
                    shou_ye2, _ = TomatoOcrText(627, 381, 710, 403, "新手试炼")
                # 暂不处理，提高执行效率
                # if not shou_ye1:
                #     shou_ye2 = TomatoOcrFindRange('冒险手册', 0.9, 360, 0, 720, 1280, '冒险手册')
                # shou_ye2 = TomatoOcrFindRange('试炼', 0.9, 360, 0, 720, 1280, '试炼')
            if res2 or shou_ye1 or shou_ye2:
                功能开关["needHome"] = 0
                Toast('线程-已返回首页')
                return True

        # # 兜底
        # if i == 3:
        #     # 开始冒险之旅
        #     login1 = TomatoOcrTap(282, 1017, 437, 1051, "开始冒险之旅")
        #     # 开始冒险
        #     login2 = TomatoOcrTap(302, 1199, 414, 1231, "开始冒险")

    return


def openTreasure(noNeedOpen=0):
    isTreasure = 0  # 是否在宝箱页
    if noNeedOpen == 0:
        noNeedOpen = 功能开关['秘境不开宝箱']

    res, _ = TomatoOcrText(300, 606, 417, 634, "宝箱尚未开启")  # 避免前置错误点击弹出宝箱尚未开启
    if res:
        res = TomatoOcrTap(99, 1199, 128, 1234, "回")  # 关闭确认弹窗，返回待领取页

    res1 = False
    tmp2 = False
    tmp3 = False
    tmp4 = False
    # 房间页 - 宝箱UI
    res1 = FindColors.find("174,1013,#F3A84B|192,1019,#F3A84B|270,1012,#F3A84B|204,1037,#F2DA70",
                           rect=[60, 102, 641, 1180], diff=0.95)
    if res1:
        isTreasure = 1
        # 加锁兜底

    if noNeedOpen == 1:
        openStatus = 0
        if isTreasure == 1:
            if 功能开关['秘境点赞队友'] == 1:
                Toast('点赞队友')
                res = TomatoOcrTap(516, 549, 592, 572, "一键全赞", 5, 5)  # 一键点赞
                if not res:
                    res = TomatoOcrTap(511, 458, 595, 484, "一键全赞", 5, 5)  # 一键点赞
                    if not res:
                        res = TomatoOcrFindRangeClick("全赞", x1=480, y1=490, x2=615, y2=768,
                                                      match_mode='fuzzy')  # 一键点赞
                if not res:
                    for i in range(2):
                        imageFindClick('点赞1', confidence1=0.8, x1=107, y1=279, x2=633, y2=809, sleep1=0.7)
                        imageFindClick('点赞2', confidence1=0.8, x1=107, y1=279, x2=633, y2=809, sleep1=0.7)
            Toast('不开宝箱-返回房间')
            # 加锁兜底
            tapSleep(645, 1235, 0.8)  # 战斗结束页确认不领取
            res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
            if not res:
                res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
                if not res:
                    tapSleep(645, 1235, 1)  # 战斗结束页确认不领取
                    res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
            if not res:
                Toast('返回房间-2')
                res = TomatoOcrTap(96, 1199, 130, 1232, "回", 10, 10, 0.8)  # 返回
                res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
                if not res:
                    Toast('返回房间-3')
                    res = TomatoOcrFindRangeClick("确定", whiteList='确定', x1=88, y1=277, x2=644,
                                                  y2=986)  # 战斗结束页确认退出
                    # res = TomatoOcrTap(331, 727, 388, 761, "确定")  # 确定返回
                if res:
                    openStatus = 1
            else:
                openStatus = 1
        return openStatus

    # 点赞队友
    if 功能开关['秘境点赞队友'] == 1:
        if isTreasure == 1:
            Toast('点赞队友')
            res = TomatoOcrTap(516, 549, 592, 572, "一键全赞", 5, 5)  # 一键点赞
            if not res:
                res = TomatoOcrTap(511, 458, 595, 484, "一键全赞", 5, 5)  # 一键点赞
                if not res:
                    res = TomatoOcrFindRangeClick("全赞", x1=480, y1=490, x2=615, y2=768,
                                                  match_mode='fuzzy')  # 一键点赞
            # if not res:
            #     for i in range(1, 4):
            #         imageFindClick('点赞1', confidence1=0.8, x1=107, y1=279, x2=633, y2=809, sleep1=0.7)
            #         imageFindClick('点赞2', confidence1=0.8, x1=107, y1=279, x2=633, y2=809, sleep1=0.7)

    attempts = 0  # 初始化尝试次数
    maxAttempts = 3  # 设置最大尝试次数

    openStatus = 0
    if isTreasure == 1:
        re = FindColors.find(
            "292,1065,#A6A1AD|306,1068,#A6A1AD|314,1065,#A6A1AD|306,1079,#A6A1AD|314,1077,#A6A1AD|290,1093,#A6A1AD",
            rect=[101, 623, 618, 1087], diff=0.93)
        if not re:
            re, _ = TomatoOcrText(453, 1006, 528, 1029, '体力不足')
        if re:
            Toast('体力不足 - 跳过宝箱')
            tapSleep(645, 1235, 0.8)  # 战斗结束页确认不领取
            res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
            if not res:
                res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
                if not res:
                    tapSleep(645, 1235, 1)  # 战斗结束页确认不领取
                    res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
            if not res:
                Toast('返回房间-2')
                res = TomatoOcrTap(96, 1199, 130, 1232, "回", 10, 10, 0.8)  # 返回
                res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
                if not res:
                    Toast('返回房间-3')
                    res = TomatoOcrFindRangeClick("确定", whiteList='确定', x1=88, y1=277, x2=644,
                                                  y2=986)  # 战斗结束页确认退出
                    # res = TomatoOcrTap(331, 727, 388, 761, "确定")  # 确定返回
            if res:
                openStatus = 1
        else:
            Toast('准备开启宝箱')
            while attempts < maxAttempts:
                res, _ = TomatoOcrText(300, 606, 417, 634, "宝箱尚未开启")  # 避免前置错误点击弹出宝箱尚未开启
                if res:
                    res = TomatoOcrTap(99, 1199, 128, 1234, "回")  # 关闭确认弹窗，返回待领取页

                attempts = attempts + 1
                # 先快速图色匹配一次宝箱图标
                res1 = FindColors.find("174,1013,#F3A84B|192,1019,#F3A84B|270,1012,#F3A84B|204,1037,#F2DA70",
                                       rect=[60, 102, 641, 1180], diff=0.95)
                if res1:
                    # 图色识别兜底
                    res = imageFindClick('宝箱-开启')
                    if res:
                        Toast('开启宝箱')
                        sleep(1.5)
                        tapSleep(340, 930)
                        openStatus = 1
                    tmp = FindColors.find(
                        "292,1065,#A6A1AD|306,1068,#A6A1AD|314,1065,#A6A1AD|306,1079,#A6A1AD|314,1077,#A6A1AD|290,1093,#A6A1AD",
                        rect=[101, 623, 618, 1087], diff=0.93)
                    if tmp:
                        Toast('体力不足 - 跳过宝箱')
                        break
                    res = imageFindClick('宝箱-开启2')
                    if res:
                        Toast('开启宝箱')
                        sleep(1.5)
                        tapSleep(340, 930)
                        openStatus = 1

    if openStatus == 1:
        Toast('开启宝箱 - 成功')

    # 开启宝箱后，返回
    if openStatus == 1 or isTreasure == 1:
        Toast("已开启宝箱 - 返回房间")
        res = TomatoOcrTap(96, 1199, 130, 1232, "回", sleep1=0.8)  # 返回
        res = TomatoOcrTap(330, 726, 387, 759, "确定")  # 确定返回
        if not res:
            res = TomatoOcrTap(331, 727, 388, 761, "确定")  # 确定返回
        if not res:
            # 识别战斗结束页提前返回
            res1 = False
            res1, _, _ = TomatoOcrFindRange("通关奖励", x1=112, y1=456, x2=620, y2=1032)  # 战斗结束页。宝箱提示
            if res1:
                tapSleep(645, 1235, 3)  # 战斗结束页确认不领取
                # res = TomatoOcrTap(329, 728, 386, 759, "确定")  # 战斗结束页确认退出
                res = TomatoOcrFindRangeClick("确定", whiteList='确定')  # 战斗结束页确认退出
                if not res:
                    res = TomatoOcrTap(96, 1199, 130, 1232, "回")  # 返回
                    res = TomatoOcrTap(329, 728, 386, 759, "确定")  # 确定
                    if not res:
                        res = TomatoOcrTap(331, 727, 388, 761, "确定")  # 确定返回
                        openStatus = 1
    return openStatus
