# __init__.py 为初始化加载文件
# 导入-节点检索库
import json
import time
import pymysql

from ascript.android.system import R
# 导入-屏幕检索库
from ascript.android.ui import WebWindow
from ascript.android.ui import Dialog
import threading
import sys
from ascript.android import system
# 向悬浮菜单中新增按钮
from ascript.android.ui import FloatWindow
from ascript.android.system import R
# 导入-屏幕检索库
from ascript.android.ui import WebWindow
# from ascript.android.ui import Loger
from datetime import datetime, timedelta
from time import sleep

config = None


def tunner(k, v):
    global config
    print(k, v)
    print(k)
    print(v)

    if k == "guan" and v == "关闭":
        config = "exit"
    if k == "submit":
        res = json.loads(v)
        config = res
        # print(type(config))
    if k == "加载" and v == "成功":
        print('加载成功')


formW = WebWindow(R.ui("ui.html"))
formW.size('100vw', '100vh')
formW.tunner(tunner)  # 在这里设置消息通道
formW.background("#FFFFFF")
formW.show()
from threading import Lock

while True:
    print("循环等待中")
    time.sleep(1)
    if config == "exit":
        Dialog.toast('取消执行', 5, 3 | 48, 200, 0)
        system.exit()
    if config:
        Dialog.toast('资源加载中 - 请等待30s', 5, 3 | 48, 200, 0)
        # time.sleep(2)
        break

import time


class TimeoutLock:
    def __init__(self, timeLock=10, lock=''):
        self.lock = lock
        if lock == '':
            self.lock = switch_lock
        self.timeout = timeLock

    def acquire_lock(self):
        start_time = time.time()
        while (time.time() - start_time) < self.timeout:
            if self.lock.acquire(False):
                return True
            time.sleep(0.2)
        print(f"尝试获取锁超时，耗时: {time.time() - start_time} 秒")
        return False

    def release_lock(self):
        self.lock.release()

    def __enter__(self):
        if not self.acquire_lock():
            raise RuntimeError("无法在指定时间内获取锁")
        # print("锁已成功获取")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release_lock()
        # print("锁已成功释放")


# 初始化锁
global switch_lock
switch_lock = Lock()
global switch_ocr_apk_lock  # apk ocr 识别锁
switch_ocr_apk_lock = Lock()
功能开关 = {}
功能开关 = config
功能配置 = {'配置1': config['配置1'], '配置2': config['配置2'], '配置3': config['配置3'], '配置4': config['配置4'],
            '配置5': config['配置5']}
if 功能开关['选择游戏版本'] == "国服":
    功能开关['游戏包名'] = "com.xd.cfbmf"
elif 功能开关['选择游戏版本'] == "台服":
    功能开关['游戏包名'] = "com.xd.muffin.tw"
elif 功能开关['选择游戏版本'] == "国际服":
    功能开关['游戏包名'] = "com.xd.muffin.tap.global"
elif 功能开关['选择游戏版本'] == "国际服2":
    功能开关['游戏包名'] = "com.xd.muffin.gp.global"


def loadConfig(configNum, accountNum=""):
    global 功能开关
    if accountNum != "":
        功能开关["选择启动区服"] = 功能开关[f"账号{configNum}启动区服"]

    configName = '配置' + str(configNum)
    new = json.loads(功能配置[configName])
    if not new:
        return False
    for index, value in new.items():
        if value == 'false':
            value = False
        if value == 'true':
            value = True
        功能开关[index] = value
    # print(222)
    # 功能开关 = new
    print(功能开关)
    return 功能开关


# thread_main_paused = False
# thread_main_cond = threading.Condition()

