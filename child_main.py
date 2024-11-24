# 导包
from time import sleep
from .res.ui.ui import 功能开关
from .baseUtils import *
from ascript.android import action
from .shilian import ShiLianTask
from .lvtuan import LvTuanTask
from .lvren import LvRenTask
from .startUp import StartUp
from .yingdi import YingDiTask
from .daily import DailyTask
from .res.ui.ui import 功能开关
from .res.ui.ui import 初始化任务记录
from .baseUtils import *
from .thread import *
import time
from ascript.android.ui import Dialog
from ascript.android.system import Device
import sys
import traceback


def mainTask():
    start_up = StartUp(f"{功能开关['游戏包名']}")
    yingdiTask = YingDiTask()
    dailyTask = DailyTask()
    lvrenTask = LvRenTask()
    lvtuanTask = LvTuanTask()
    shilianTask = ShiLianTask()

    # debug
    # start_up.saveAccount(2)
    # sys.exit()

    功能开关["breakChild"] = 0
    功能开关["fighting"] = 0
    功能开关["needHome"] = 0

    # 处理休息时间
    need_run_minute = safe_int(功能开关.get("定时运行", 0))  # 分钟
    if need_run_minute == '':
        need_run_minute = 0
    need_wait_minute = safe_int(功能开关.get("定时休息", 0))  # 分钟
    if need_wait_minute == '':
        need_wait_minute = 0
    need_switch_account_minute = safe_int(功能开关.get("定时切号", 0))  # 分钟
    if need_switch_account_minute == '':
        need_switch_account_minute = 0
    need_switch_role_minute = safe_int(功能开关.get("定时切角色", 0))  # 分钟
    if need_switch_role_minute == '':
        need_switch_role_minute = 0

    total_wait = need_run_minute * 60
    total_switch_account_minute = need_switch_account_minute * 60
    total_switch_role_minute = need_switch_role_minute * 60

    start_time = int(time.time())

    runThreadNotice()
    runThreadReturnHome()
    runThreadBaoZouBoss()
    counter = 0

    global thread_main_paused
    global thread_main_cond
    while True:
        with thread_main_cond:
            while thread_main_paused:
                thread_main_cond.wait()
            print("任务执行中...")

            try:
                # 获取当前设备运行的APP信息
                info = Device.memory()
                # 返回单位是字节
                total_memory_mb = info[2] / (1024 ** 2)
                used_memory_mb = info[1] / (1024 ** 2)
                free_memory_mb = info[0] / (1024 ** 2)
                print(f"剩余内存:{free_memory_mb},已用内存{used_memory_mb},总共内存{total_memory_mb}")
                counter += 1

                if counter % 3 == 0:
                    runThreadNotice()
                    runThreadReturnHome()
                    runThreadBaoZouBoss()
                    counter = 0  # 重置计数器

                # 启动app
                start_up.start_app()
                if 功能开关["营地总开关"] == 0 and 功能开关["日常总开关"] == 0 and 功能开关["旅团总开关"] == 0 and 功能开关['冒险总开关'] == 0:
                    Toast('未开启功能，请检查功能配置')
                    sleep(3)
                # 营地活动（优先领取）
                yingdiTask.yingdiTask()
                # 日常（优先领取）
                dailyTask.dailyTask()

                # 旅人相关
                lvrenTask.lvrenTask()

                # 旅团相关
                lvtuanTask.lvtuanTask()

                # 营地活动（最后领取）
                yingdiTask.yingdiTaskEnd()

                # 试炼
                shilianTask.shilian()

                # 日常（最后领取）
                dailyTask.dailyTaskEnd()

                # 定时休息
                current_time = int(time.time())

                if total_wait != 0 and current_time - start_time >= total_wait:
                    Toast(f"休息 {need_wait_minute} 分钟")
                    功能开关["fighting"] = 0
                    功能开关["needHome"] = 0
                    action.Key.home()
                    初始化任务记录()
                    sleep(need_wait_minute * 60)
                    start_time = int(time.time())

                # 定时切角色
                if total_switch_role_minute != 0 and current_time - start_time >= total_switch_role_minute:
                    Toast(f"运行 {need_switch_role_minute} 分钟，准确切换角色")
                    功能开关["fighting"] = 0
                    功能开关["needHome"] = 0
                    初始化任务记录()
                    start_up.switchRole()
                    start_time = int(time.time())
            except Exception as e:
                # 处理异常
                # 获取异常信息
                exc_type, exc_value, exc_traceback = sys.exc_info()
                # 输出异常信息和行号
                file_name, line_number, _, _ = traceback.extract_tb(exc_traceback)[-1]
                error_message = f"发生错误: {e} 在文件 {file_name} 第 {line_number} 行"
                # 显示对话框
                print(error_message)
                Dialog.confirm(error_message)