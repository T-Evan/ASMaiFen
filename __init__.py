# ui.py 为初始化加载文件
import sys
import traceback
import json

# 导入动作模块
from .res.ui.ui import 功能开关, loadConfig
from .res.ui.ui import 任务记录
from .shilian import ShiLianTask
from .lvtuan import LvTuanTask
from .lvren import LvRenTask
from .startUp import StartUp
from .yingdi import YingDiTask
from .daily import DailyTask
from .res.ui.ui import 初始化任务记录
from .baseUtils import *
from .thread import *
from .threadMain import *
import time
from ascript.android.ui import Dialog
import pymysql
from datetime import datetime
from ascript.android.system import Device
from ascript.android.ui import Loger
from ascript.android import system
from ascript.android.action import Path

# ldE.set_log_level(10)  # Debug
# ldE.set_log_level(20)  # Info
# ldE.set_log_level(30)  # Warn
# ldE.set_log_level(40)  # ERROR

初始化任务记录()


def kamiActive():
    db = pymysql.connect(
        host="8.140.162.237",  # 开发者后台,创建的数据库 “主机地址”
        port=3307,  # 开发者后台,创建的数据库 “端口”
        user='yiwan233',  # 开发者后台,创建的数据库 “用户名”
        password='233233',  # 开发者后台,创建的数据库 “初始密码”
        database='db_dev_12886',  # 开发者后台 ,创建的 "数据库"
        charset='utf8mb4'  ""
    )  # 连接数据库
    cursor = db.cursor()
    sql = "SELECT * FROM kami WHERE kami != '' and kami LIKE %s"
    # 使用参数化查询
    cursor.execute(sql, (功能开关['激活码'],))
    results = cursor.fetchall()

    # 循环遍历所有数据
    kami = ''
    device_id = ''
    expire_time = 0
    device_available_num = ''
    for row in results:
        # 我们的表数据,总共4列,因此逐个获取每列数据
        kami = row[0]
        device_id = row[1]
        expire_time = row[3]
        device_available_num = row[5]

    if kami == '':
        now_device_id = '"' + Device.id() + '"'
        # 判断设备是否激活过试用
        sql = "SELECT * FROM kami WHERE device_id LIKE %s and kami = ''"
        # 使用参数化查询
        cursor.execute(sql, now_device_id)
        results = cursor.fetchall()
        for row in results:
            device_id = row[1]
            expire_time = row[3]
        if device_id == '':
            expire_time = int(time.time()) + 86400 * 0.5  # 日卡
            dt_object = datetime.fromtimestamp(expire_time)
            formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            now_device_id = Device.id()
            device_ids = json.dumps(now_device_id)
            # 构造 SQL 语句
            sql = "Insert into kami (device_id,expire_time,kami) Values (%s,%s,'')"
            # 使用参数化查询
            cursor.execute(sql, (device_ids, expire_time))
            db.commit()  # 不要忘了提交,不然数据上不去哦
            activeInfo = '试用卡密激活成功，过期时间：' + formatted_date
            Toast(activeInfo, 3000)
        if device_id != '':
            # 判断首次激活
            if expire_time == 0:
                expire_time = int(time.time()) + 86400 * 0.5  # 日卡
                dt_object = datetime.fromtimestamp(expire_time)
                formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                now_device_id = Device.id()
                device_ids = json.dumps(now_device_id)
                # 构造 SQL 语句
                sql = "UPDATE kami SET device_id = %s, expire_time = %s WHERE device_id LIKE %s and kami == ''"
                # 使用参数化查询
                cursor.execute(sql, (device_ids, expire_time, kami))
                db.commit()  # 不要忘了提交,不然数据上不去哦
                activeInfo = '试用卡密激活成功，过期时间：' + formatted_date
                Toast(activeInfo, 3000)
            if expire_time != 0:
                dt_object = datetime.fromtimestamp(expire_time)
                formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                # 判断卡密是否过期
                if int(time.time()) > expire_time:
                    activeInfo = '卡密已过期，过期时间：' + formatted_date
                    Dialog.confirm(activeInfo, "激活码失效")
                    Toast(activeInfo, 3000)
                    sleep(2)
                    system.exit()
                else:
                    activeInfo = '试用已激活，' + '过期时间：' + formatted_date
                    Toast(activeInfo, 3000)
                    sleep(2)

    # activeInfo = '卡密不存在，请重新输入'
    # Dialog.confirm(activeInfo, "激活码失效")
    # Toast(activeInfo, 3000)
    # system.exit()
    if kami != '':
        # 判断首次激活
        if expire_time == 0:
            if 'test' in kami:
                expire_time = int(time.time()) + 86400 * 1  # 日卡
            else:
                expire_time = int(time.time()) + 86400 * 30  # 月卡
            dt_object = datetime.fromtimestamp(expire_time)
            formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            now_device_id = Device.id()
            device_ids = json.dumps(now_device_id)
            # 构造 SQL 语句
            sql = "UPDATE kami SET device_id = %s, expire_time = %s WHERE kami = %s"
            # 使用参数化查询
            cursor.execute(sql, (device_ids, expire_time, kami))
            db.commit()  # 不要忘了提交,不然数据上不去哦
            activeInfo = '卡密激活成功，过期时间：' + formatted_date
            Toast(activeInfo, 3000)
        if expire_time != 0:
            dt_object = datetime.fromtimestamp(expire_time)
            formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            # 判断卡密是否过期
            if int(time.time()) > expire_time:
                activeInfo = '卡密已过期，过期时间：' + formatted_date
                Dialog.confirm(activeInfo, "激活码失效")
                Toast(activeInfo, 3000)
                sleep(2)
                system.exit()
            # 判断登录设备数
            now_device_id = Device.id()
            device_ids = json.loads(device_id)
            if now_device_id in device_id:
                activeInfo = '已激活，' + '过期时间：' + formatted_date
                Toast(activeInfo, 3000)
                sleep(2)
            else:
                # 判断已激活设备数
                if len(device_ids) >= device_available_num:
                    activeInfo = '已超过可激活设备数量'
                    Dialog.confirm(activeInfo, "激活码失效")
                    Toast(activeInfo, 3000)
                    sleep(2)
                    system.exit()
                else:
                    # 激活当前设备
                    device_ids.append(now_device_id)
                    set_device_ids = json.dumps(device_ids)
                    # 构造 SQL 语句
                    sql = "UPDATE kami SET device_id = %s WHERE kami = %s"
                    # 使用参数化查询
                    cursor.execute(sql, (set_device_ids, kami))
                    db.commit()  # 不要忘了提交,不然数据上不去哦
                    activeInfo = '激活新设备成功，' + '过期时间：' + formatted_date
                    Toast(activeInfo, 3000)
                    sleep(2)

    # 执行完之后要记得关闭游标和数据库连接
    cursor.close()
    # 执行完毕后记得关闭db,不然会并发连接失败哦
    db.close()


