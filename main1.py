import math
from datetime import datetime
import datetime
from pysolar.solar import get_altitude
from pvlib import location
import pandas as pd
from PyQt5 import  QtWidgets, uic
from PyQt5.QtWidgets import QApplication
class mainwin():# 主窗口
    def __init__(self):# 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi('main.ui')
        self.ui.simple.clicked.connect(lambda:self.calculate_irradiance(self.ui.localtime.dateTime().toString("yyyy-MM-dd hh:mm:ss"), self.ui.lat.value(), self.ui.lon.value(), self.ui.utctimezone.value()))
        self.ui.clearsky.clicked.connect(lambda:self.clearsky(location.Location(self.ui.lat.value(), self.ui.lon.value(), tz=self.ui.timezone.toPlainText()), self.ui.localtime.dateTime().toString("yyyy-MM-dd hh:mm:ss")))#菜单栏的选择文件

    def clearsky(self, site_location, time_str):
        cur_time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        times = pd.date_range(start='2008-06-25 14:35', freq='1min', periods=20, tz=site_location.tz)
        # 使用默认的内部模型生成晴天数据start=f'{cur_time.year}-{cur_time.month}-{cur_time.day} {cur_time.hour}:{cur_time.minute}'
        # get_ clearsky方法返回具有GHI、DNI和DHI值的数据表
        clearsky = site_location.get_clearsky(times)
        irradiance = pd.DataFrame({'GHI': clearsky['ghi'], 'DNI': clearsky['dni'], 'DHI': clearsky['dhi']})
        irradiance.index = irradiance.index.strftime("%H:%M")
        output = str(irradiance['GHI'].iloc[0])
        self.printf(output)
    def calculate_irradiance_base(self,day_year, latitude, longitude, utc):
        """
        北纬为正，东经为正
        latitude:所在维度
        longitude:所在经度
        longitude_time:电站所采用时区的中心经度
        """
        G_0 = 1368  # 取太阳常数为1368（W/m2）
        k = 1 + 0.034 * (math.cos(2 * math.pi / 365 * day_year))        # 计算日地距离修正系数

        altitude = get_altitude(latitude, longitude, utc)
        print(altitude)
        G = k * G_0 * math.sin(altitude/180*math.pi)
        if G < 0:
            G = 0
        self.printf(f'{G}')

    def calculate_irradiance(self, time_str, latitude, longitude, utctime):
        """从datetime类型的时间计算当前大气外理论辐照度"""
        cur_time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        print(cur_time)
        day_year = int(datetime.datetime.strftime(cur_time, '%j'))   # j是积日
        utc = datetime.datetime(cur_time.year, cur_time.month, cur_time.day, cur_time.hour, cur_time.minute, 1, 130320, tzinfo=datetime.timezone(datetime.timedelta(hours=utctime)))
        print(utc)
        return self.calculate_irradiance_base(day_year, latitude, longitude, utc)

    def printf(self, mes):
        self.ui.textBrowser.append(mes)  # 在指定的区域显示提示信息
        self.ui.textBrowser.ensureCursorVisible()
if __name__ == '__main__':
    app = QApplication([])
    Qmainwin = mainwin()  # 创建主窗口
    Qmainwin.ui.show()  # show出窗口
    app.exec_()  # 维持窗口
