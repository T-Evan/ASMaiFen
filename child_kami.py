# 导包
from ascript.android import system

from .特征库 import *
from ascript.android.ui import Dialog
from .baseUtils import *
from .res.ui.ui import 功能开关,db
from ascript.android.screen import Colors
import pymysql
from ascript.android.system import Device

清空ip倒计时 = 0


# 识别屏幕是否卡死
def main():
    while True:
        if 功能开关['激活码'] != '':
            kamiOnlineDeviceCount()
        sleep(10)


# 每 30s 清空一次在线设备ip数，每 10s 检查在线ip数是否超过2个
def kamiOnlineDeviceCount():
    cursor = db.cursor()
    global 清空ip倒计时
    nowTime = time.time()
    if nowTime - 清空ip倒计时 > 60:
        # 构造 SQL 语句
        sql = "UPDATE kami SET device_ip = '[]' WHERE kami = %s"
        # 使用参数化查询
        cursor.execute(sql, (功能开关['激活码']))
        print('设备心跳更新成功')
        清空ip倒计时 = nowTime
        db.commit()

    kami = ''
    device_ip = ''
    device_available_num = ''
    sql = "SELECT * FROM kami WHERE kami = %s"
    # 使用参数化查询
    cursor.execute(sql, (功能开关['激活码']))
    results = cursor.fetchall()
    for row in results:
        kami = row[0]
        device_available_num = row[5]
        device_ip = row[6]

    now_device_ip = Device.ip()
    device_ips = json.loads(device_ip)
    if now_device_ip in device_ips:
        print('设备心跳检查成功')
    else:
        # 判断已激活设备数
        if len(device_ips) >= device_available_num:
            # if len(device_ips) >= 2:
            activeInfo = '已超过可在线设备数量'
            print('设备心跳检查失败')
            # Dialog.confirm(activeInfo, "激活码失效")
            # Toast(activeInfo, 3000)
            # system.exit()
        else:
            # 激活当前设备
            device_ips.append(now_device_ip)
            set_device_ips = json.dumps(device_ips)
            # 构造 SQL 语句
            sql = "UPDATE kami SET device_ip = %s WHERE kami = %s"
            # 使用参数化查询
            cursor.execute(sql, (set_device_ips, kami))
            db.commit()
            print('设备心跳发送成功')

    # 执行完之后要记得关闭游标和数据库连接
    cursor.close()
    # # 执行完毕后记得关闭db,不然会并发连接失败哦
    # db.close()