print('卡密联网激活开始')
kamiActive()
print('卡密联网激活完成')

display = Device.display()
# 屏幕宽度
if display.widthPixels != 720 or display.heightPixels != 1280:
    Dialog.confirm("屏幕分辨率不为 720 * 1280，请重新设置", "分辨率错误")
    Dialog.confirm("屏幕分辨率不为 720 * 1280，请重新设置", "分辨率错误")


# debug
# res = Ocr.mlkitocr_v2()
# if res:
#     #循环打印识别到的每一个段落
#     for r in res:
#         print("文字:",r.text)
#         print("文字中心坐标:",r.center_x,r.center_y)
#         print("文字范围:",r.rect)
# return1 = ldE.element_exist('返回-1')
# print(return1)
# def tunner(k,v):
#     print(k,v)

# loger 继承 Window ,因此 Window 中的方法,loger都可以使用
# lw = Loger(R.ui("loger.html"))
# lw.tunner(tunner) # 设置消息通道
# lw.show() # 展示
# print(功能开关['角色4开关'])
# if 功能开关['角色4开关'] == 0 or 功能开关['角色4开关'] == False:
# loadConfig(5)
# print(功能开关)
# for k in range(100):
#     player_messages = shijieShoutText()
#     print(player_messages)
#     sleep(0.5)
# tapSleep(574, 1051,0.1)  # 点击奖励
# tapSleep(570, 1062,0.1)  # 点击奖励
# tapSleep(104,1218,0.1)  # 点击奖励
# system.exit()


