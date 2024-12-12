# 导包
from .baseUtils import *
from .res.ui.ui import 功能开关
from .res.ui.ui import 任务记录
from ascript.android.screen import FindColors


class AutoMove:
    def __init__(self):
        self.fighting = 0
        self.lastCheckFighting = 0

    # 自动锁敌、自动走位
    def autoMove(self):
        while 1:
            if 任务记录['喊话-并发锁'] == 1:
                sleep(0.2)
                continue

            # 间隔2s检查战斗中状态
            if self.fighting == 0 or time.time() - self.lastCheckFighting > 5:
                re1 = CompareColors.compare(
                    "657,324,#F3EDDD|659,324,#F3EDDD|664,331,#F3EDDD|676,329,#F3EDDD|681,337,#F3EDDD|687,334,#F3EDDD")  # 战斗内队伍图标
                if re1:
                    res3, _ = TomatoOcrText(647, 879, 686, 904, '自动')  # 辅助施法-识别战斗状态
                    res4, _ = TomatoOcrText(647, 879, 686, 904, '手动')  # 辅助施法-识别战斗状态
                    # print('辅助施法-识别战斗状态')
                    # if res1 or res2 or res3 or res4:
                    if res3 or res4:
                        print('辅助战斗AI-识别战斗状态-开始战斗')
                        self.fighting = 1
                    else:
                        sleep(0.2)
                        self.fighting = 0
                else:
                    任务记录['战斗-恶龙名称'] = ''  # 重置
                    sleep(0.2)
                    self.fighting = 0  # 主线推图不辅助施法
                self.lastCheckFighting = time.time()

            if self.fighting == 0:
                continue

            # 识别当前职业
            if 任务记录['玩家-当前职业'] == '':
                re, x, y = imageFind("职业-战士", 0.85, 4, 41, 72, 118)
                if re:
                    Toast('识别当前职业-战士')
                    任务记录['玩家-当前职业'] = '战士'
            if 任务记录['玩家-当前职业'] == '':
                re, x, y = imageFind("职业-服事", 0.85, 4, 41, 72, 118)
                if re:
                    Toast('识别当前职业-服事')
                    任务记录['玩家-当前职业'] = '服事'
            if 任务记录['玩家-当前职业'] == '':
                re, x, y = imageFind("职业-刺客", 0.85, 4, 41, 72, 118)
                if re:
                    Toast('识别当前职业-刺客')
                    任务记录['玩家-当前职业'] = '刺客'
            if 任务记录['玩家-当前职业'] == '':
                re, x, y = imageFind("职业-法师", 0.85, 4, 41, 72, 118)
                if re:
                    Toast('识别当前职业-法师')
                    任务记录['玩家-当前职业'] = '法师'
            if 任务记录['玩家-当前职业'] == '':
                re, x, y = imageFind("职业-游侠", 0.85, 4, 41, 72, 118)
                if re:
                    Toast('识别当前职业-游侠')
                    任务记录['玩家-当前职业'] = '游侠'

            if 功能开关['队伍AI锁敌']:
                # 切换攻击目标
                point = FindColors.find(
                    "135,252,#7CA2E2|153,238,#7DA1E2|170,255,#85A7E1|164,265,#7DA1E2|150,271,#94B1E5",
                    rect=[1, 175, 697, 836], diff=0.95)
                if point:
                    Toast('切换攻击目标')
                    print(point.x, point.y)
                    tapSleep(point.x, point.y)

            if 功能开关['队伍AI走位']:
                # 移动走位
                # 部分地图根据机制走位
                if 任务记录['玩家-当前职业'] == '战士':
                    if "云涌风雷王座" in 任务记录['玩家-当前关卡'] or "雷神之锤" in 任务记录['玩家-当前关卡']:
                        # 不走位，避免移动引雷
                        Toast('停止移动，避免引雷')
                        continue

                if 任务记录['战斗-恶龙名称'] == '' or time.time() - 任务记录['战斗-恶龙名称-识别倒计时'] > 5:
                    re, 任务记录['战斗-恶龙名称'] = TomatoOcrText(288, 222, 408, 246, '恶龙名称')
                    任务记录['战斗-恶龙名称-识别倒计时'] = time.time()
                if 任务记录['战斗-恶龙名称'] == '真炎界印龙':
                    for k in range(30):
                        # 定位玩家位置
                        x, y = 298, 746
                        point = FindColors.find("336,738,#BFFF26|336,740,#BFFF26|341,737,#BFFF26|341,738,#BFFF26")
                        if point:
                            x, y = point.x, point.y

                        # 玩家头上为星星
                        re = FindColors.find(
                            "650,732,#FEFED5|650,737,#FEFED7|647,743,#FEFED7|637,741,#FEFECC|666,743,#FEFECF",
                            rect=[x - 10, y - 130, x + 120, y])
                        if re:
                            Toast('恶龙黯蚀‌-星星，自动走位')
                            re = imageFindClick('恶龙-星星', x1=9, y1=632, x2=205, y2=797)

                        # 玩家头上为太阳
                        re = FindColors.find_all(
                            "407,669,#FEFAA3|404,664,#FEFAA3|412,666,#FEFAA3|394,680,#FEF89B|405,686,#FEF89B|418,681,#FEF89B",
                            rect=[x - 10, y - 130, x + 120, y])
                        if re:
                            Toast('恶龙黯蚀‌-太阳，自动走位')
                            re = imageFindClick('恶龙-太阳', x1=9, y1=632, x2=205, y2=797)

                        # 玩家头上为月亮
                        re = FindColors.find(
                            "337,666,#FCFEFE|334,677,#FCFEFE|334,689,#FCFEFE|336,681,#FDFEFE|350,703,#FAFEFE|356,711,#80B2FB",
                            rect=[x - 10, y - 130, x + 120, y])
                        if re:
                            Toast('恶龙黯蚀‌-月亮，自动走位')
                            re = imageFindClick('恶龙-月亮', x1=9, y1=632, x2=205, y2=797)

                        re1 = FindColors.find(
                            "393,719,#FEEE5D|399,719,#FEF166|404,713,#FEF46C|405,721,#FEE14D|416,705,#FEF671|423,718,#FEF774",
                            rect=[203, 658, 519, 741])
                        re2 = FindColors.find(
                            "484,667,#FEFEA1|480,675,#FEFEB2|473,680,#FEFEB7|487,688,#FEFEB2|481,696,#FEFEB6",
                            rect=[205, 640, 509, 757])
                        re3 = FindColors.find(
                            "475,676,#FEEE61|470,681,#FEF268|459,689,#FEF670|481,697,#FEF063|464,706,#FEF773",
                            rect=[205, 640, 522, 757])
                        if re1 or re2 or re3:
                            Toast('恶龙真炎-顺时针，自动走位')
                            tapSleep(63, 677)
                            for j in range(20):
                                re, _ = TomatoOcrText(326, 523, 377, 549, '真炎')
                                if not re:
                                    continue
                                Toast('恶龙真炎-顺时针，自动走位')
                                tapSleep(63, 677)
                                sleep(0.4)

                        re1 = FindColors.find(
                            "463,693,#FEFEAF|451,695,#FEFEB7|456,702,#FEFEB8|442,695,#FEFEB7|447,713,#FEFEBC|428,711,#FEC84D",
                            rect=[205, 640, 509, 757])
                        re2 = FindColors.find(
                            "360,722,#FEFEB0|348,719,#FEFEBB|330,713,#FEFEBE|325,730,#FEFEBC|307,727,#FEFED4",
                            rect=[205, 640, 509, 757])
                        re3 = FindColors.find(
                            "483,681,#FEF065|480,683,#FEF46B|448,688,#FEF268|470,699,#FEF773|456,710,#FEF56E",
                            rect=[205, 640, 509, 757])
                        if re1 or re2 or re3:
                            Toast('恶龙真炎-逆时针，自动走位')
                            tapSleep(143, 675)
                            for j in range(20):
                                re, _ = TomatoOcrText(326, 523, 377, 549, '真炎')
                                if not re:
                                    continue
                                Toast('恶龙真炎-逆时针，自动走位')
                                tapSleep(143, 675)
                                sleep(0.4)
                        re, _ = TomatoOcrText(326, 523, 377, 549, '真炎')
                        if re:
                            Toast('恶龙真炎，自动走位')
                            tapSleep(143, 675)
                        sleep(0.5)
                    sleep(0.5)
                    continue

                # 恶龙红圈
                re = FindColors.find("211,1018,#EA1F1B|214,1025,#EA3020|215,1020,#E71919|210,1020,#EA281D",
                                     rect=[118, 894, 503, 1052], diff=0.9)
                if re:
                    re = imageFindClick('战斗-向左移动', x1=11, y1=565, x2=206, y2=778)
                    if re:
                        Toast('boss技能，自动走位')

                re = FindColors.find("181,684,#FEFEC7|183,684,#FEFEDB|187,686,#FEFEC9|184,684,#FEFEDF",
                                     rect=[3, 1155, 112, 1213], diff=0.9)
                if re:
                    # 黑曜界印龙
                    Toast('恶龙技能，自动走位')
                    tapSleep(64, 672)
                    任务记录['战斗-上一次移动'] = time.time()

                # 灾厄真体破界龙
                if 任务记录['战斗-恶龙名称'] == '灾厄真体破':
                    for k in range(30):
                        re = FindColors.find(
                            "564,1030,#9AD3C6|566,1029,#9BD3C6|566,1027,#9FD5C9|571,1028,#98D3C6|577,1027,#569D91",
                            rect=[11, 757, 690, 1114], diff=0.9)
                        if re:
                            # 灾厄真体破界龙
                            Toast('恶龙技能，自动走位')
                            tapSleep(64, 672)
                            任务记录['战斗-上一次移动'] = time.time()
                        sleep(0.5)
                    sleep(0.5)
                    continue

                if time.time() - 任务记录['战斗-上一次移动'] > 7:
                    re = imageFindClick('战斗-向左移动', x1=11, y1=565, x2=206, y2=778)
                    if re:
                        Toast('自动走位')
                    任务记录['战斗-上一次移动'] = time.time()
