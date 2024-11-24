# 导包
from ascript.android import system

from .特征库 import *
from ascript.android.ui import Dialog
from .baseUtils import *
from .res.ui.ui import 功能开关
from ascript.android.screen import Colors

lastColorNum = 0
failTimes = 0


# 识别屏幕是否卡死
def main():
    while True:
        checkBlock()
        sleep(10)

def checkBlock():
    global failTimes
    global lastColorNum
    currColorNum = Colors.count("#000000-#FFFFFF", rect=[151, 129, 570, 377])
    print(currColorNum)
    if currColorNum == lastColorNum:
        failTimes = failTimes + 1
        Toast(f'检测到屏幕无变动{failTimes}/6')
    else:
        lastColorNum = currColorNum
        failTimes = 0

    # 1分钟内屏幕颜色无变化
    if failTimes > 6:
        Toast("识别到屏幕卡死，重启脚本")
        # 结束应用
        # r = system.shell("am kill com.xd.cfbmf")
        r = system.shell(f"am force-stop {功能开关['游戏包名']}")
        system.open(f"{功能开关['游戏包名']}")
        failTimes = 0
