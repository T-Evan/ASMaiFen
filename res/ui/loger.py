
from ascript.android.system import R
# 导入-屏幕检索库
from ascript.android.ui import WebWindow
from ascript.android.ui import Loger

def tunner(k,v):
    print(k,v)

# loger 继承 Window ,因此 Window 中的方法,loger都可以使用
lw = loger(R(__file__).ui("loger.html"))
lw.tunner(tunner) # 设置消息通道
lw.show() # 展示

# lw.close()


