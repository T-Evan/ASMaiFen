# 导包
from ascript.android import system
from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .res.ui.ui import 任务记录
from .res.ui.ui import switch_lock
from .baseUtils import *
from .shilian import ShiLianTask
from .daily import DailyTask
import shutil
import os
import sys

class StartUp:
    # 构造器
    def __init__(self, app_name):
        self.app_name = app_name
        self.shilianTask = ShiLianTask()
        self.dailyTask = DailyTask()

    # 实例方法
    def start_app(self):
        global 功能开关

        system.open(self.app_name)

        max_attempt = 15
        for attempt in range(max_attempt):
            # 识别是否进入登录页
            login1, _ = TomatoOcrText(282, 1017, 437, 1051, "开始冒险之旅")
            login2, _ = TomatoOcrText(302, 1199, 414, 1231, "开始冒险")
            if login1 or login2:
                Toast('准备进入游戏')
                return self.login()
            else:
                re = TomatoOcrTap(330, 1201, 389, 1238, '冒险')
                if not re:
                    # 不在登录页，尝试开始返回首页
                    功能开关["needHome"] = 1

            # 识别是否进入首页
            res2, _ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
            shou_ye1 = False
            shou_ye2 = False
            if not res2:
                shou_ye1 = TomatoOcrFindRange('冒险手册', 0.9, 360, 0, 720, 1280, '冒险手册')
                if not shou_ye1:
                    shou_ye2 = TomatoOcrFindRange('试炼', 0.9, 360, 0, 720, 1280, '试炼')
            if res2 or shou_ye1 or shou_ye2:
                # 避免首页识别到冒险手册，但存在未关闭的返回弹窗；兜底识别1次
                return3 = TomatoOcrTap(91, 1185, 127, 1221, '回', 10, 10)
                if return3:
                    Toast('返回首页')

                功能开关["needHome"] = 0
                Toast('已进入游戏')
                return True
            else:
                # 不在首页，尝试开始返回首页
                # 开始异步处理返回首页
                功能开关["needHome"] = 1

            # 识别是否战斗中
            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
            res1, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")
            if res1 or (teamName1 != "" or teamName2 != ""):  # 战斗中
                # 大暴走战斗中
                if 功能开关["大暴走开关"] == 1 and 功能开关["暴走进入战斗后启动"] == 1:
                    Toast("进入暴走战斗成功 - 开始战斗")
                    self.shilianTask.fightingBaoZou()
                    return

            Toast('启动游戏，等待加载中')

            sleep(3)  # 等待游戏启动
        print('启动游戏失败，超过最大尝试次数')

    def login(self):
        功能开关["needHome"] = 0
        sleep(1.5)
        # 开始冒险之旅
        login1 = TomatoOcrTap(282, 1017, 437, 1051, "开始冒险之旅")
        # login1 = ldE.element_exist('登录页-开始冒险之旅')
        # if login1:
        #     login1.click_element().execute(sleep=1)

        # 开始冒险
        login2, _ = TomatoOcrText(302, 1199, 414, 1231, "开始冒险")
        if login2:
            self.switchRole(2, 任务记录['当前任务角色'])
        if not login1 and not login2:
            return self.start_app()

        login2 = TomatoOcrTap(302, 1199, 414, 1231, "开始冒险")

        # 跳过启动动画
        if login2:
            tapSleep(340, 930, 1)
            tapSleep(340, 930, 1)
            tapSleep(340, 930)
            sleep(5)
        else:
            return self.start_app()

        shou_ye = False
        for loopCount in range(1, 4):  # 循环3次，从1到3
            shou_ye1 = TomatoOcrFindRange('冒险手册', 0.9, 360, 0, 720, 1280, '冒险手册')
            shou_ye2 = TomatoOcrFindRange('试炼', 0.9, 360, 0, 720, 1280, '试炼')
            # 避免首页识别到冒险手册，但存在未关闭的返回弹窗；兜底识别1次
            return3 = TomatoOcrTap(91, 1185, 127, 1221, '回', 10, 10)
            if return3:
                Toast('返回首页')
            if shou_ye1 or shou_ye2:
                Toast('已进入游戏')
                shou_ye = True
                break
            sleep(3)  # 等待 3 秒

        if not shou_ye:
            return self.start_app()

        return shou_ye

    def switchRole(self, ifRestart=1, selectRole=''):
        功能开关['fighting'] = 0
        功能开关['needHome'] = 0
        Toast('开始切换角色')

        # if ifRestart == 1:
        #     system.reboot()  # 重启应用让配置生效

        # 判断是否在角色切换页
        login1 = TomatoOcrTap(282, 1017, 437, 1051, "开始冒险之旅")
        login2, _ = TomatoOcrText(302, 1199, 414, 1231, "开始冒险")
        if not login1 and not login2:
            self.dailyTask.homePage()
            res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
            tapSleep(47, 340)
            res = TomatoOcrTap(135, 741, 222, 774, "返回主界面", 10, 10)
            if res:
                sleep(5)
                for i in range(1, 6):
                    login1 = TomatoOcrTap(282, 1017, 437, 1051, "开始冒险之旅")
                    if login1:
                        break
                    sleep(5)
            else:
                Toast('返回登录界面失败，跳过角色切换')
                return

        任务记录['当前任务角色'] = safe_int(任务记录['当前任务角色'])
        下一角色 = 任务记录['当前任务角色'] + 1
        if selectRole != '':
            selectRole = safe_int(selectRole)
            下一角色 = selectRole
            if selectRole == '' or selectRole == 0:
                return

        if 下一角色 > 5:
            下一角色 = 1

        角色开关 = '角色' + str(下一角色) + '开关'
        if 功能开关[角色开关] == 0:
            Toast(角色开关 + '-未开启')
            任务记录['当前任务角色'] = 下一角色
            return self.switchRole(2)

        Toast('切换角色' + str(下一角色))
        res, _ = TomatoOcrText(302, 1199, 414, 1231, "开始冒险")
        if res == False:
            res5 = TomatoOcrTap(171, 1189, 200, 1216, "回")
            res6 = TomatoOcrTap(98, 1202, 128, 1231, "回")
            res7 = TomatoOcrTap(93, 1186, 127, 1217, "回")

        res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
        # dialog(下一角色)
        if 下一角色 <= 3:
            swipe(190, 1090, 555, 1090)  # 翻到最左
            sleep(3)
            x = 190 + (下一角色 - 1) * 165  # 从第一个角色 190，依次往右加 165 至下一角色
            y = 1090
            tapSleep(x, y)
            res, _ = TomatoOcrText(300, 1197, 420, 1232, "选择职业")
            if res:
                # 无该角色，退出
                res = TomatoOcrTap(70, 1198, 125, 1232, "返回")
                任务记录['当前任务角色'] = 0
                return self.switchRole(2)

        if 下一角色 > 3:
            swipe(555, 1090, 190, 1090)  # 翻到最右
            sleep(3)
            x = 540 - (5 - 下一角色) * 165  # 从第五个角色 540，依次往左减 165 至下一角色
            y = 1090
            tapSleep(x, y)
            res, _ = TomatoOcrText(300, 1197, 420, 1232, "选择职业")
            if res:
                # 无该角色，退出
                res = TomatoOcrTap(70, 1198, 125, 1232, "返回")
                任务记录['当前任务角色'] = 0
                return self.switchRole(2)
        任务记录['当前任务角色'] = 下一角色

    def saveAccount(self, account_name):
        account_name = str(account_name)
        old_path1 = "/data/data/com.xd.cfbmf/shared_prefs/"
        new_path1 = "/data/data/com.xd.cfbmf/shared_prefs/accountConfig" + account_name + "_shared_prefs"

        print(11111111)
        # 删除文件夹
        shutil.rmtree(new_path1, ignore_errors=True)
        print(22222222)
        # 新建文件夹
        os.makedirs(new_path1, exist_ok=True)
        print(33333333)
        # 复制文件夹
        flag1 = shutil.copytree(old_path1, new_path1, dirs_exist_ok=True)
        print(444444444)

        old_path2 = "/data/data/com.xd.cfbmf/app_webview/"
        new_path2 = "/data/data/com.xd.cfbmf/shared_prefs/accountConfig" + account_name + "_app_webview"

        # 删除文件夹
        shutil.rmtree(new_path2, ignore_errors=True)
        # 新建文件夹
        os.makedirs(new_path2, exist_ok=True)
        # 复制文件夹
        flag2 = shutil.copytree(old_path2, new_path2, dirs_exist_ok=True)

        # 复制文件夹及里面所有文件
        if flag1 and flag2:
            Dialog.confirm(f"已保存账号 {account_name} 登录信息！请重启软件")
        else:
            Dialog.confirm("保存失败！请联系作者")
        sys.exit()
        return True  # 这里返回True可能不会被执行到，
