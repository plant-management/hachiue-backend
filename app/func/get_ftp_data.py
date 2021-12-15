import datetime
from ftplib import FTP

# 日照の衛星情報取得用
def get_ftp():
  config={
      'host': 'ftp.ptree.jaxa.jp',
      'user': 'b039vdv_yamaguchi-u.ac.jp',
      'passwd': 'SP+wari8'
  }
  dt_now=datetime.datetime.now(datetime.timezone.utc)
  if('dt_now' in locals()):
    dt_past=dt_now + datetime.timedelta(minutes=-30)
    #print('now')
  yyyymm=dt_past.strftime('%Y%m')
  dd=dt_past.strftime('%d')
  hh=dt_past.strftime('%H')
  mm=str(int(dt_past.strftime('%M'))//10*10)
  hhmm=hh+mm
  dir='/pub/himawari/L2/PAR/010/'+ yyyymm+ '/'+ dd+'/'+hh
  filenname='H08_'+ yyyymm+ dd+ '_'+ hh+ mm+ '_rFL010_FLDK.02701_02601.nc'
  #02:40-02:50UTCと14:40-14:50UTCは取得しない(02:40と14:40のデータはない)
  if(hhmm!= '0240' or hhmm!= '1440'):
    with FTP(**config) as ftp:
      ftp.cwd(dir)
      with open(filenname,'wb') as fp:
        ftp.retrbinary("RETR "+ filenname, fp.write)
      ftp.close()

get_ftp()#日照データをファイルとして取得する