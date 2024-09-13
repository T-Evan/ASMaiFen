import threading
from .child_main import mainTask as mainTask
from .res.ui.ui import 功能开关
from .child_mijing_team import main as mijing_team
from .child_another_login import main as another_login

# 子协程处理弹窗
threadMain = threading.Thread(target=mainTask, daemon=True)
threadMijingTeam = threading.Thread(target=mijing_team, daemon=True)
threadAnotherLogin = threading.Thread(target=another_login, daemon=True)

def runThreadMain():
    try:
        if not threadMain.is_alive():
            threadMain.start()
    except RuntimeError as e:
        print(f"ThreadMain Error: {e}")


def runThreadMijingTeam():
    if 功能开关["冒险总开关"] == 1 and 功能开关["秘境自动接收邀请"] == 1:
        try:
            if not threadMijingTeam.is_alive():
                threadMijingTeam.start()
        except RuntimeError as e:
            print(f"ThreadMijingTeam Error: {e}")

def runThreadAnotherLogin():
    if 功能开关["顶号等待"] != "" and 功能开关["顶号等待"] != "0":
        try:
            if not threadAnotherLogin.is_alive():
                threadAnotherLogin.start()
        except RuntimeError as e:
            print(f"ThreadAnotherLogin Error: {e}")
