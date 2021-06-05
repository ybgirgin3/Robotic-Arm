# tarih ve saat isimli rapor oluşturacak
from datetime import datetime 
from time import sleep
import os

date_ = datetime.now().strftime("%Y-%m-%d %H:%M")
os.mkdir(date_)

fname ="{0}.md".format(date_)

sleep(1.5)
# with open(fname, 'a') as f:
f = open(f"{date_}/{fname}", "x")

if not f:
    raise("dosya zaten mevcut")

