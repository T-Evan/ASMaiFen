# __init__.py 为初始化加载文件
# 导入-节点检索库
import json
import time

from ascript.android.system import R
# 导入-屏幕检索库
from ascript.android.ui import WebWindow
from ascript.android.ui import Dialog
import threading
import sys
from ascript.android import system

config = None


def tunner(k, v):
    global config
    print(k, v)
    print(k)
    print(v)

    if k == "guan" and v == "关闭":
        config = "exit"
    if k == "submit":
        res = json.loads(v)
        config = res
        # print(type(config))
    if k == "加载" and v == "成功":
        print('加载成功')


formW = WebWindow(R.ui("ui.html"))
formW.size('100vw', '100vh')
formW.tunner(tunner)  # 在这里设置消息通道
formW.background("#FFFFFF")
formW.show()
from threading import Lock

while True:
    print("循环等待中")
    time.sleep(1)
    if config == "exit":
        Dialog.toast('取消执行', 5, 3 | 48, 200, 0)
        system.exit()
    if config:
        Dialog.toast('资源加载中 - 请等待30s', 5, 3 | 48, 200, 0)
        # time.sleep(2)
        break

import time

class TimeoutLock:
    def __init__(self, timeLock = 10):
        self.lock = switch_lock
        self.timeout = timeLock

    def acquire_lock(self):
        start_time = time.time()
        while (time.time() - start_time) < self.timeout:
            if self.lock.acquire(False):
                return True
            time.sleep(0.2)
        print(f"尝试获取锁超时，耗时: {time.time() - start_time} 秒")
        return False

    def release_lock(self):
        self.lock.release()

    def __enter__(self):
        if not self.acquire_lock():
            raise RuntimeError("无法在指定时间内获取锁")
        # print("锁已成功获取")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release_lock()
        # print("锁已成功释放")

# 初始化锁
global switch_lock
switch_lock = Lock()
global switch_ocr_apk_lock # apk ocr 识别锁
switch_ocr_apk_lock = Lock()
功能开关 = {}
功能开关 = config
功能配置 = {'配置1': config['配置1'], '配置2': config['配置2'], '配置3': config['配置3'], '配置4': config['配置4'],
            '配置5': config['配置5']}

def loadConfig(configNum):
    global 功能开关
    configName = '配置'+ str(configNum)
    new = json.loads(功能配置[configName])
    for index, value in new.items():
        if value == 'false':
            value = False
        if value == 'true':
            value = True
        功能开关[index] = value
    # print(222)
    # 功能开关 = new
    print(功能开关)
    return 功能开关

# thread_main_paused = False
# thread_main_cond = threading.Condition()

任务记录 = {
    "当前任务账号": 功能开关["选择启动账号"],
    "当前任务角色": 功能开关["选择启动角色"],
}

def 初始化任务记录(initAll=True):
    # 日常
    任务记录.update({
        "首页卡死检测-倒计时": 0,

        "仓鼠百货-完成": 0,
        "邮件领取-完成": 0,
        "寻找结伴-完成": 0,
        "大暴走-完成": 0,

        "冒险手册-倒计时": 0,
    })

    # 旅团
    任务记录.update({
        "旅团-浇树-完成": 0,
        "旅团-调查队-完成": 0,
        "旅团-许愿墙-完成": 0,
        "旅团-任务-完成": 0,
        "旅团-商店-完成": 0,
    })

    # 旅人
    任务记录.update({
        "强化装备-倒计时": 0,
        "分解装备-倒计时": 0,
        "更换装备-倒计时": 0,
        "技能升级-倒计时": 0,

        "旅人-猫猫果木-完成": 0,
        "日常-招式创造-完成": 0,
        "日常-骑兽乐园-完成": 0,
        "日常-释放1次战术技能-完成": 0,

        "日常-升级1次麦乐兽-完成": 0,
        "试炼-秘境-体力消耗完成": 0,
        "试炼-恶龙-完成次数": 0,
        "日常-宝藏湖-完成": 0,
    })

    if initAll:
        任务记录.update({"日常-洗练1次装备-完成": 0,})

    # 营地
    任务记录.update({
        "月签到-完成": 0,
        "月卡-完成": 0,
        "日礼包-完成": 0,
        "露营打卡点-完成": 0,
        "舞会签到簿-完成": 0,
        "纸飞机-完成": 0,
        "星辰同行-完成": 0,
        "秘宝领取-完成": 0,
        "限时特惠-完成": 0,
        "登录好礼-完成": 0,
        "箱庭苗圃-倒计时": 0,
        "箱庭苗圃-完成": 0,
        "派对大师-完成": 0,
        "队伍喊话-倒计时": 0,
        "世界喊话-倒计时": 0,
    })
