# __init__.py 为初始化加载文件
# 导入-节点检索库
import json
import time

from ascript.android.system import R
# 导入-屏幕检索库
from ascript.android.ui import WebWindow
from ascript.android.ui import Dialog

config = None


def tunner(k, v):
    global config
    print(k, v)
    print(k)
    print(v)

    if k == "guan" and v == "关闭":
        R.exit()
    if k == "submit":
        res = json.loads(v)
        config = res
        print(type(config))
    if k == "加载" and v == "成功":
        print(v)


formW = WebWindow(R.ui("ui.html"))
formW.size('100vw', '100vh')
formW.tunner(tunner)  # 在这里设置消息通道
formW.background("#FFFFFF")
formW.show()
from threading import Lock

while True:
    print("循环等待中")
    time.sleep(1)
    if config:
        Dialog.toast('资源加载中 - 请等待30s', 5, 3 | 48, 200, 0)
        break

import time

class TimeoutLock:
    def __init__(self, lock, timeout = 10):
        self.lock = lock
        self.timeout = timeout
        self.start_time = None

    def acquire_lock(self):
        start_time = time.time()
        while (time.time() - start_time) < self.timeout:
            if self.lock.acquire(False):
                return True
            time.sleep(0.1)
        print(f"尝试获取锁超时，耗时: {time.time() - start_time} 秒")
        return False

    def release_lock(self):
        self.lock.release()

# 初始化锁
global switch_lock
switch_lock = Lock()
global switch_ocr_apk_lock # apk ocr 识别锁
switch_ocr_apk_lock = Lock()
global 功能开关
功能开关 = config

任务记录 = {
    "当前任务账号": 功能开关["选择启动账号"],
    "当前任务角色": 功能开关["选择启动角色"],
}

def 初始化任务记录():
    # 日常
    任务记录.update({
        "仓鼠百货-完成": 0,
        "邮件领取-完成": 0,
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
        "旅人-猫猫果木-完成": 0,
        "日常-招式创造-完成": 0,
        "日常-骑兽乐园-完成": 0,
        "试炼-秘境-体力消耗完成": 0,
        "试炼-恶龙-完成次数": 0,
    })

    # 营地
    任务记录.update({
        "月签到-完成": 0,
        "月卡-完成": 0,
        "日礼包-完成": 0,
        "露营打卡点-完成": 0,
    })
