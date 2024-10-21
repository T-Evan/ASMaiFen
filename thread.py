import threading
from .child_notice import main as notice_main
from .child_return_home import main as return_home_main
from .child_baozou import main as bao_zou_boss
from .res.ui.ui import 功能开关
import multiprocessing
from java.lang import Runnable, Thread
from java import dynamic_proxy

# 子协程处理弹窗

class RunThreadNotice(dynamic_proxy(Runnable)):
    def __init__(self):
        super().__init__()
    def run(self):
        print("启动空白弹窗处理线程")
        notice_main()

class RunThreadReturnHome(dynamic_proxy(Runnable)):
    def __init__(self):
        super().__init__()
    def run(self):
        print("启动返回首页处理线程")
        return_home_main()

class RunThreadDaBaoZou(dynamic_proxy(Runnable)):
    def __init__(self):
        super().__init__()
    def run(self):
        print("启动大暴走处理线程")
        bao_zou_boss()
def runThreadNotice():
    try:
        r = RunThreadNotice()
        t = Thread(r)
        t.start()
    except RuntimeError as e:
        print(f"空白弹窗处理线程 Error: {e}")
    # thread1 = threading.Thread(target=notice_main, daemon=True)
    # processNotice = multiprocessing.Process(target=notice_main)
    # try:
    #     if not thread1.is_alive():
    #         thread1.start()
    # except RuntimeError as e:
    #     print(f"空白弹窗处理线程异常: {e}")
    # try:
    #     if not processNotice.is_alive():
    #         processNotice.start()
    # except Exception as e:
    #     print(f"Caught exception from child process: {e}")


def runThreadReturnHome():
    try:
        r = RunThreadReturnHome()
        t = Thread(r)
        t.start()
    except RuntimeError as e:
        print(f"返回首页处理线程 Error: {e}")
    # thread2 = threading.Thread(target=return_home_main, daemon=True)
    # try:
    #     if not thread2.is_alive():
    #         thread2.start()
    # except RuntimeError as e:
    #     print(f"Thread2 Error: {e}")


def runThreadBaoZouBoss():
    if 功能开关["大暴走开关"] == 1:
        try:
            r = RunThreadDaBaoZou()
            t = Thread(r)
            t.start()
        except RuntimeError as e:
            print(f"大暴走处理线程 Error: {e}")
        # threadBaoZouBoss = threading.Thread(target=bao_zou_boss, daemon=True)
        # try:
        #     if not threadBaoZouBoss.is_alive():
        #         threadBaoZouBoss.start()
        # except RuntimeError as e:
        #     print(f"ThreadBoss Error: {e}")
