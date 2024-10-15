import threading
from .child_notice import main as notice_main
from .child_return_home import main as return_home_main
from .child_baozou import main as bao_zou_boss
from .res.ui.ui import 功能开关
import multiprocessing

# 子协程处理弹窗
thread1 = threading.Thread(target=notice_main, daemon=True)
processNotice = multiprocessing.Process(target=notice_main)
thread2 = threading.Thread(target=return_home_main, daemon=True)
threadBaoZouBoss = threading.Thread(target=bao_zou_boss, daemon=True)


def runThread1():
    try:
        if not thread1.is_alive():
            thread1.start()
    except RuntimeError as e:
        print(f"空白弹窗处理线程异常: {e}")
    # try:
    #     if not processNotice.is_alive():
    #         processNotice.start()
    # except Exception as e:
    #     print(f"Caught exception from child process: {e}")


def runThread2():
    try:
        if not thread2.is_alive():
            thread2.start()
    except RuntimeError as e:
        print(f"Thread2 Error: {e}")


def runThreadBaoZouBoss():
    if 功能开关["大暴走开关"] == 1:
        try:
            if not threadBaoZouBoss.is_alive():
                threadBaoZouBoss.start()
        except RuntimeError as e:
            print(f"ThreadBoss Error: {e}")