def main():
    try:
        start_up = StartUp(f'{功能开关["游戏包名"]}')
        yingdiTask = YingDiTask()
        dailyTask = DailyTask()
        lvrenTask = LvRenTask()
        lvtuanTask = LvTuanTask()
        shilianTask = ShiLianTask()

        功能开关["breakChild"] = 0
        功能开关["fighting"] = 0
        功能开关["fighting_baozou"] = 0
        功能开关["needHome"] = 0

        # 处理休息时间
        need_run_minute = safe_int(功能开关.get("定时运行", 0))  # 分钟
        if need_run_minute == '':
            need_run_minute = 0
        need_wait_minute = safe_int(功能开关.get("定时休息", 0))  # 分钟
        if need_wait_minute == '':
            need_wait_minute = 0
        need_switch_account_minute = safe_int(功能开关.get("定时切账号", 0))  # 分钟
        if need_switch_account_minute == '':
            need_switch_account_minute = 0
        need_switch_role_minute = safe_int(功能开关.get("定时切角色", 0))  # 分钟
        if need_switch_role_minute == '':
            need_switch_role_minute = 0

        total_wait = need_run_minute * 60
        total_switch_account_minute = need_switch_account_minute * 60
        total_switch_role_minute = need_switch_role_minute * 60

        任务记录["切换角色-倒计时"] = time.time()
        任务记录["切换账号-倒计时"] = time.time()
        任务记录["切换配置-倒计时"] = time.time()
        任务记录["定时休息-倒计时"] = time.time()
        任务记录["任务重置-倒计时"] = time.time()

        # 多账号处理
        start_up.multiAccount()

        if 功能开关["选择启动配置"] != "0" and 任务记录['当前任务配置'] == 0:
            configNum = safe_int(功能开关["选择启动配置"])
            for k in range(5):
                if 功能开关[f"配置{configNum}名称"] == "":
                    continue
                need_config_minute = safe_int(功能开关.get(f"配置{configNum}运行时长", 0))  # 分钟
                Toast(
                    f'加载配置{configNum}{功能开关[f"配置{configNum}名称"]} + 预计执行{need_config_minute}分后继续切换')
                sleep(1.5)
                res = loadConfig(configNum)
                if not res:
                    configNum = configNum + 1
                    continue
                任务记录['当前任务配置'] = configNum
                break

        if 功能开关['技能进入战斗后启动'] == 1 or 功能开关['AI进入战斗后启动'] == 1:
            runThreadAutoSkill()
            runThreadAutoSkill2()
            runThreadAutoSkill3()
            runThreadAutoMove()
        else:
            runThreadNotice()
            runThreadReturnHome()
            runThreadBaoZouBoss()
            runThreadMijingTeam()
            runThreadAnotherLogin()
            # runThreadCheckKami()
            runThreadAutoSkill()
            runThreadAutoSkill2()
            runThreadAutoSkill3()
            runThreadAutoMove()
        # runThreadCheckBlock()
        counter = 0

        # debug
        # while 1:
        #     功能开关["fighting"] = 1
        #     sleep(1)
        # system.exit()

        while True:
            try:
                if 功能开关["fighting"] == 1:
                    # Toast('战斗中 - 主进程暂停')
                    sleep(5)
                    continue
                if 功能开关['技能进入战斗后启动'] == 1 or 功能开关['AI进入战斗后启动'] == 1 or 功能开关[
                    '暴走进入战斗后启动'] == 1:
                    Toast('已开启-进入战斗后启动！等待进入战斗')
                    # 识别是否战斗中
                    res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
                    res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
                    # res1, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")
                    if "等级" in teamName1 or "等级" in teamName2 or "Lv" in teamName1 or "Lv" in teamName2:
                        # 大暴走战斗中
                        if 功能开关["大暴走开关"] == 1 and 功能开关["暴走进入战斗后启动"] == 1:
                            Toast("进入暴走战斗成功 - 开始战斗")
                            shilianTask.fightingBaoZou()
                            return
                    sleep(10)
                    continue
                # 获取当前设备运行的APP信息
                # info = Device.memory()
                # # 返回单位是字节
                # total_memory_mb = info[2] / (1024 ** 2)
                # used_memory_mb = info[1] / (1024 ** 2)
                # free_memory_mb = info[0] / (1024 ** 2)
                # print(f"剩余内存:{free_memory_mb},已用内存{used_memory_mb},总共内存{total_memory_mb}")
                # counter += 1
                # if counter % 3 == 0:
                #     runThreadNotice()
                #     runThreadReturnHome()
                #     runThreadBaoZouBoss()
                #     runThreadMijingTeam()
                #     runThreadAnotherLogin()
                #     counter = 0  # 重置计数器

                # 启动app
                start_up.start_app()
                if 功能开关["营地总开关"] == 0 and 功能开关["日常总开关"] == 0 and 功能开关["旅团总开关"] == 0 and \
                        功能开关['冒险总开关'] == 0:
                    Toast('未开启功能，请检查功能配置')
                    sleep(3)

                if 功能开关["日常总开关"] == 1 and 功能开关["优先推图到最新关卡"] == 1:
                    for i in range(5):
                        Toast(f'重复推图到最新关卡 第{i + 1}次')
                        res = dailyTask.newMap()
                        if not res:
                            break

                # 首页卡死检测（通过点击行李判断能否跳转成功）
                status = dailyTask.checkGameStatus()
                if not status:
                    continue  # 重启游戏，重新执行登录流程

                # 营地活动（优先领取）
                yingdiTask.yingdiTask()
                # 日常（优先领取）
                dailyTask.dailyTask()

                # 检查背包是否已满
                lvrenTask.deleteEquip(needDelete=True)

                # 试炼
                shilianTask.shilian()

                # 旅团相关
                lvtuanTask.lvtuanTask()

                # 旅人相关
                lvrenTask.lvrenTask()

                # 日常2
                dailyTask.dailyTask2()

                # 日常（最后领取）
                dailyTask.dailyTaskEnd()

                # 营地活动（优先领取）
                yingdiTask.yingdiTask2()

                # 营地活动（最后领取）
                yingdiTask.yingdiTaskEnd()

                # 日常（最后领取一次冒险手册）
                dailyTask.maoXianShouCe()

                # 定时休息
                current_time = int(time.time())

                # 将时间戳转换为 datetime 对象
                # 判断执行时间超过4小时（重置每日任务）
                if current_time - 任务记录["任务重置-倒计时"] > 60 * 60 * 4:
                    Toast(f"执行时间超过4小时，重置每日任务")
                    sleep(1.5)
                    初始化任务记录(False)
                    任务记录["任务重置-倒计时"] = int(time.time())

                if total_wait != 0 and current_time - 任务记录["定时休息-倒计时"] >= total_wait:
                    Toast(f"休息 {need_wait_minute} 分钟")
                    sleep(1.5)
                    功能开关["fighting"] = 0
                    功能开关["needHome"] = 0
                    action.Key.home()
                    初始化任务记录(False)
                    sleep(need_wait_minute * 60)
                    任务记录["定时休息-倒计时"] = int(time.time())

                # 定时切配置
                if 功能开关["选择启动配置"] != "0":
                    configNum = safe_int(任务记录["当前任务配置"])
                    need_switch_config_minute = safe_int(功能开关.get(f"配置{configNum}运行时长", 0))  # 分钟
                    if need_switch_config_minute == '':
                        need_switch_config_minute = 0
                    total_switch_config_minute = need_switch_config_minute * 60
                    if total_switch_config_minute != 0:
                        if current_time - 任务记录["切换配置-倒计时"] >= total_switch_config_minute:
                            Toast(f"运行 {need_switch_config_minute} 分钟，准备切换配置")
                            sleep(1.5)
                            功能开关["fighting"] = 0
                            功能开关["needHome"] = 0
                            初始化任务记录(False)
                            for k in range(5):
                                configNum = configNum + 1
                                if configNum > 5:
                                    configNum = 1  # 从配置1重新切换
                                if 功能开关[f"配置{configNum}名称"] == "" or 功能开关[f"配置{configNum}运行时长"] == "":
                                    continue
                                need_config_minute = safe_int(功能开关.get(f"配置{configNum}运行时长", 0))  # 分钟
                                if need_config_minute == 0:
                                    continue
                                Toast(
                                    f'加载配置{configNum}{功能开关[f"配置{configNum}名称"]} + 预计执行{need_config_minute}分后继续切换')
                                res = loadConfig(configNum)
                                if not res:
                                    continue
                                任务记录["当前任务配置"] = configNum
                                break
                            任务记录["切换配置-倒计时"] = int(time.time())
                        else:
                            tmpMinute = round((current_time - 任务记录["切换配置-倒计时"]) / 60, 2)
                            tmpDiffMinute = round(
                                need_switch_config_minute - ((current_time - 任务记录["切换配置-倒计时"]) / 60), 2)
                            Toast(f"运行 {tmpMinute} 分钟，{tmpDiffMinute} 分后切换配置")
                            sleep(1.5)

                # 定时切角色
                if total_switch_role_minute != 0:
                    if current_time - 任务记录["切换角色-倒计时"] >= total_switch_role_minute:
                        Toast(f"运行 {need_switch_role_minute} 分钟，准备切换角色")
                        sleep(1.5)
                        功能开关["fighting"] = 0
                        功能开关["needHome"] = 0
                        初始化任务记录(False)
                        start_up.switchRole()
                        任务记录["切换角色-倒计时"] = int(time.time())
                    else:
                        tmpMinute = round((current_time - 任务记录["切换角色-倒计时"]) / 60, 2)
                        tmpDiffMinute = round(
                            need_switch_role_minute - ((current_time - 任务记录["切换角色-倒计时"]) / 60), 2)
                        Toast(f"运行 {tmpMinute} 分钟，{tmpDiffMinute} 分后切换角色")
                        sleep(1.5)

                # 定时切账号
                current_time = int(time.time())
                if total_switch_account_minute != 0:
                    if current_time - 任务记录["切换账号-倒计时"] >= total_switch_account_minute:
                        Toast(f"运行 {need_switch_account_minute} 分钟，准备切换账号")
                        sleep(1.5)
                        初始化任务记录(False)
                        start_up.switchAccount()
                        print(功能开关)
                        任务记录["切换账号-倒计时"] = int(time.time())
                    else:
                        tmpMinute = round((current_time - 任务记录["切换账号-倒计时"]) / 60, 2)
                        tmpDiffMinute = round(
                            need_switch_account_minute - ((current_time - 任务记录["切换账号-倒计时"]) / 60), 2)
                        Toast(f"运行 {tmpMinute} 分钟，{tmpDiffMinute} 分后切换账号")
                        sleep(1.5)

                # 定时重启脚本（3h）
                # need_reboot_minute = 6 * 60
                # need_reboot_minute = 0.1
                # total_reboot_minute = need_reboot_minute * 60
                # if current_time - start_time >= total_reboot_minute:
                #     Toast(f"运行 {need_reboot_minute} 分钟,重启脚本")
                #     system.reboot()
                # else:
                #     tmpMinute = round((current_time - start_time) / 60, 2)
                #     tmpDiffMinute = round(need_reboot_minute - ((current_time - start_time) / 60), 2)
                #     Toast(f"已运行 {tmpMinute} 分钟，{tmpDiffMinute} 分后重启脚本")
            except Exception as e:
                # 处理异常
                # 获取异常信息
                exc_type, exc_value, exc_traceback = sys.exc_info()
                # 输出异常信息和行号
                file_name, line_number, _, _ = traceback.extract_tb(exc_traceback)[-1]
                error_message = f"发生错误: {e} 在文件 {file_name} 第 {line_number} 行"
                # 显示对话框
                print(error_message)
    except Exception as e:
        # 处理异常
        # 获取异常信息
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # 输出异常信息和行号
        file_name, line_number, _, _ = traceback.extract_tb(exc_traceback)[-1]
        error_message = f"发生错误: {e} 在文件 {file_name} 第 {line_number} 行"
        # 显示对话框
        print(error_message)
        if error_message != '':
            Dialog.confirm(error_message)
        else:
            Toast('检测到执行出现异常，请联系群主反馈')
    sys.exit()


main()
