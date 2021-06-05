#from servoController import panAndTilt, wristAndElbow
from pc_servoController import panAndTilt, wristAndElbow
from skimage import measure
from time import sleep
import numpy as np
import cv2

# birincil kameradan verileri oku
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('inputs/ball.mp4')

# varsayılan olarak gelen 
# video yükseklik ve genişliğini değiştir
H = 480
W = 640

# videodan fpsleri al
fps = int(cap.get(cv2.CAP_PROP_FPS))

# video olarak okunması için sonsuz döngü içine al
while True:
    succ, frame = cap.read()
    # eğer okuma başarılı değilse dosya bulunamadı hatası ver
    # uygulamayı kapat
    if not succ:
        raise FileNotFoundError("Girdi dosyası bulunamadı")
        break

    # bazı videolarda yüksek fps durumu olduğundan dolayı 
    # hız yavaşlatma durumu uygulamamız gerekebilir
    # sleep(3 / fps)

    # resim karesini üstte belirlediğimiz 
    # ölçülere getiriyoruz
    frame = cv2.resize(frame, (W,H))

    # hsv tarzından renk ayrımı yapıyoruz
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # kırmızı renk için gerekli olan 
    # alt ve üst değerlerini ayarla 
    lowRed  = np.array([163, 74, 30])
    highRed = np.array([179, 255, 255])

    # renk değerlerini bir maske olarak opencv'ye tanıt
    redMask = cv2.inRange(hsv, lowRed, highRed)
    red = cv2.bitwise_and(frame, frame, mask = redMask)

    # kontür ayarlamalarını yap (bir liste olarak sıralıyor sanırım) ( köşe ayarlamaları olarak düşünebiliriz)
    cntRed = cv2.findContours(redMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2]
    # bulunan köşe listelerini sıralar
    cnts = sorted(cntRed, key = lambda x:cv2.contourArea(x), reverse=True)

    # bulunan köşelerin her birinin çapını, resim karesi üzerindeki konumunu bul
    for cnt in cnts:
        (x, y, w, h) = cv2.boundingRect(cnt)
        # Getting Position of rectangle & line colour & thickness
        cv2.rectangle(frame, (x , y) , (x + w, y + h) , (0, 255, 0), 2)
        x_medium = int((x+x+w) / 2)
        y_medium = int((y+y+h) / 2)

        # verileri dosyaya yaz
        with open("information.txt", "a") as f:
            toWrite = """
                object: x: {}, y: {}
                        w: {}, h: {}
                """.format(x, y, w, h)
            f.write(toWrite)

        # servo fonksiyonlarına yolla
        panAndTilt(x, y, w, h)
        break

    # üzerinde işlem yapılan resim karesini 
    # ekranda göster
    cv2.imshow("frame", frame)

    # q tuşuna basıldığından işlemi bitir
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# gösterim işlemini
# işlem tamamlandığından
# kapat
cap.release()
cv2.destroyAllWindows()

