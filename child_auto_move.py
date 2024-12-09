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
                        return

                # 恶龙红圈
                re = FindColors.find("211,1018,#EA1F1B|214,1025,#EA3020|215,1020,#E71919|210,1020,#EA281D",
                                     rect=[118, 894, 503, 1052], diff=0.9)
                if re:
                    re = imageFindClick('战斗-向左移动', x1=11, y1=565, x2=206, y2=778)
                    if re:
                        Toast('boss技能，自动走位')

                if time.time() - 任务记录['战斗-上一次移动'] > 7:
                    re = imageFindClick('战斗-向左移动', x1=11, y1=565, x2=206, y2=778)
                    if re:
                        Toast('自动走位')
                    任务记录['战斗-上一次移动'] = time.time()
