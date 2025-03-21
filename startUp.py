# 导包
from ascript.android import system
from six import print_
from ascript.android.system import ShellListener

from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .res.ui.ui import 任务记录
from .res.ui.ui import 功能配置
from .res.ui.ui import loadConfig
from .res.ui.ui import switch_lock
from .baseUtils import *
import shutil
import os
import sys
from ascript.android import system
from ascript.android.screen import FindColors
import sys
import traceback


class StartUp:
    # 构造器
    def __init__(self, app_name):
        self.app_name = app_name

    # 实例方法
    def start_app(self):
        global 功能开关
        # r = system.shell(f"start -n com.xd.cfbmf")
        tryTimes = 0

        max_attempt = 14
        for attempt in range(max_attempt):
            tryTimes = tryTimes + 1
            if 功能开关["fighting"] == 1:
                if tryTimes < 3:
                    res, _ = TomatoOcrText(502, 187, 582, 213, '离开队伍')
                    if res:
                        return
                    res, _ = TomatoOcrText(649, 321, 694, 343, '队伍')
                    if res:
                        sleep(30)
                        continue

                    point = CompareColors.compare(
                        "108,94,#6884BA|102,86,#6584B9|121,89,#6584B9|107,101,#F4EEDE|105,97,#6989B9")
                    if point:
                        Toast('检查登录状态-收起喊话窗口')
                        tapSleep(107, 93)
                    Toast(f'检查登录状态 - 等待任务结束{tryTimes * 2}/6')
                    sleep(2)
                    continue

            system.open(self.app_name)
            if tryTimes > 5:
                TomatoOcrTap(330, 828, 390, 871, '同意')  # 隐私政策更新

            # 识别是否进入登录页
            login1, _ = TomatoOcrText(287, 1019, 339, 1049, "开始")  # 开始冒险之旅
            # login2, _ = TomatoOcrText(302, 1199, 414, 1231, "开始冒险")
            if login1:
                Toast('准备进入游戏')
                self.login()
            else:
                re = TomatoOcrTap(330, 1201, 389, 1238, '冒险')
                if not re:
                    # 不在登录页，尝试开始返回首页
                    功能开关["needHome"] = 1
                    功能开关["fighting"] = 0

            # 判断是否已在首页
            # 判断底部冒险图标
            res2 = CompareColors.compare(
                "375,1229,#F6F1E7|377,1216,#7C532E|386,1220,#F8ECCD|382,1205,#FCF8EE|382,1193,#FCF8EE|380,1183,#FCF8EE")
            shou_ye1 = False
            shou_ye2 = False
            if not res2:
                shou_ye1, _ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
                if not shou_ye1:
                    shou_ye2, _ = TomatoOcrText(627, 381, 710, 403, "新手试炼")
                    if not shou_ye2:
                        shou_ye2, _ = TomatoOcrText(546, 378, 628, 405, "新手试炼")
            if res2 or shou_ye1 or shou_ye2:
                # 避免首页识别到冒险手册，但存在未关闭的返回弹窗；兜底识别1次
                return3 = TomatoOcrTap(93, 1186, 126, 1220, '回', 10, 10)
                if return3:
                    Toast('返回首页')

                功能开关["needHome"] = 0
                if 任务记录["玩家名称"] == "":
                    self.zhiYeZhanLi()
                    Toast(
                        f'玩家：{任务记录["玩家名称"]}-战力：{任务记录["玩家战力"]}-职业：{任务记录["玩家-当前职业"]}已进入游戏')
                return True
            else:
                # 不在首页，尝试开始返回首页
                # 开始异步处理返回首页
                功能开关["needHome"] = 1
                功能开关["fighting"] = 0

            if tryTimes > 5:
                resConnErr, _ = TomatoOcrText(292, 691, 427, 722, "尝试重新连接")
                if resConnErr:
                    Toast('网络断开，尝试重启游戏')
                    # 结束应用
                    r = system.shell(f"am force-stop {功能开关['游戏包名']}", L())
                    # 重启游戏
                    return self.start_app()

            Toast(f'启动游戏，等待加载中，{attempt}/{max_attempt}')

            sleep(3)  # 等待游戏启动
        print('启动游戏失败，尝试重启游戏')
        # 结束应用
        r = system.shell(f"am force-stop {功能开关['游戏包名']}", L())
        # 重启游戏
        return self.start_app()

    def login(self):
        功能开关["needHome"] = 0
        功能开关["fighting"] = 1
        sleep(0.5)
        # 开始冒险之旅
        for i in range(2):
            login1, _ = TomatoOcrText(287, 1019, 339, 1049, "开始")  # 开始冒险之旅
            if login1:
                # 切换区服
                print(功能开关['选择启动区服'])
                print(任务记录['当前任务账号'])
                启动区服 = 0
                if 任务记录['当前任务账号'] != "":
                    if isinstance(任务记录['当前任务账号'], str):
                        当前账号 = 任务记录['当前任务账号'].replace('账号', '')
                    else:
                        当前账号 = 任务记录['当前任务账号']
                    if 当前账号 != 0 and 当前账号 != "" and 当前账号 != "0":
                        启动区服 = safe_int_v2(功能开关[f'账号{当前账号}启动区服'])
                if 功能开关['选择启动区服'] != "":
                    启动区服 = safe_int_v2(功能开关['选择启动区服'])
                if 启动区服 > 0:
                    Toast(f'准备切换区服-{启动区服}区')
                    # 检查当前区服
                    ifFind = False
                    for l in range(2):
                        if ifFind:
                            break
                        res, _ = TomatoOcrText(295, 943, 345, 980, f'{启动区服}服')
                        if res:
                            Toast(f'当前选择区服-{启动区服}区')
                            break
                        if not res:
                            Toast(f'切换启动区服-{启动区服}区')
                            tapSleep(358, 958, 0.7)
                            for k in range(10):
                                res = TomatoOcrFindRangeClick(f'{启动区服}服', x1=110, y1=339, x2=292, y2=615,
                                                              sleep1=0.7,
                                                              match_mode='fuzzy')
                                if res:
                                    ifFind = True
                                    break
                                sleep(0.5)
                                res = TomatoOcrFindRangeClick(f'{启动区服}服', x1=110, y1=339, x2=292, y2=615,
                                                              sleep1=0.7,
                                                              match_mode='fuzzy')
                                if res:
                                    ifFind = True
                                    break
                                if k < 5:
                                    Toast(f'下翻，寻找{启动区服}服')
                                    swipe(228, 552 + k, 228, 440)  # 下翻
                                if k > 5:
                                    Toast(f'上翻，寻找{启动区服}服')
                                    swipe(228, 430 + k, 228, 552)  # 上翻
                                sleep(1.5)
                                if k == 9:
                                    Toast(f'未找到，{启动区服}区角色')
                                    tapSleep(325, 1117, 1)  # 关闭选区界面
            if login1:
                break

        login2 = False
        for i in range(5):
            login1 = TomatoOcrTap(287, 1019, 339, 1049, "开始", sleep1=0.8)  # 开始冒险之旅
            # 开始冒险
            login2, _ = TomatoOcrText(302, 1199, 414, 1231, "开始冒险")
            if login2:
                break
        # 开始冒险
        if login2:
            self.switchRole(2, 任务记录['当前任务角色'])
        if not login1 and not login2:
            return self.start_app()

        login2 = TomatoOcrTap(302, 1199, 414, 1231, "开始冒险")

        # 跳过启动动画
        if login2:
            tapSleep(340, 930, 1)
            tapSleep(340, 930, 1)
            tapSleep(340, 930)
            sleep(5)
        # else:
        #     return self.start_app()

        shou_ye = False
        for loopCount in range(1, 4):  # 循环3次，从1到3
            shou_ye1, _, _ = TomatoOcrFindRange('冒险手册', 0.9, 360, 0, 720, 1280, '冒险手册')
            shou_ye2, _, _ = TomatoOcrFindRange('试炼', 0.9, 360, 0, 720, 1280, '试炼')
            # 避免首页识别到冒险手册，但存在未关闭的返回弹窗；兜底识别1次
            return3 = TomatoOcrTap(91, 1185, 127, 1221, '回', 10, 10)
            if return3:
                Toast('返回首页')
            if shou_ye1 or shou_ye2:
                Toast('已进入游戏')
                shou_ye = True
                sleep(0.5)  # 等待 3 秒

        # if not shou_ye:
        #     return self.start_app()

        return shou_ye

    def switchRole(self, ifRestart=1, selectRole=''):
        if (功能开关['选择启动角色'] == "false" and 功能开关['角色1开关'] == "false" and 功能开关[
            '角色2开关'] == "false" and 功能开关['角色3开关'] == "false" and 功能开关['角色4开关'] == "false" and
                功能开关['角色5开关'] == "false"):
            Toast('未配置角色切换')
            sleep(0.5)
            return
        if (功能开关['选择启动角色'] == 0 and 功能开关['角色1开关'] == 0 and 功能开关['角色2开关'] == 0 and
                功能开关['角色3开关'] == 0 and 功能开关['角色4开关'] == 0 and 功能开关['角色5开关'] == 0):
            Toast('未配置角色切换')
            sleep(0.5)
            return

        功能开关['fighting'] = 0
        功能开关['needHome'] = 0
        Toast('开始切换角色')

        # if ifRestart == 1:
        #     system.reboot()  # 重启应用让配置生效
        sleep(0.5)
        # 判断是否在角色切换页
        login1 = TomatoOcrTap(287, 1019, 339, 1049, "开始")  # 开始冒险之旅
        login2, _ = TomatoOcrText(302, 1199, 414, 1231, "开始冒险")
        if not login1 and not login2:
            # 重启应用
            # r = system.shell("am kill com.xd.cfbmf")
            Toast('切换角色，尝试重启游戏')
            r = system.shell(f"am force-stop {功能开关['游戏包名']}")
            system.open(self.app_name)
            sleep(5)
            for i in range(15):
                system.open(self.app_name)
                功能开关['fighting'] = 0
                功能开关['needHome'] = 0
                login1 = TomatoOcrTap(287, 1019, 339, 1049, "开始")  # 开始冒险之旅
                if login1:
                    break
                TomatoOcrFindRangeClick('', 0.9, 0.9, 6, 1084, 127, 1267, timeLock=5,
                                        offsetX=20, offsetY=20,
                                        keywords=[{'keyword': '返回', 'match_mode': 'fuzzy'},
                                                  {'keyword': '营地', 'match_mode': 'fuzzy'}])
                Toast(f'等待游戏加载{i}/15')
                sleep(5)
            else:
                Toast('返回登录界面失败，跳过角色切换')
                return

        任务记录['当前任务角色'] = safe_int(任务记录['当前任务角色'])
        下一角色 = 任务记录['当前任务角色'] + 1
        if selectRole != '':
            selectRole = safe_int(selectRole)
            下一角色 = selectRole
            if selectRole == '' or selectRole == 0:
                return

        if 下一角色 > 5:
            下一角色 = 1

        角色开关 = '角色' + str(下一角色) + '开关'
        # print(角色开关 + 功能开关[角色开关])
        if 功能开关[角色开关] == 0 or 功能开关[角色开关] == "false":
            Toast(角色开关 + '-未开启')
            sleep(0.3)
            任务记录['当前任务角色'] = 下一角色
            return self.switchRole(2)

        Toast('切换角色' + str(下一角色))
        res, _ = TomatoOcrText(302, 1199, 414, 1231, "开始冒险")
        if res == False:
            res5 = TomatoOcrTap(171, 1189, 200, 1216, "回")
            res6 = TomatoOcrTap(98, 1202, 128, 1231, "回")
            res7 = TomatoOcrTap(93, 1186, 127, 1217, "回")

        res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
        # dialog(下一角色)
        for p in range(3):
            if 下一角色 <= 3:
                swipe(190, 1090, 555, 1090, 300)  # 翻到最左
                sleep(1.5)
                swipe(150, 1090, 535, 1090, 300)  # 翻到最左
                sleep(1.5)
                swipe(210, 1090, 575, 1090, 300)  # 翻到最左
                sleep(2)
                x = 190 + (下一角色 - 1) * 157  # 从第一个角色 190，依次往右加 165 至下一角色
                y = 1090
                tapSleep(x, y, 1.5)
                res, _ = TomatoOcrText(300, 1197, 420, 1232, "选择职业")
                if res:
                    # 无该角色，退出
                    Toast('未创建角色' + str(下一角色))
                    res = TomatoOcrTap(70, 1198, 125, 1232, "返回")
                    任务记录['当前任务角色'] = 0
                    return self.switchRole(2)
                # 检查是否已选中
                re = FindColors.find("148,1076,#FDF2DE|148,1073,#FDF2DE|153,1081,#FDF2DE",
                                     rect=[x - 20, y - 20, x + 20, y + 20])
                if re:
                    Toast('已选中角色' + str(下一角色))
                    break

            if 下一角色 > 3:
                swipe(555, 1090, 190, 1090, 300)  # 翻到最右
                sleep(1.5)
                swipe(535, 1090, 170, 1090, 300)  # 翻到最右
                sleep(1.5)
                swipe(575, 1090, 210, 1090, 300)  # 翻到最右
                sleep(2)
                x = 540 - (5 - 下一角色) * 165  # 从第五个角色 540，依次往左减 165 至下一角色
                y = 1090
                tapSleep(x, y, 1.5)
                res, _ = TomatoOcrText(300, 1197, 420, 1232, "选择职业")
                if res:
                    # 无该角色，退出
                    res = TomatoOcrTap(70, 1198, 125, 1232, "返回")
                    任务记录['当前任务角色'] = 0
                    return self.switchRole(2)
                # 检查是否已选中
                re = FindColors.find("148,1076,#FDF2DE|148,1073,#FDF2DE|153,1081,#FDF2DE",
                                     rect=[x - 20, y - 20, x + 20, y + 20])
                if re:
                    Toast('已选中角色' + str(下一角色))
                    break
        任务记录['当前任务角色'] = 下一角色

    def switchAccount(self):
        功能开关["fighting"] = 0
        功能开关["needHome"] = 0
        if 任务记录['当前任务账号'] != "":
            tmpAccount = safe_int(任务记录['当前任务账号'])
            tmpAccount = tmpAccount + 1  # 切换下一账号
            for i in range(tmpAccount, 6):
                if 功能开关['账号' + str(i) + '开关'] == 1 or 功能开关['账号' + str(i) + '开关'] == "true":
                    任务记录['当前任务账号'] = i
                    return self.loadAccount(i)

            # 循环一遍后，重新执行
            for i in range(1, 6):
                if 功能开关['账号' + str(i) + '开关'] == 1 or 功能开关['账号' + str(i) + '开关'] == "true":
                    任务记录['当前任务账号'] = i
                    return self.loadAccount(i)
                return None
            return None
        return None

    def multiAccount(self):
        if 功能开关['账号1保存']:
            self.saveAccount(1)

        if 功能开关['账号2保存']:
            self.saveAccount(2)

        if 功能开关['账号3保存']:
            self.saveAccount(3)

        if 功能开关['账号4保存']:
            self.saveAccount(4)

        if 功能开关['账号5保存']:
            self.saveAccount(5)

        # 指定账号启动
        if 功能开关['选择启动账号'] != "" and 功能开关['选择启动账号'] != 0 and 功能开关['选择启动账号'] != "0":
            self.loadAccount(功能开关['选择启动账号'])

    def loadAccount(self, account_name):
        try:
            global 功能开关
            account_name = str(account_name)
            Toast('加载账号' + account_name)
            # 结束应用
            # r = system.shell("am kill com.xd.cfbmf", L())
            r = system.shell(f"am force-stop {功能开关['游戏包名']}", L())
            print(r)
            oldPath1 = f"/data/data/{功能开关['游戏包名']}/shared_prefs/"
            # 删除文件夹
            r = system.shell(f"rm -rf {oldPath1} 2>/dev/null", L())
            new_path1 = f"/data/data/{功能开关['游戏包名']}/accountConfig" + account_name + "_shared_prefs/"
            flag1 = system.shell(f"cp -r -a {new_path1} {oldPath1}", L())
            # oldPath2 = "/data/data/com.xd.cfbmf/"
            # new_path2 = "/data/data/com.xd.cfbmf/accountConfig" + account_name + "_shared_prefs/shared_prefs"
            # flag1 = system.shell(f"cp -r -a {new_path2} {oldPath2}", L())
            # print(flag1)
            configNum = 功能开关['账号' + str(account_name) + '配置']
            if configNum != 0 and configNum != '' and configNum != '0':
                Toast(f'加载账号{account_name} + 加载配置{configNum}')
                功能开关 = loadConfig(configNum, account_name)
                print(功能开关)
            # system.open("com.xd.cfbmf")
            # r = system.shell(f"am start -n com.xd.cfbmf")
            # r = system.shell("am kill com.xd.cfbmf")
            # r = system.shell("am force-stop com.xd.cfbmf")
            # system.open("com.xd.cfbmf")
            # r = system.shell(f"am start -a com.xd.cfbmf")
            # r = system.shell(f"am start -a com.xd.cfbmf")
            system.open(f"{功能开关['游戏包名']}")
            # system.open("出发吧麦芬")
        except Exception as e:
            # 处理异常
            # 获取异常信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # 输出异常信息和行号
            file_name, line_number, _, _ = traceback.extract_tb(exc_traceback)[-1]
            error_message = f"发生错误: {e} 在文件 {file_name} 第 {line_number} 行"
            # 显示对话框
            print(error_message)

    def saveAccount(self, account_name):
        account_name = str(account_name)
        old_path1 = f"/data/data/{功能开关['游戏包名']}/shared_prefs"
        new_path1 = f"/data/data/{功能开关['游戏包名']}/accountConfig" + account_name + "_shared_prefs"

        # 删除文件夹
        r = system.shell(f"rm -rf {new_path1} 2>/dev/null")
        # shutil.rmtree(new_path1, ignore_errors=True)
        # 新建文件夹
        # r = system.shell(f"mkdir -p {new_path1}")
        # os.makedirs(new_path1, exist_ok=True)
        # 复制文件夹
        flag1 = system.shell(f"cp -r -a {old_path1} {new_path1}")
        # flag1 = shutil.copytree(old_path1, new_path1, dirs_exist_ok=True)

        old_path2 = f"/data/data/{功能开关['游戏包名']}/app_webview"
        new_path2 = f"/data/data/{功能开关['游戏包名']}/accountConfig" + account_name + "_app_webview"

        # 删除文件夹
        r = system.shell(f"rm -rf {new_path2} 2>/dev/null")
        # shutil.rmtree(new_path2, ignore_errors=True)
        # 新建文件夹
        # r = system.shell(f"mkdir -p {new_path2}")
        # os.makedirs(new_path2, exist_ok=True)
        # 复制文件夹
        flag2 = system.shell(f"cp -r -a {old_path2} {new_path2}")
        # flag2 = shutil.copytree(old_path2, new_path2, dirs_exist_ok=True)

        # 复制文件夹及里面所有文件
        if flag1 is None and flag2 is None:
            Dialog.confirm(f"已保存账号 {account_name} 登录信息！请重新启动后继续配置")
        else:
            Dialog.confirm("保存失败！请检查是否授予root权限")
        system.exit()
        return True

    def zhiYeZhanLi(self):
        if 任务记录["玩家名称"] == "":
            res, name = TomatoOcrText(94, 78, 210, 102, '玩家名称')
            任务记录["玩家名称"] = name
        if 任务记录["玩家战力"] == "":
            res, fightNum = TomatoOcrText(113, 101, 193, 117, '玩家战力')
            if fightNum != "":
                if "万" in fightNum:
                    任务记录["玩家战力"] = float(fightNum.replace("万", "")) * 10000
                else:
                    任务记录["玩家战力"] = float(fightNum.replace("万", ""))
        # 识别当前职业
        if 任务记录['玩家-当前职业'] == '':
            re = CompareColors.compare(
                "34,75,#384458|37,78,#FEFEE3|34,77,#384458|37,78,#FEFEE3|37,83,#384458|31,85,#FEFEDD|30,78,#384458|41,78,#FEFEDC|39,85,#384458")
            if re:
                Toast('识别当前职业-战士')
                任务记录['玩家-当前职业'] = '战士'
        if 任务记录['玩家-当前职业'] == '':
            re = CompareColors.compare(
                "39,83,#384458|36,86,#FFFEE1|39,80,#585F68|33,83,#384458|33,80,#4A5260|34,77,#404A5B|34,75,#464F5E|34,77,#404A5B|36,78,#FFFEE1")
            if re:
                Toast('识别当前职业-服事')
                任务记录['玩家-当前职业'] = '服事'
        if 任务记录['玩家-当前职业'] == '':
            re = CompareColors.compare(
                "30,77,#B2B4A4|33,75,#CBCDBA|33,80,#374558|34,83,#374558|37,83,#FEFEE1|39,83,#FEFEE1|39,86,#374558")
            if re:
                Toast('识别当前职业-法师')
                任务记录['玩家-当前职业'] = '法师'
        if 任务记录['玩家-当前职业'] == '':
            re = CompareColors.compare(
                "34,75,#374558|39,78,#FDFDDD|31,78,#374558|34,75,#374558|36,80,#FFFEE1|37,77,#FEFEE3|39,83,#374558|34,83,#374558")
            if re:
                Toast('识别当前职业-游侠')
                任务记录['玩家-当前职业'] = '游侠'
        # if 任务记录['玩家-当前职业'] == '':
        #     Toast('识别当前职业-刺客')
        #     任务记录['玩家-当前职业'] = '刺客'


class L(ShellListener):
    def commandOutput(self, i: int, s: str):
        print('?', s)

    def commandTerminated(self, i: int, s: str):
        pass

    def commandCompleted(self, i: int, i1: int):
        pass
