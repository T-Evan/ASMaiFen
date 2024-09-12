# 导包
from ascript.android import system

from .特征库 import *
from ascript.android.ui import Dialog
from .baseUtils import *
from .res.ui.ui import 功能开关
from .shilian import ShiLianTask

shilianTask = ShiLianTask()

# 实例方法
def main():
    if 功能开关["冒险总开关"] == 1 and 功能开关["秘境自动接收邀请"] == 1:
        while True:
            sleep(5)  # 等待 5 秒
            Toast('等待组队邀请')
            waitInvite()


def waitInvite():
    功能开关["fighting"] = 1
    tmpBx = 功能开关["秘境不开宝箱"]
    功能开关["秘境不开宝箱"] = 1
    res1 = TomatoOcrTap(584, 651, 636, 678, "同意")
    res2, _ = TomatoOcrText(457, 607, 502, 631, "准备")  # 秘境准备
    # 判断体力用尽提示
    res3, _ = TomatoOcrText(242, 598, 314, 616, "体力不足")
    if res3:
        if 功能开关["秘境无体力继续"]:
            Toast("秘境任务 - 体力不足继续挑战")
            res = TomatoOcrTap(334, 743, 385, 771, "确定")

    if not res1 and not res2:
        quitTeamRe = shilianTask.quitTeam()
        功能开关["fighting"] = 0
        功能开关["秘境不开宝箱"] = tmpBx
        return

    if res1:
        Toast('接受组队邀请')

    waitFight = False
    for i in range(1, 4):
        waitTime = (i - 1) * 10
        Toast(f'等待队长开始{waitTime}/30s')
        sleep(5)
        waitFight = shilianTask.WaitFight()
        if waitFight:
            break
        sleep(5)
    if not waitFight:
        Toast(f'等待进入战斗超时，退出组队')

    quitTeamRe = shilianTask.quitTeam()
    功能开关["fighting"] = 0
    功能开关["秘境不开宝箱"] = tmpBx

    return
