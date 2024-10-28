# 导包
from ascript.android import system

from .特征库 import *
from ascript.android.ui import Dialog
from .baseUtils import *
from .res.ui.ui import 功能开关


# 实例方法
def main():
    if 功能开关["顶号等待"] != "" and 功能开关["顶号等待"] != "0":
        while True:
            anotherLogin()
            sleep(10)

def anotherLogin():
    res, _ = TomatoOcrText(311, 588, 408, 637, "异地登录")
    if res:
        print("顶号等待，检查被顶号")
        start_time = int(time.time())
        need_another_minute = safe_int(功能开关.get("顶号等待", 0))  # 分钟
        if need_another_minute == '':
            need_another_minute = 0
        total_another_minute = need_another_minute * 60
        while True:
            功能开关["needHome"] = 0
            功能开关["fighting"] = 1
            current_time = int(time.time())
            if total_another_minute != 0 and current_time - start_time >= total_another_minute:
                tapSleep(320, 760, 0.5)
                tapSleep(320, 760, 0.5)
                res = TomatoOcrTap(320, 760, 396, 798, "确认")
                res = TomatoOcrTap(320, 760, 396, 798, "确认")
                res = TomatoOcrTap(320, 760, 396, 798, "确认")
                Toast("顶号等待，开始重新登录")
                for i in range(1, 5):
                    login()
                    sleep(4)
                    功能开关["fighting"] = 0
                    sleep(30)
                break
            tmpMinute = (current_time - start_time) / 60
            tmpDiffMinute = (total_another_minute - (current_time - start_time)) / 60
            Toast(f"顶号等待，已等待{tmpMinute}分钟/剩余等待{tmpDiffMinute}分钟")
            tapSleep(505,667)  # 点击防止进入房车动画页
            sleep(10)  # 等待
    else:
        # login()
        print("顶号等待，检查状态正常")

    return


def login():
    功能开关["needHome"] = 0
    功能开关["fighting"] = 1
    sleep(1.5)
    # 开始冒险之旅
    login1 = TomatoOcrTap(282, 1017, 437, 1051, "开始冒险之旅")
    # 开始冒险
    login2 = TomatoOcrTap(302, 1199, 414, 1231, "开始冒险")
    # 跳过启动动画
    if login2:
        tapSleep(340, 930, 1)
        tapSleep(340, 930, 1)
        tapSleep(340, 930)
        sleep(5)
