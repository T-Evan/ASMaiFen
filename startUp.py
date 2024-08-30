# 导包
from ascript.android import system
from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .res.ui.ui import 任务记录
from .res.ui.ui import switch_lock
from .baseUtils import *
from .shilian import ShiLianTask


class StartUp:
    # 构造器
    def __init__(self, app_name):
        self.app_name = app_name
        self.shilianTask = ShiLianTask()

    # 实例方法
    def start_app(self):
        global 功能开关

        system.open(self.app_name)
        # re = ldE.element_exist('启动应用')
        # if re:
        #     ldE.element('启动应用-允许').click_element().execute()
        # else:
        Toast('启动游戏，等待加载中')

        # 识别是否进入登录页
        login1 = TomatoOcrTap(282, 1017, 437, 1051, "开始冒险之旅")
        login2 = TomatoOcrTap(302, 1199, 414, 1231, "开始冒险")
        if login1 or login2:
            Toast('准备进入游戏')
            return self.login()
        else:
            # 不在登录页，尝试开始返回首页
            with switch_lock:
                功能开关["needHome"] = 1

        # 识别是否进入首页
        res2, _ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
        shou_ye1 = False
        shou_ye2 = False
        if not res2:
            shou_ye1 = ldE.element_exist('首页-冒险手册')
            if not shou_ye1:
                shou_ye2 = ldE.element_exist('首页-新手试炼')
        if res2 or shou_ye1 or shou_ye2:
            with switch_lock:
                功能开关["needHome"] = 0
            Toast('已进入游戏')
            return True

        # 识别是否战斗中
        res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
        res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
        res1, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")
        if res1 or (teamName1 != "" or teamName2 != ""):  # 战斗中
            # 大暴走战斗中
            if 功能开关["暴走进入战斗后启动"] == 1:
                Toast("进入暴走战斗成功 - 开始战斗")
                self.shilianTask.fightingBaoZou()
                return

        ldE.sleep(3)  # 等待游戏启动

        return self.start_app()

    def login(self):
        with switch_lock:
            功能开关["needHome"] = 0
        ldE.sleep(1.5)
        # 开始冒险之旅
        login1 = TomatoOcrTap(282, 1017, 437, 1051, "开始冒险之旅")
        # login1 = ldE.element_exist('登录页-开始冒险之旅')
        # if login1:
        #     login1.click_element().execute(sleep=1)

        # 开始冒险
        login2 = TomatoOcrTap(302, 1199, 414, 1231, "开始冒险")
        # login2 = ldE.element_exist('登录页-开始冒险')
        # if login2:
        #     todo：切换角色
        #     login2.click_element().execute(sleep=1)
        if not login1 and not login2:
            return self.start_app()

        # 跳过启动动画
        if login2:
            tapSleep(340, 930, 1)
            tapSleep(340, 930, 1)
            tapSleep(340, 930)
            ldE.sleep(5)
        else:
            return self.start_app()

        shou_ye = False
        for loopCount in range(1, 4):  # 循环3次，从1到3
            shou_ye1 = ldE.element_exist('首页-冒险手册')
            shou_ye2 = ldE.element_exist('首页-新手试炼')
            if shou_ye1 or shou_ye2:
                Toast('已进入游戏')
                shou_ye = True
                break
            ldE.sleep(3)  # 等待 3 秒

        if not shou_ye:
            return self.start_app()

        return shou_ye

    def switchRole(self, selectRole, ifRestart=1):
        功能开关['fighting'] = 0
        功能开关['needHome'] = 0
        Toast('开始切换角色')

        if ifRestart == 1:
            system.reboot('com.xd.cfbmf')  # 重启应用让配置生效

        下一角色 = 任务记录['当前任务角色'] + 1
        if selectRole != '':
            selectRole = safe_int(selectRole)
            if selectRole == '':
                return

        if 下一角色 > 5:
            下一角色 = 1

        角色开关 = '角色' + 下一角色 + '开关'
        if 功能开关[角色开关] == 0:
            任务记录['当前任务角色'] = 下一角色
            return self.switchRole(2)

        res = TomatoOcrText(302, 1199, 414, 1231, "开始冒险")
        if res == False:
            res5 = TomatoOcrTap(171, 1189, 200, 1216, "回")
            res6 = TomatoOcrTap(98, 1202, 128, 1231, "回")
            res7 = TomatoOcrTap(93, 1186, 127, 1217, "回")

        res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
        # dialog(下一角色)
        if 下一角色 <= 3:
            ldE.swipe([190, 1090], [555, 1090])  # 翻到最左
            ldE.sleep(3)
            x = 190 + (下一角色 - 1) * 165  # 从第一个角色 190，依次往右加 165 至下一角色
            y = 1090
            tapSleep(x, y)
            res = TomatoOcrText(300, 1197, 420, 1232, "选择职业")
            if res:
                # 无该角色，退出
                res = TomatoOcrTap(70, 1198, 125, 1232, "返回")
                任务记录['当前任务角色'] = 0
                return self.switchRole(2)

        if 下一角色 > 3:
            ldE.swipe([555, 1090], [190, 1090])  # 翻到最右
            ldE.sleep(3)
            x = 540 - (5 - 下一角色) * 165  # 从第五个角色 540，依次往左减 165 至下一角色
            y = 1090
            tapSleep(x, y)
            res = TomatoOcrText(300, 1197, 420, 1232, "选择职业")
            if res:
                # 无该角色，退出
                res = TomatoOcrTap(70, 1198, 125, 1232, "返回")
                任务记录['当前任务角色'] = 0
                return self.switchRole(2)
        任务记录['当前任务角色'] = 下一角色
