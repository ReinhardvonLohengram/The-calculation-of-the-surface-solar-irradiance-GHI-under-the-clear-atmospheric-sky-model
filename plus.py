from pvlib import location
from pvlib import irradiance
import pandas as pd
from matplotlib import pyplot as plt

tz='Asia/Shanghai'
# 哈尔滨地区纬度、经度
lat, lon = 45.739, 120.683

# 创建本地对象，存储维度、经度、时区
site = location.Location(lat, lon, tz=tz)

# 计算晴天的GHI并将其转换到阵列的平面
# 定义函数，获取某个地方的辐照度（理论标准辐照度）
def get_irradiance(site_location, date, tilt, surface_azimuth):
    # 创建一天间隔10分钟的时间序列
    times = pd.date_range(date, freq='1min', periods=60*24,tz=site_location.tz)
    #使用默认的内部模型生成晴天数据
    #get_ clearsky方法返回具有GHI、DNI和DHI值的数据表
    clearsky = site_location.get_clearsky(times)
    # 获取太阳方位角和天空顶点以传递到函数
    solar_position = site_location.get_solarposition(times=times)
    # 使用get_total_iradiance函数将GHI转换为POA

    return pd.DataFrame({'GHI': clearsky['ghi'],'DNI': clearsky['dni'],'DHI': clearsky['dhi']})
#获取夏至和冬至的辐照度数据，假设倾斜25度，和朝南的阵列
summer_irradiance = get_irradiance(site, '06-21-2022', 25, 180)
winter_irradiance = get_irradiance(site, '12-22-2022', 25, 180)

# 转换时间序列为小时：分钟，方便绘图
summer_irradiance.index = summer_irradiance.index.strftime("%H:%M")
winter_irradiance.index = winter_irradiance.index.strftime("%H:%M")

plt.rcParams['figure.figsize']= 12,4
plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False
plt.rcParams.update({"font.size":11})
# 画夏季和冬季的 GHI  POA
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
summer_irradiance['GHI'].plot(ax=ax1, label='GHI')
summer_irradiance['DNI'].plot(ax=ax1, label='DNI')
summer_irradiance['DHI'].plot(ax=ax1, label='DHI')
winter_irradiance['GHI'].plot(ax=ax2, label='GHI')
winter_irradiance['DNI'].plot(ax=ax2, label='DNI')
winter_irradiance['DHI'].plot(ax=ax2, label='DHI')
ax1.set_xlabel('日时间序列 (夏季)')
ax2.set_xlabel('日时间序列 (冬季)')
ax1.set_ylabel('辐照度 ($W/m^2$)')
ax1.legend()
ax2.legend()
plt.show()
print(summer_irradiance['GHI'])