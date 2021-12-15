import pytz, base64, uuid
from PIL import Image
from ctypes import resize
from datetime import datetime


# #経過日数取得用[関数]
def calc_progress_day(time1):
    date1 = time1.date()
    time2 = datetime.now(pytz.timezone("Asia/Tokyo"))
    date2 = time2.date()
    day = date2 - date1
    return day


#png→base64に変換
def png_to_base64(img_path):
    img_resize = Image.open(img_path).resize((150,150)) #ここ処理は取得時に行う
    img_resize.save(img_path)                           #ここ処理は取得時に行う
    img_data = open(img_path,"rb").read()
    b64_data = base64.b64encode(img_data).decode('utf-8')
    return b64_data
# print(png_to_base64("test1.png"))


# base64→pngに変換
def b64_to_png(Base64_image, UPLOAD_FOLDER):    
    #character画像の保存先パス
    plant_image_path = UPLOAD_FOLDER + str(uuid.uuid4()) + ".png" 
    img = base64.b64decode(Base64_image.encode())
    with open(plant_image_path, 'bw') as b64_buffer:
        b64_buffer.write(img)
    return plant_image_path