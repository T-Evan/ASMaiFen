import threading
from .child_notice import main as notice_main
from .child_return_home import main as return_home_main
from .child_baozou import main as bao_zou_boss

# 子协程处理弹窗
thread1 = threading.Thread(target=notice_main, daemon=True)
thread2 = threading.Thread(target=return_home_main, daemon=True)
threadBaoZouBoss = threading.Thread(target=bao_zou_boss, daemon=True)

def runThread1():
    if not thread1.is_alive():
        thread1.start()

def runThread2():
    if not thread2.is_alive():
        thread2.start()

def runThreadBaoZouBoss():
    if not threadBaoZouBoss.is_alive():
        threadBaoZouBoss.start()