任务记录 = {
    "提示-并发锁": 0,
    "喊话-并发锁": 0,
    "启动时间": time.time(),

    "当前任务账号": 功能开关["选择启动账号"],
    "当前任务角色": 功能开关["选择启动角色"],
    "当前任务配置": 0,

    "切换角色-倒计时": 0,
    "切换账号-倒计时": 0,
    "切换配置-倒计时": 0,
    "定时休息-倒计时": 0,
    "任务重置-倒计时": 0,

    "AI发言-广告开关": 0,
    "AI发言-检测队友关注": 0,
    "AI发言-上一次发言": [],
    "战斗-上一次移动": 0,
    "战斗-推荐战力": 0,
    "战斗-关卡名称": '',
    "战斗-房主名称": '',
    "战斗-房主旅团": '',
    "战斗-房主战力": 0,
    "战斗-房主上次相遇": 0,
    "战斗-恶龙名称": 0,
    "战斗-恶龙名称-识别倒计时": 0,
    "带队次数": "",
    "玩家名称": "",
    "玩家战力": "",
    "玩家-当前关卡": "",
    "玩家-当前关卡-倒计时": 0,
    "玩家-当前职业": "",
    "玩家-当前旅团": "",
    "玩家-当前旅团-倒计时": 0,
}


def 初始化任务记录(initAll=True):
    # 日常
    任务记录.update({
        "首页卡死检测-倒计时": 0,

        "仓鼠百货-完成": 0,
        "邮件领取-完成": 0,
        "兑换码领取-完成": 0,
        "自动使用经验补剂-完成": 0,
        "寻找结伴-完成": 0,
        "大暴走-完成": 0,
        "桎梏之形-完成": 0,
        "三魔头-完成": 0,

        "冒险手册-倒计时": 0,

        "半周年庆典签到": 0,
        "双旦联欢签到": 0,
        "西行记签到": 0,
        "忆战回环签到": 0,
        "大家的麦芬": 0,

        "摆摊奇才签到": 0,
        "红包传好运": 0,
        "祈福交好运": 0,
        "欢庆连五日": 0,
        "斗歌会-完成": 0,

        "盛大公演": 0,
        "逍遥大圣": 0,
        "来富巳": 0,
        "BBQ派对": 0,
    })

    # 旅团
    任务记录.update({
        "旅团-浇树-完成": 0,
        "旅团-调查队-完成": 0,
        "旅团-许愿墙-完成": 0,
        "旅团-任务-完成": 0,
        "旅团-商店-完成": 0,
        "旅团-大采购-完成": 0,
    })

    # 冒险
    任务记录.update({
        "恶龙任务": 0,
    })

    # 旅人
    任务记录.update({
        "强化装备-倒计时": 0,
        "分解装备-倒计时": 0,
        "更换装备-倒计时": 0,
        "技能升级-倒计时": 0,

        "装备数量": 0,

        "旅人-猫猫果木-完成": 0,
        "旅人-秘宝升星-完成": 0,
        "日常-招式创造-完成": 0,
        "日常-骑兽乐园-完成": 0,
        "日常-释放1次战术技能-完成": 0,
        "日常-洗练1次装备-完成": 0,

        "日常-升级1次麦乐兽-完成": 0,
        "试炼-秘境-体力消耗完成": 0,
        "试炼-恶龙-完成次数": 0,
        "日常-宝藏湖-完成": 0,
        "日常-摸鱼时间到-完成": 0,
    })

    # if initAll:
    #     任务记录.update({"日常-洗练1次装备-完成": 0, })

    # 营地
    任务记录.update({
        "月签到-完成": 0,
        "月卡-完成": 0,
        "日礼包-完成": 0,
        "露营打卡点-完成": 0,
        "舞会签到簿-完成": 0,
        "纸飞机-完成": 0,
        "星辰同行-完成": 0,
        "秘宝领取-完成": 0,
        "限时特惠-完成": 0,
        "登录好礼-完成": 0,
        "箱庭苗圃-倒计时": 0,
        "箱庭苗圃-完成": 0,
        "紧急委托-完成": 0,
        "火力全开-完成": 0,
        "派对大师-完成": 0,
        "队伍喊话-倒计时": 0,
        "世界喊话-倒计时": 0,
        "世界喊话AI-倒计时": 0,
    })


def tunner(k, v):
    print(k, v)


# loger 继承 Window ,因此 Window 中的方法,loger都可以使用
# lw = Loger(R.ui("loger.html"))
# lw.tunner(tunner)  # 设置消息通道


# lw.show() # 展示
# lw.close()

