# 导包
from time import sleep

from ascript.android import system
from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .res.ui.ui import switch_lock
from .baseUtils import *
from threading import Lock
from ascript.android.screen import FindColors


# 实例方法
def main():
    while True:
        if 功能开关["needHome"] == 1 and 功能开关["fighting"] == 0:
            print("返回首页处理线程 - 运行中")
            returnHome()
            sleep(1)  # 等待 1 秒
        else:
            sleep(1)  # 等待 5 秒


def returnHome():
    for i in range(4):
        return1 = False
        return2 = False
        return3 = False
        return4 = False
        return5 = False
        if 功能开关["needHome"] == 1 and 功能开关["fighting"] == 0:
            return1 = TomatoOcrTap(67, 1182, 121, 1221, '返回', 10, 10)
            return3 = TomatoOcrTap(91, 1185, 127, 1221, '回', 10, 10)
        if i > 2 and (return1 and 功能开关["needHome"] == 1 and 功能开关["fighting"] == 0) or (return3 and 功能开关["needHome"] == 1 and 功能开关["fighting"] == 0):
            # 返回上级页面时二次确认入口通用处理
            sleep(0.2)
            re = TomatoOcrFindRangeClick(x1=39,y1=250,x2=674,y2=1205,keywords=[{'keyword': '确定', 'match_mode': 'exact'},{'keyword': '确认', 'match_mode': 'exact'}])
            Toast('返回首页')

        if not return1 and not return3 and 功能开关["fighting"] == 0:
            return6 = TomatoOcrTap(89,1197,136,1220, '返回', 10, 10)
            if not return6:
                return5 = TomatoOcrTap(69, 1182, 127, 1220, '营地', 10, 10)
                if not return5:
                    # return2 = imageFindClick('返回_1')
                    return2 = TomatoOcrTap(86,1193,140,1224, '返回', 10, 10)
                    if return2 and 功能开关["needHome"] == 1:
                        Toast('返回首页')

                    return4 = imageFindClick('返回_2')
                    if return4 and 功能开关["needHome"] == 1:
                        Toast('返回首页')

        if not return1 and not return2 and not return3 and not return4 and 功能开关["needHome"] == 1 and 功能开关["fighting"] == 0:
            # 识别是否进入首页
            # 点击首页-冒险
            # re = TomatoOcrTap(330, 1201, 389, 1238, '冒险')

            # 判断底部冒险图标
            res2 = FindColors.find(
                "323,1210,#FCF8EE|333,1210,#FCF8ED|336,1212,#F9ECCB|336,1234,#FEF8E9|347,1231,#FCF8EE|363,1231,#FEF7EB|377,1229,#F4EFE1|372,1218,#88684E|353,1216,#9E8776",
                rect=[301, 1130, 421, 1273])
            shou_ye1 = False
            shou_ye2 = False
            if not res2:
                shou_ye1, _ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
                if not shou_ye1:
                    shou_ye2, _ = TomatoOcrText(627, 381, 710, 403, "新手试炼")
                # 暂不处理，提高执行效率
                # if not shou_ye1:
                #     shou_ye2 = TomatoOcrFindRange('冒险手册', 0.9, 360, 0, 720, 1280, '冒险手册')
                # shou_ye2 = TomatoOcrFindRange('试炼', 0.9, 360, 0, 720, 1280, '试炼')
            if res2 or shou_ye1 or shou_ye2:
                功能开关["needHome"] = 0
                Toast('已返回首页')
                return True

        # # 兜底
        # if i == 3:
        #     # 开始冒险之旅
        #     login1 = TomatoOcrTap(282, 1017, 437, 1051, "开始冒险之旅")
        #     # 开始冒险
        #     login2 = TomatoOcrTap(302, 1199, 414, 1231, "开始冒险")

    return
