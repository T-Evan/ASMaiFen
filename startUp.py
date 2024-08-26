# 导包
from ascript.android import system
from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .res.ui.ui import switch_lock
from .baseUtils import *

class StartUp:
    # 构造器
    def __init__(self, app_name):
        self.app_name = app_name

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
        login1, _ = TomatoOcrText(282, 1017, 437, 1051, "开始冒险之旅")
        login2, _ = TomatoOcrText(302, 1199, 414, 1231, "开始冒险")
        if login1 or login2:
            Toast('准备进入游戏')
            return self.login()
        else:
            # 不在登录页，尝试开始返回首页
            with switch_lock:
                功能开关["needHome"] = 1

        # 识别是否进入首页
        res2,_ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
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

        ldE.sleep(3)  # 等待游戏启动

        return self.start_app()


    def login(self):
        with switch_lock:
            功能开关["needHome"] = 0
        ldE.sleep(1.5)
        # 开始冒险之旅
        login1, _ = TomatoOcrText(282, 1017, 437, 1051, "开始冒险之旅")
        # login1 = ldE.element_exist('登录页-开始冒险之旅')
        if login1:
            login1.click_element().execute(sleep=1)

        # 开始冒险
        login2, _ = TomatoOcrText(302, 1199, 414, 1231, "开始冒险")
        # login2 = ldE.element_exist('登录页-开始冒险')
        if login2:
        #     todo：切换角色
            login2.click_element().execute(sleep=1)
        if not login1 and not login2:
            return self.start_app()

        # 跳过启动动画
        if login2:
            ldE.click('50%', '50%', 7)
            ldE.sleep(1)
            ldE.click('50%', '50%', 7)
            ldE.sleep(1)
            ldE.click('50%', '50%', 7)
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