def a():
    totalTime = time.time() - 任务记录['启动时间']
    # 计算小时和分钟
    hours = int(totalTime // 3600)
    minutes = int((totalTime % 3600) // 60)

    # 任务记录['玩家名称'] = '咸鱼搜麦乐芬'

    if 任务记录['玩家名称'] == "":
        Dialog.toast(
            f"数据加载中，请稍后再来查看吧~\nps:多次加载失败可尝试重启脚本",
            3000, 3 | 48, 0, 0, "#666666", "#FFFFFF")
        return

    任务记录['提示-并发锁'] = 1
    userTotalDaiDuiCount, userTodayDaiDuiCount, TodayDaiDuiPaiHang, UserDaiDuiPaiHang = daiDuiCount()

    Dialog.toast(
        f"已运行{hours}小时{minutes}分\n玩家：{任务记录['玩家名称']}\n总带队{userTotalDaiDuiCount}次，今日带队{userTodayDaiDuiCount}次\n今天带队排行:\n{TodayDaiDuiPaiHang}\n您带队玩家排行:\n{UserDaiDuiPaiHang}",
        5000, 3 | 48, 0, 0, "#666666", "#FFFFFF")
    sleep(5)
    任务记录['提示-并发锁'] = 0


FloatWindow.add_menu("10001", R.img("ico_rank.png"), a)


def daiDuiCount():
    db = pymysql.connect(
        host="8.140.162.237",  # 开发者后台,创建的数据库 “主机地址”
        port=3307,  # 开发者后台,创建的数据库 “端口”
        user='yiwan233',  # 开发者后台,创建的数据库 “用户名”
        password='233233',  # 开发者后台,创建的数据库 “初始密码”
        database='db_dev_12886',  # 开发者后台 ,创建的 "数据库"
        charset='utf8mb4'  ""
    )  # 连接数据库

    # 获取当前时间
    now = datetime.now()
    # 获取今天的0点时间
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    # 将今天的0点时间转换为Unix时间戳
    today_start_timestamp = int(today_start.timestamp())

    userTotalDaiDuiCount = 0
    cursor = db.cursor()
    sql = "SELECT count(distinct(team_name)) FROM daidui WHERE user_name = %s"
    # 使用参数化查询
    cursor.execute(sql, (任务记录['玩家名称']))
    results = cursor.fetchall()
    print(results)
    for row in results:
        userTotalDaiDuiCount = row[0]

    userTodayDaiDuiCount = 0
    sql = f"SELECT count(distinct(team_name)) FROM daidui WHERE user_name = %s and last_time > {today_start_timestamp}"
    # 使用参数化查询
    cursor.execute(sql, (任务记录['玩家名称']))
    results = cursor.fetchall()
    print(results)
    for row in results:
        userTodayDaiDuiCount = row[0]

    TodayDaiDuiPaiHang = ""
    sql = f"SELECT user_name,count(distinct(team_name)) as ct FROM daidui WHERE user_name not in ('','（','）') and last_time > {today_start_timestamp} group by user_name order by ct desc limit 10"
    # 使用参数化查询
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    for row in results:
        # userName = row[0][:-1] + '*'
        userName = row[0]
        TodayDaiDuiPaiHang += f"{userName}:{row[1]}次\n"

    UserDaiDuiPaiHang = ""
    sql = f"SELECT team_name,count FROM daidui WHERE  user_name = %s and team_name not in ('','（','）') group by team_name order by count desc limit 10"
    # 使用参数化查询
    cursor.execute(sql, (任务记录['玩家名称']))
    results = cursor.fetchall()
    print(results)
    for row in results:
        UserDaiDuiPaiHang += f"{row[0]}:{row[1]}次\n"
    UserDaiDuiPaiHang = UserDaiDuiPaiHang.rstrip('\n')

    # 执行完之后要记得关闭游标和数据库连接
    cursor.close()
    # 执行完毕后记得关闭db,不然会并发连接失败哦
    db.close()

    return userTotalDaiDuiCount, userTodayDaiDuiCount, TodayDaiDuiPaiHang, UserDaiDuiPaiHang
