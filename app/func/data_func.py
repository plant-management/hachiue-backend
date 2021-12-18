import datetime
import random

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
    if hhmm == "0240":
        hhmm = "0230" 
    if hhmm == "1440":
        hhmm = "1430"
    nc = netCDF4.Dataset(
        "./eisei/H08_" + yyyymmdd + "_" + hhmm + "_rFL010_FLDK.02701_02601.nc", "r"
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
    return float(val[lat_no][lon_no])


# lat=33.9576#緯度を入力
# lon=131.2711#経度を入力
# sunlight=get_sunlight_value(lat, lon)#日照度を取得する
# print(sunlight)#確認用


def select_comment(moisture, sunlight):
    comment = []

    # 時間
    dt_now = datetime.datetime.now()
    hh = int(dt_now.strftime("%H"))
    if 0 <= hh < 2:
        comment.append("おやすみー。")
    elif 2 <= hh < 6:
        comment.append("zzz")
    elif 6 <= hh <= 10:
        comment.append("おはよー。今日も一日頑張ろうね!")
    elif 10 < hh <= 17:
        comment.append("こんにちは!")
    elif 17 < hh <= 20:
        comment.append("こんばんは!")
    elif 20 < hh <= 24:
        comment.append("もう夜だねー。")

    # 日照量
    if 0 <= sunlight < 500:
        comment.append("外暗いねー。")
    elif 500 <= sunlight < 700:
        comment.append("ちょっと暗いね。ちょっとだけ。")
    elif 700 <= sunlight < 1000:
        comment.append("日向ぼっこはいいねー。ずっとこうしていたいよ。")
    elif 1000 <= sunlight:
        comment.append("日差しが強いねー。日焼けしそうだよ…。")
    # 土壌水分
    if 0 <= moisture < 33:
        comment.append("のどがカラカラだよー")
    elif 33 <= moisture <= 66:
        comment.append("今日はすごく気持ちがいいな!")
    elif 66 < moisture <= 100:
        comment.append("じめじめするー。")

    # 今後追加するかも…
    """
    #天気
    if(weather_icon=="Thunderstorm"):#雷雨
        comment.append('雨ひどいねー。こんな日は外出たくないよー。')
    elif(weather_icon=="Drizzle"):#霧雨
        comment.append('ねー。見てみて。霧が濃くてなんも見えん笑')
    elif(weather_icon=="Rain"):#雨
        comment.append('恵みの雨!雨ごいした甲斐があったよー')
    elif(weather_icon=="Snow"):#雪
        comment.append('ゆっ、雪だーー。雪だるま作ろうよ')
    elif(weather_icon=="Clear"):#晴天
        comment.append('おー、雲一つない空!')
    elif(weather_icon=="Clouds"):#雲
        comment.append('雲がモクモクだね。モクモク。')
    
    #気温
    if(15<=temp<=25):
        comment.append('心地いいねー')
    elif(10<=temp<15):
        comment.append('ちょっと冷えるね')
    elif(temp<10):
        comment.append('寒いよー')
    elif(25<temp<30):
        comment.append('ちょっと暑いねー')
    elif(30<temp):
        comment.append('暑すぎだよー')
    """

    return comment[random.randrange(len(comment))]


# sunlight_val=1087.3#日照度を入力
# moisture_val=45#土壌水分量を入力
# #今後使うかも
# '''
# weather_icon='Clouds'
# temp=35.2
# humidity=67
# '''
# text=select_comment(moisture=moisture_val,sunlight=sunlight_val)#コメントを選定する

# # print(text)#確認用

# 表情変更用
def satisfact(sunlight, moisture, health):
    dt_now = datetime.datetime.now()
    hh = int(dt_now.strftime("%H"))
    if 0 <= hh < 7 or 19 <= hh <= 24:
        sunlight_res = 1
    elif 7 <= hh < 19:
        if 0 <= sunlight < 500:
            sunlight_res = 1 / 3
        elif 500 <= sunlight < 700:
            sunlight_res = 2 / 3
        elif 700 <= sunlight < 1000:
            sunlight_res = 3 / 3
        elif 1000 <= sunlight:
            sunlight_res = 1 / 2

    if 0 <= moisture < 33:
        moisture_res = moisture / 49.5
    elif 33 <= moisture <= 66:
        moisture_res = (49.5 - abs(moisture - 49.5)) / 49.5
    elif 66 < moisture <= 100:
        moisture_res = (100 - moisture) / 49.5

    health_res = health / 3

    return (sunlight_res + moisture_res + health_res) / 3


#天気の変更関数
def weather_icon_select(weather_icon):
    weather_icon = weather_icon.strip()
    if(weather_icon=="Thunderstorm"):#雷雨
        weather_icon = "rain"
    elif(weather_icon=="Drizzle"):#霧雨
        weather_icon = "rain"
    elif(weather_icon=="Rain"):#雨
        weather_icon = "rain"
    elif(weather_icon=="Snow"):#雪
        weather_icon = "rain"
    elif(weather_icon=="Clear"):#晴天
        weather_icon = "sunny"
    elif(weather_icon=="Clouds"):#雲
        weather_icon = "cloud"

    return weather_icon