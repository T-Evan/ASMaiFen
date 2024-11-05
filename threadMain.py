import threading
from .child_main import mainTask as mainTask
from .res.ui.ui import 功能开关
from .child_mijing_team import main as mijing_team
from .child_another_login import main as another_login
from java.lang import Runnable, Thread
from java import dynamic_proxy

# 子协程处理弹窗
# threadMain = threading.Thread(target=mainTask, daemon=True)
# threadMijingTeam = threading.Thread(target=mijing_team, daemon=True)
# threadAnotherLogin = threading.Thread(target=another_login, daemon=True)

class RunThreadMijingTeam(dynamic_proxy(Runnable)):
    def __init__(self):
        super().__init__()
    def run(self):
        print("启动自动入队处理线程")
        mijing_team()

class RunThreadAnotherLogin(dynamic_proxy(Runnable)):
    def __init__(self):
        super().__init__()
    def run(self):
        print("启动顶号等待处理线程")
        another_login()
#
# class RunThreadCheckBlock(dynamic_proxy(Runnable)):
#     def __init__(self):
#         super().__init__()
#     def run(self):
#         print("启动卡死检测线程")
#         check_block()

# def runThreadMain():
#     try:
#         if not threadMain.is_alive():
#             threadMain.start()
#     except RuntimeError as e:
#         print(f"ThreadMain Error: {e}")


def runThreadMijingTeam():
    if 功能开关["秘境自动接收邀请"] == 1 or 功能开关['梦魇自动接收邀请'] == 1 or 功能开关['恶龙自动接收邀请'] == 1 or 功能开关['暴走自动接收邀请'] == 1 or 功能开关['终末战自动接收邀请'] == 1 or 功能开关['绝境自动接收邀请'] == 1 or 功能开关['调查队自动接收邀请'] == 1:
        try:
            r = RunThreadMijingTeam()
            t = Thread(r)
            t.start()
        except RuntimeError as e:
            print(f"自动入队处理线程 Error: {e}")
        # try:
        #     if not threadMijingTeam.is_alive():
        #         threadMijingTeam.start()
        # except RuntimeError as e:
        #     print(f"自动入队处理线程 Error: {e}")

def runThreadAnotherLogin():
    if 功能开关["顶号等待"] != "" and 功能开关["顶号等待"] != "0":
        try:
            r = RunThreadAnotherLogin()
            t = Thread(r)
            t.start()
        except RuntimeError as e:
            print(f"顶号等待处理线程 Error: {e}")
        # try:
        #     if not threadAnotherLogin.is_alive():
        #         threadAnotherLogin.start()
        # except RuntimeError as e:
        #     print(f"ThreadAnotherLogin Error: {e}")

# def runThreadCheckBlock():
#     try:
#         r = RunThreadCheckBlock()
#         t = Thread(r)
#         t.start()
#     except RuntimeError as e:
#         print(f"卡死检测线程 Error: {e}")