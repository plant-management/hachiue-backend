import datetime

import netCDF4
import requests


# 天気情報取得用
def weather(lat, lon):
    params = {
        "lat": str(lat),
        "lon": str(lon),
        "units": "metric",
        "appid": "47323be29c7adfb45789b53971bc5311",
    }
    url = "http://api.openweathermap.org/data/2.5/weather"
    res = requests.get(url, params=params)
    k = res.json()
    w = str(k["weather"]).split(",")
    m = w[1].split(":")
    weat = str(m[1]).replace("'", "")  # 天気
    tmp = k["main"]["temp"]  # 気温
    hum = k["main"]["humidity"]  # 湿度
    return (weat, tmp, hum)


# lat=33.9576#緯度を入力
# lon=131.2711#経度を入力
# wth=weather(lat,lon)
# weather_icon = wth[0]#天気
# temp=wth[1]#気温
# humidity=wth[2]#湿度
# print(weather_icon, temp, humidity)#確認用


# 緯度経度の取得用
def location(post_code):
    post_code = str(post_code)
    # ハイフンが無ければ追加する
    if post_code[3] != "-":
        post_code = post_code[:3] + "-" + post_code[3:]
    params = {"zip": post_code + ",jp", "appid": "47323be29c7adfb45789b53971bc5311"}
    url = "http://api.openweathermap.org/data/2.5/weather"
    res = requests.get(url, params=params)
    k = res.json()
    return (k["coord"]["lat"], k["coord"]["lon"])


# post_code = "7550068"
# lat, lon = location(post_code) # 緯度経度を取得
# print(lat,lon)#確認用

# 日照量取得用
def get_sunlight_value(lat_val, lon_val):
    # 小数点以下2桁にする
    lat_val = round(float(lat_val), 2)
    lon_val = round(float(lon_val), 2)
    # 直近のデータを取得(30分前)
    dt_now = datetime.datetime.now(datetime.timezone.utc)
    dt_past = dt_now + datetime.timedelta(minutes=-31)
    yyyymmdd = dt_past.strftime("%Y%m%d")
    hh = dt_past.strftime("%H")
    mm = str(int(dt_past.strftime("%M")) // 10 * 10)
    hhmm = hh + mm
    nc = netCDF4.Dataset(
        "H08_" + yyyymmdd + "_" + hhmm + "_rFL010_FLDK.02701_02601.nc", "r"
    )
    # nc= netCDF4.Dataset('H08_20210929_1650_rFL010_FLDK.02701_02601.nc','r')#確認用
    val = nc.variables["PAR"][:]
    lat = nc.variables["latitude"][:]  # 緯度情報（0-2600,北緯50.0-24.0,0.01度刻み）
    lon = nc.variables["longitude"][:]  # 経度情報（0-2700,東経123.0-150,0.01度刻み）
    lat1 = []
    lon1 = []
    for t in lat:
        lat1.append(str(round(t, 2)))
    for t in lon:
        lon1.append(str(round(t, 2)))
    if 24.0 <= lat_val <= 50.0 and 123.0 <= lon_val <= 150.0:
        lat_no = lat1.index(str(lat_val))
        lon_no = lon1.index(str(lon_val))
    else:
        print("location BAD")
        exit()
    return val[lat_no][lon_no]


# lat=33.9576#緯度を入力
# lon=131.2711#経度を入力
# sunlight=get_sunlight_value(lat, lon)#日照度を取得する
# print(sunlight)#確認用
