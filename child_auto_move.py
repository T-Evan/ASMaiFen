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

            # 关闭进入战斗后启动时，依赖主线程判断是否进入战斗状态
            if 功能开关['AI进入战斗后启动'] == 0:
                if 功能开关["fighting"] == 0:
                    sleep(2)
                    continue

            # 间隔2s检查战斗中状态
            if (self.fighting == 0 and time.time() - self.lastCheckFighting > 5) or (
                    self.fighting == 1 and time.time() - self.lastCheckFighting > 10):
                re1 = CompareColors.compare(
                    "657,324,#F3EDDD|659,324,#F3EDDD|664,331,#F3EDDD|676,329,#F3EDDD|681,337,#F3EDDD|687,334,#F3EDDD")  # 战斗内队伍图标
                if re1:
                    res3, _ = TomatoOcrText(646, 879, 687, 902, '自动')  # 辅助施法-识别战斗状态
                    res4, _ = TomatoOcrText(646, 879, 687, 902, '手动')  # 辅助施法-识别战斗状态
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
                    rect=[93, 263, 628, 749], diff=0.95)
                if point:
                    Toast('切换攻击目标')
                    # print(point.x, point.y)
                    tapSleep(point.x, point.y)

            if 功能开关['队伍AI走位']:
                # 移动走位
                # 部分地图根据机制走位
                if 任务记录['玩家-当前职业'] == '战士':
                    if "云涌风雷王座" in 任务记录['战斗-关卡名称'] or "雷神之锤" in 任务记录['战斗-关卡名称']:
                        # 不走位，避免移动引雷
                        Toast('停止移动，避免引雷')
                        continue

                if 任务记录['战斗-恶龙名称'] == '' or time.time() - 任务记录['战斗-恶龙名称-识别倒计时'] > 5:
                    re, 任务记录['战斗-恶龙名称'] = TomatoOcrText(288, 222, 408, 246, '恶龙名称')
                    if 任务记录['战斗-恶龙名称'] == "":
                        # 识别右上角关卡名称
                        re, 任务记录['战斗-恶龙名称'] = TomatoOcrText(440, 138, 600, 160, '关卡名称')
                    if 任务记录['战斗-恶龙名称'] == "":
                        re, 任务记录['战斗-恶龙名称'] = TomatoOcrText(439, 63, 615, 92, '关卡名称')
                    任务记录['战斗-恶龙名称-识别倒计时'] = time.time()

                # 白网与织女
                if '白网与织女' in 任务记录['战斗-恶龙名称']:
                    sleep(3)
                    continue

                if '暴走' in 任务记录['战斗-恶龙名称']:
                    sleep(5)
                    continue

                # 三打三守三魔头
                if '三打三守' in 任务记录['战斗-恶龙名称']:
                    if 任务记录['战斗-上一次移动'] == 0:
                        任务记录['战斗-上一次移动'] = time.time()
                    Toast(f'三打三守三魔头 - 自动走位')
                    for k in range(30):
                        # 自动施法
                        skill = CompareColors.compare("422,944,#FFFFCC|425,943,#FDFAC0|427,943,#FCF8C1")
                        if skill:
                            Toast('释放技能')
                            tapSleep(424, 975)
                        if time.time() - 任务记录['战斗-上一次移动'] > 5:
                            # 黄色牛头boss
                            re = FindColors.find("98,628,#863F2D|103,628,#853E30|106,628,#873F30",
                                                 rect=[13, 585, 196, 774], diff=0.93)
                            if re:
                                任务记录['战斗-上一次移动'] = time.time()
                                Toast('前往战斗地块')
                                tapSleep(re.x, re.y)
                                tapSleep(re.x, re.y)
                                continue
                            # 蓝色精英兵
                            re = FindColors.find("151,688,#83E5E8|153,684,#67D1E0|146,691,#98F2EF",
                                                 rect=[13, 585, 196, 774], diff=0.93)
                            if re:
                                任务记录['战斗-上一次移动'] = time.time()
                                Toast('前往战斗地块')
                                tapSleep(re.x, re.y)
                                tapSleep(re.x, re.y)
                                continue
                            re = FindColors.find("105,612,#F05941|72,636,#EE4038|138,634,#E14A4F",
                                                 rect=[11, 585, 210, 798], diff=0.9)
                            # 爆炸图标
                            re = FindColors.find("56,683,#F6C27D|57,683,#F8C07B|68,691,#FAD395|69,699,#FEEEC9")
                            if re:
                                任务记录['战斗-上一次移动'] = time.time()
                                Toast('前往战斗地块')
                                tapSleep(re.x, re.y)
                                tapSleep(re.x, re.y)
                                continue
                            re = FindColors.find("105,612,#F05941|72,636,#EE4038|138,634,#E14A4F",
                                                 rect=[11, 585, 210, 798], diff=0.9)
                            if re:
                                任务记录['战斗-上一次移动'] = time.time()
                                tapSleep(re.x + 20, re.y + 30)  # 移动-红色地块
                                tapSleep(re.x + 20, re.y + 30)  # 移动-红色地块
                                Toast('前往战斗地块')
                            if not re:
                                re = FindColors.find("105,610,#AD414C|72,637,#B64B48|140,642,#A95863",
                                                     rect=[11, 585, 210, 798], diff=0.9)
                                if re:
                                    任务记录['战斗-上一次移动'] = time.time()
                                    tapSleep(re.x, re.y + 30)  # 移动-红色地块
                                    tapSleep(re.x, re.y + 30)  # 移动-红色地块
                                    Toast('前往战斗地块')
                            if not re:
                                re = FindColors.find("104,708,#BE6D6E|75,735,#A94E4E|138,738,#A94C4D",
                                                     rect=[17, 590, 200, 789], diff=0.9)
                                if re:
                                    任务记录['战斗-上一次移动'] = time.time()
                                    tapSleep(re.x, re.y + 30)  # 移动-红色地块
                                    tapSleep(re.x, re.y + 30)  # 移动-红色地块
                                    Toast('前往战斗地块')
                            if not re:
                                re = FindColors.find(
                                    "154,661,#A76B6C|121,684,#9F5051|186,689,#8E4B4D|184,689,#8D4A4C",
                                    rect=[23, 598, 194, 784], diff=0.9)
                                if re:
                                    任务记录['战斗-上一次移动'] = time.time()
                                    tapSleep(re.x, re.y + 30)  # 移动-红色地块
                                    tapSleep(re.x, re.y + 30)  # 移动-红色地块
                                    Toast('前往战斗地块')
                        sleep(0.5)
                        continue
                    sleep(0.5)
                    continue

                # 三头盘踞拦路关
                if '三头毒' in 任务记录['战斗-恶龙名称']:
                    if 任务记录['战斗-上一次移动'] == 0:
                        任务记录['战斗-上一次移动'] = time.time()
                    name = 任务记录['战斗-恶龙名称']
                    Toast(f'三头盘踞拦路关-自动走位')
                    for k in range(30):
                        if time.time() - 任务记录['战斗-上一次移动'] > 20:
                            任务记录['战斗-上一次移动'] = time.time()
                            tapSleep(142, 673)  # 移动-右侧地块
                            Toast('前往下一地块')
                        sleep(0.5)
                        continue
                    sleep(0.5)
                    continue

                # 雷电焦土深处 - 万钧雷鹫
                if '万钧雷' in 任务记录['战斗-恶龙名称']:
                    Toast(f'雷电焦土深处-自动走位')
                    for k in range(30):
                        re1 = CompareColors.compare("243,962,#EA5F29|251,959,#EA5F29")  # 最左侧地块
                        if re1:
                            tapSleep(145, 675)  # 移动-右侧地块

                        re3 = CompareColors.compare("192,781,#FE6A2C|198,784,#FE692D")  # 最右侧地块红色
                        if re3:
                            tapSleep(58, 677)  # 移动-左侧地块

                        # 定位玩家位置
                        x, y = 298, 746
                        point = FindColors.find("336,738,#BFFF26|336,740,#BFFF26|341,737,#BFFF26|341,738,#BFFF26",
                                                diff=0.95)
                        if point:
                            x, y = point.x, point.y
                        # 玩家所在地板红色
                        re = FindColors.find(
                            "211,896,#E8A780|219,890,#E8BEA5",
                            rect=[x - 100, y - 10, x + 120, y + 200], diff=0.98)
                        if re:
                            tapSleep(145, 675)  # 移动-右侧地块
                            Toast('前往下一地块')
                            for p in range(3):
                                # 玩家所在地板红色
                                re = FindColors.find(
                                    "211,896,#E8A780|219,890,#E8BEA5",
                                    rect=[x - 100, y - 10, x + 120, y + 200], diff=0.98)
                                if re:
                                    tapSleep(58, 677, 1)  # 移动-左侧地块
                        sleep(0.5)
                        continue
                    sleep(0.5)
                    continue

                if 任务记录['战斗-恶龙名称'] == '真炎界印龙' or 任务记录['战斗-恶龙名称'] == '熔火乡界印':
                    name = 任务记录['战斗-恶龙名称']
                    Toast(f'{name}-自动走位')
                    for k in range(30):
                        # 定位玩家位置
                        x, y = 298, 746
                        point = FindColors.find("336,738,#BFFF26|336,740,#BFFF26|341,737,#BFFF26|341,738,#BFFF26",
                                                diff=0.95)
                        if point:
                            x, y = point.x, point.y

                        #
                        if 任务记录['战斗-恶龙名称'] == '熔火乡界印':
                            # 炸地板
                            re = FindColors.find("660,1191,#EAEAE3|660,1191,#EAEAE3|663,1191,#EAEAE5|650,1200,#E9E9C3",
                                                 rect=[9, 1150, 704, 1240], diff=0.95)
                            if re:
                                Toast('恶龙炸地板，自动走位')
                                re = tapSleep(64, 677)

                        # 玩家头上为星星
                        re = FindColors.find(
                            "650,732,#FEFED5|650,737,#FEFED7|647,743,#FEFED7|637,741,#FEFECC|666,743,#FEFECF",
                            rect=[x - 10, y - 130, x + 120, y], diff=0.95)
                        if re:
                            Toast('恶龙黯蚀‌-星星，自动走位')
                            re = imageFindClick('恶龙-星星', x1=9, y1=632, x2=205, y2=797)

                        # 玩家头上为太阳
                        re = FindColors.find(
                            "407,669,#FEFAA3|404,664,#FEFAA3|412,666,#FEFAA3|394,680,#FEF89B|405,686,#FEF89B|418,681,#FEF89B",
                            rect=[x - 10, y - 130, x + 120, y], diff=0.95)
                        if re:
                            Toast('恶龙黯蚀‌-太阳，自动走位')
                            re = imageFindClick('恶龙-太阳', x1=9, y1=632, x2=205, y2=797)

                        # 玩家头上为月亮
                        re1 = FindColors.find(
                            "337,666,#FCFEFE|334,677,#FCFEFE|334,689,#FCFEFE|336,681,#FDFEFE|350,703,#FAFEFE|356,711,#80B2FB",
                            rect=[x - 10, y - 130, x + 120, y], diff=0.95)
                        re2 = FindColors.find(
                            "347,669,#FEFEFE|350,675,#FDFEFE|360,677,#FCFEFE|363,678,#FCFEFE|363,686,#D0A9F4",
                            rect=[x - 10, y - 130, x + 120, y], diff=0.95)
                        if re1 or re2:
                            Toast('恶龙黯蚀‌-月亮，自动走位')
                            re = imageFindClick('恶龙-月亮', x1=9, y1=632, x2=205, y2=797)

                        re1 = FindColors.find(
                            "393,719,#FEEE5D|399,719,#FEF166|404,713,#FEF46C|405,721,#FEE14D|416,705,#FEF671|423,718,#FEF774",
                            rect=[203, 658, 519, 741], diff=0.95)
                        re2 = FindColors.find(
                            "484,667,#FEFEA1|480,675,#FEFEB2|473,680,#FEFEB7|487,688,#FEFEB2|481,696,#FEFEB6",
                            rect=[205, 640, 509, 757], diff=0.95)
                        re3 = FindColors.find(
                            "475,676,#FEEE61|470,681,#FEF268|459,689,#FEF670|481,697,#FEF063|464,706,#FEF773",
                            rect=[205, 640, 522, 757], diff=0.95)
                        re4 = FindColors.find(
                            "410,705,#FEEF63|401,708,#FEF46C|393,710,#FEF773|396,726,#FEF775|418,729,#FEF46B|420,729,#FEF36A",
                            rect=[205, 640, 522, 757], diff=0.95)
                        if re1 or re2 or re3 or re4:
                            Toast('恶龙真炎-顺时针，自动走位')
                            tapSleep(63, 677)
                            for j in range(20):
                                # 真炎
                                re = CompareColors.compare(
                                    "359,533,#FCFCFC|363,531,#FEFEFE|363,530,#FFFFFF|367,532,#FFFFFF|369,543,#FFFFFF",
                                    diff=0.95)
                                # re, _ = TomatoOcrText(326, 523, 377, 549, '真炎')
                                if not re:
                                    continue
                                Toast('恶龙真炎-顺时针，自动走位')
                                tapSleep(63, 677)
                                sleep(0.2)

                        re1 = FindColors.find(
                            "463,693,#FEFEAF|451,695,#FEFEB7|456,702,#FEFEB8|442,695,#FEFEB7|447,713,#FEFEBC|428,711,#FEC84D",
                            rect=[205, 640, 509, 757], diff=0.95)
                        re2 = FindColors.find(
                            "360,722,#FEFEB0|348,719,#FEFEBB|330,713,#FEFEBE|325,730,#FEFEBC|307,727,#FEFED4",
                            rect=[205, 640, 509, 757], diff=0.95)
                        re3 = FindColors.find(
                            "483,681,#FEF065|480,683,#FEF46B|448,688,#FEF268|470,699,#FEF773|456,710,#FEF56E",
                            rect=[205, 640, 509, 757], diff=0.95)
                        re4 = FindColors.find(
                            "311,700,#FEEF62|315,702,#FEEF63|325,705,#FEF267|342,708,#FEF56E|322,721,#773930",
                            rect=[205, 640, 509, 757], diff=0.95)
                        if re1 or re2 or re3 or re4:
                            Toast('恶龙真炎-逆时针，自动走位')
                            tapSleep(143, 675)
                            for j in range(20):
                                # 真炎
                                re = CompareColors.compare(
                                    "359,533,#FCFCFC|363,531,#FEFEFE|363,530,#FFFFFF|367,532,#FFFFFF|369,543,#FFFFFF",
                                    diff=0.95)
                                if not re:
                                    continue
                                Toast('恶龙真炎-逆时针，自动走位')
                                tapSleep(143, 675)
                                sleep(0.2)
                        sleep(0.5)
                    sleep(0.5)
                    continue

                # 神封城破界龙
                if 任务记录['战斗-恶龙名称'] == '神封城破界':
                    # 恶龙红圈
                    re = FindColors.find("211,1018,#EA1F1B|214,1025,#EA3020|215,1020,#E71919|210,1020,#EA281D",
                                         rect=[118, 894, 503, 1052], diff=0.9)
                    if re:
                        re = imageFindClick('战斗-向左移动', x1=11, y1=565, x2=206, y2=778)
                        if re:
                            Toast('boss技能，自动走位')

                if 任务记录['战斗-恶龙名称'] == '黑曜界印龙':
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
                        re1 = FindColors.find("424,809,#F1F2E7|434,814,#E6EFE8|443,814,#E8EFEC|459,804,#F7F7F7",
                                              rect=[12, 703, 678, 1093])
                        re2 = FindColors.find(
                            "566,512,#FBFEF8|570,512,#FBFEFB|572,514,#FCFEF9|576,519,#FBFEFA|576,526,#F2FEF8",
                            rect=[12, 703, 678, 1093])
                        if re1 or re2:
                            # 灾厄真体破界龙
                            Toast('恶龙技能，自动走位')
                            tapSleep(64, 672)
                            任务记录['战斗-上一次移动'] = time.time()
                        sleep(0.5)
                    sleep(0.5)
                    continue

                # 绮梦晶彩龙
                if 任务记录['战斗-恶龙名称'] == '绮梦晶彩龙':
                    re = CompareColors.compare("269,888,#EADFEA|266,894,#EADFEA|262,905,#EAE2EA|258,923,#E9DDEA")
                    if re:
                        Toast('恶龙炸地板，自动走位')
                        tapSleep(69, 674)  # 向左移动
                    入梦能量空 = CompareColors.compare("416,946,#0C0C0C|420,946,#121212|423,946,#151515")
                    isInYun = FindColors.find("653,716,#1D220C|653,694,#1E240D|645,678,#0D1607|686,692,#22290E",
                                              rect=[285, 639, 697, 1149], diff=0.95)
                    # if 入梦能量空:
                    #     # 未入梦，跟随梦境绮云
                    #     if not isInYun:
                    #         Toast('未入梦，跟随梦境绮云-移动')
                    #         yunPoint = FindColors.find(
                    #             "653,716,#1D220C|653,694,#1E240D|645,678,#0D1607|686,692,#22290E", diff=0.95)
                    #         if yunPoint and yunPoint.x > 360:
                    #             # 右半屏
                    #             tapSleep(144, 677)  # 向右移动
                    #         else:
                    #             tapSleep(69, 674)  # 向左移动
                    #     else:
                    #         Toast('未入梦，跟随梦境绮云-停留')
                    # if not 入梦能量空:
                    #     # 已入梦，跟随梦境绮云
                    #     if isInYun:
                    #         Toast('已入梦，躲避梦境绮云-移动')
                    #         tapSleep(69, 674)  # 向左移动
                    #     else:
                    #         Toast('已入梦，躲避梦境绮云-停留')
                    #         sleep(1.5)
                    # 已入梦，跟随梦境绮云
                    if isInYun:
                        Toast('躲避梦境绮云-移动')
                        tapSleep(69, 674)  # 向左移动
                    else:
                        Toast('躲避梦境绮云-停留')
                        sleep(1.5)

                    # 凡世侵袭 = CompareColors.compare(
                    #     "319,605,#F6F6F6|336,608,#FBFBFB|346,609,#FCFCFC|371,608,#FFFFFF|387,611,#F8F8F8")
                    # if 凡世侵袭:
                    #     if not 入梦能量空:
                    #         Toast('凡世侵袭，开始入梦')
                    #         tapSleep(423, 972)
                    #     else:
                    #         Toast('凡世侵袭，等待入梦')
                    #
                    # 梦境袭扰 = CompareColors.compare(
                    #     "313,605,#FEFEFE|323,615,#FFFFFF|341,616,#F8F8F8|367,619,#F8F8F8|392,621,#F1F1F1")
                    # if 梦境袭扰:
                    #     已入梦 = CompareColors.compare(
                    #         "418,951,#FFFFE8|421,951,#FFFFEC|410,954,#FFFFD4|427,959,#FFFFEA")
                    #     if 已入梦:
                    #         Toast('梦境袭扰，取消入梦')
                    #         tapSleep(423, 972)
                    #     else:
                    #         Toast('梦境袭扰，未入梦')
                    sleep(0.5)
                    continue

                # 绮梦晶彩龙
                if 任务记录['战斗-恶龙名称'] == '曳风晶彩龙':
                    Toast(f'曳风晶彩龙-等待走位')
                    re = FindColors.find(
                        "493,883,#E4EAEA|483,896,#EAEBEB|473,911,#EAEBEB|464,927,#EAEAEA|470,924,#EAEAEB",
                        rect=[383, 475, 699, 1153])
                    if re:
                        Toast('恶龙技能，自动走位')
                        tapSleep(69, 674)  # 向左移动

                    re = FindColors.find("313,1123,#74C33F|324,1122,#14874B|332,1125,#1F9450",
                                         rect=[62, 699, 706, 1163])
                    if re:
                        Toast('恶龙技能，自动走位')
                        tapSleep(148, 675)  # 向右移动

                    re = FindColors.find("284,1106,#DFE9DC|295,1123,#CAE9C7|312,1141,#CDE9CB|314,1155,#C9E9C5",
                                         rect=[225, 686, 702, 1191], diff=0.98)
                    if re:
                        Toast('恶龙炸地板，自动走位')
                        tapSleep(69, 674)  # 向左移动

                    re = FindColors.find("236,1081,#DAE9E9|240,1066,#E9E9E9|241,1052,#E9E9E9|247,1049,#E9E9E9",
                                         rect=[91, 694, 701, 1208], diff=0.98)
                    if re:
                        Toast('恶龙技能，自动走位')
                        tapSleep(148, 675)  # 向右移动

                    re = FindColors.find("337,822,#227342|334,827,#227446|328,834,#1A7243|320,844,#106B3D",
                                         rect=[91, 694, 701, 1208], diff=0.95)
                    if re:
                        Toast('恶龙技能，自动走位')
                        tapSleep(69, 674)  # 向左移动
                    re = FindColors.find("418,1004,#3A8675|411,1003,#388272|418,1006,#377F70",
                                         rect=[371, 926, 478, 1016], diff=0.95)
                    if re:
                        Toast('释放技能')
                        tapSleep(423, 974)  # 技能
                    sleep(0.5)
                    continue

                if '眠域' not in 任务记录['战斗-关卡名称'] and '梦境' not in 任务记录['战斗-关卡名称'] and time.time() - \
                        任务记录['战斗-上一次移动'] > 7:
                    re = imageFindClick('战斗-向左移动', x1=11, y1=565, x2=206, y2=778)
                    if re:
                        Toast('自动走位')
                    任务记录['战斗-上一次移动'] = time.time()

                if '眠域' not in 任务记录['战斗-关卡名称'] and '梦境' not in 任务记录['战斗-关卡名称'] and time.time() - \
                        任务记录['战斗-上一次移动'] > 15:
                    re = imageFindClick('战斗-向右移动', x1=11, y1=565, x2=206, y2=778)
                    if re:
                        Toast('自动走位')
                    任务记录['战斗-上一次移动'] = time.time()
