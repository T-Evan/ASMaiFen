# ui.py 为初始化加载文件
import sys
import traceback
import json

# 导入动作模块
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
import pymysql
from ascript.android.system import Device
from datetime import datetime

# ldE.set_log_level(10)  # Debug
# ldE.set_log_level(20)  # Info
ldE.set_log_level(30)  # Warn
# ldE.set_log_level(40)  # ERROR

初始化任务记录()

db = pymysql.connect(
    host="8.140.162.237",  # 开发者后台,创建的数据库 “主机地址”
    port=3307,  # 开发者后台,创建的数据库 “端口”
    user='yiwan233',  # 开发者后台,创建的数据库 “用户名”
    password='233233',  # 开发者后台,创建的数据库 “初始密码”
    database='db_dev_12886',  # 开发者后台 ,创建的 "数据库"
    charset='utf8mb4'  ""
)  # 连接数据库

cursor = db.cursor()
sql = "SELECT * FROM kami WHERE kami LIKE %s"
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
    activeInfo = '卡密不存在，请重新输入'
    Dialog.confirm(activeInfo, "激活码失效")
    Toast(activeInfo, 3000)
    sys.exit()
if kami != '':
    # 判断首次激活
    if expire_time == 0:
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
    if expire_time != 0:
        dt_object = datetime.fromtimestamp(expire_time)
        formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        # 判断卡密是否过期
        if int(time.time()) > expire_time:
            activeInfo = '卡密已过期，过期时间：' + formatted_date
            Dialog.confirm(activeInfo, "激活码失效")
            Toast(activeInfo, 3000)
            ldE.sleep(2)
            sys.exit()
    # 判断登录设备数
        now_device_id = Device.id()
        device_ids = json.loads(device_id)
        if now_device_id in device_id:
            activeInfo = '当前设备已激活，' + '过期时间：' + formatted_date
            Toast(activeInfo, 3000)
            ldE.sleep(2)
        else:
            # 判断已激活设备数
            if len(device_ids) >= device_available_num:
                activeInfo = '已超过可激活设备数量'
                Dialog.confirm(activeInfo, "激活码失效")
                Toast(activeInfo, 3000)
                ldE.sleep(2)
                sys.exit()
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
                ldE.sleep(2)

# 执行完之后要记得关闭游标和数据库连接
cursor.close()
# 执行完毕后记得关闭db,不然会并发连接失败哦
db.close()

display = Device.display()
# 屏幕宽度
if display.widthPixels != 720 or display.heightPixels != 1280:
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
# if return1:
#     return1.click(rx=5, ry=5).execute(sleep=1)
# res, buyCount = TomatoOcrText(496,815,510,835, "已购买次数")  # 1 / 9
# re = ldE.find_element('结伴-当前地图').target
# sys.exit()


def main():
    try:
        start_up = StartUp("com.xd.cfbmf")
        yingdiTask = YingDiTask()
        dailyTask = DailyTask()
        lvrenTask = LvRenTask()
        lvtuanTask = LvTuanTask()
        shilianTask = ShiLianTask()

        # dailyTask.quitTeam()
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
        need_switch_minute = safe_int(功能开关.get("定时切号", 0))  # 分钟
        if need_switch_minute == '':
            need_switch_minute = 0
        need_switch_role_minute = safe_int(功能开关.get("定时切角色", 0))  # 分钟
        if need_switch_role_minute == '':
            need_switch_role_minute = 0

        total_wait = need_run_minute * 60
        total_switch_minute = need_switch_minute * 60
        total_switch_role_minute = need_switch_role_minute * 60

        start_time = int(time.time())

        while True:
            if not thread1.is_alive():
                runThread1()

            if not thread2.is_alive():
                runThread2()

            if not threadBaoZouBoss.is_alive():
                runThreadBaoZouBoss()

            # 启动app
            start_up.start_app()
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
                ldE.sleep(need_wait_minute * 60)
                start_time = int(time.time())
    except Exception as e:
        # 处理异常
        # 获取异常信息
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # 输出异常信息和行号
        file_name, line_number, _, _ = traceback.extract_tb(exc_traceback)[-1]
        error_message = f"发生错误: {e} 在文件 {file_name} 第 {line_number} 行"
        # 显示对话框
        Dialog.confirm(error_message)
    sys.exit()


main()
