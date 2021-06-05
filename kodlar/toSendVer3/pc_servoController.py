#import pigpio
from termcolor import colored
from numpy import interp
import time

# servo pinleri
panServo = 4
tiltServo = 17

# temp values
wristServo = 10
elbowServo = 11

# en baştaki pozisyon
panPos = 1500
tiltPos = 1500

# yarım açık olsunlar
elbowPos = 750
wristPos = 750

# idle values
idle_panPos = 1500
idle_tiltPos = 1500

"""
servo = pigpio.pi()
servo.set_servo_pulsewidth(panServo, panPos)
servo.set_servo_pulsewidth(tiltServo, tiltPos)
"""

minMov = 1
maxMov = 10

# bu şekilde oluyor
#print(colored("wrist opened", "blue"))
print(colored("bilek açıldı", "blue"))

# first func
# panning and tilting
# works
def panAndTilt(x, y, w, h) -> int:
    """
    :param1: x-axis of the current frame
    :param2: y-axis of the current frame
    :param3:  width of the current frame (?)
    :param4: height of the current frame (?)

    verilen değerlere göre panning ve tilting servolarına değişimde bulunuyor

    görev:
        np.interp fonksiyonu yardımı ile hesaplama yaptırıp
        azar azar servolara açılmaları için komutlar veren fonk

    """
    # open elbow

    global panPos
    global tiltPos

    global idle_panPos 
    global idle_tiltPos 

   # int(x+(w/2)) > 360 means flame is on the right side of the frame
    if int(x+(w/2)) > 360:
        panPos = int(panPos - interp(int(x+(w/2)), (360, 640), (minMov, maxMov)))

    # int(x+(w/2)) < 280 means flame is on the left side of the frame
    elif int(x+(w/2)) < 280:
        panPos = int(panPos + interp(int(x+(w/2)), (280, 0), (minMov, maxMov)))

    if int(y+(h/2)) > 280:
        tiltPos = int(tiltPos + interp(int(y+(h/2)), (280, 480), (minMov, maxMov)))

    elif int(y+(h/2)) < 200:
        tiltPos = int(tiltPos - interp(int(y+(h/2)), (200, 0), (minMov, maxMov)))

    # control tilting idle
    if  is_idle(idle_tiltPos, tiltPos, idle_panPos, panPos):
        wristAndElbow(x, y, w, h)
    else: 
        # servoların değerlerini servolara gönder
        # panning servo
        if not panPos > 2500 or not panPos < 550:
            #servo.set_servo_pulsewidth(panServo, panPos)
            print('panServo: {}'.format(colored(panPos, "yellow")))

        
        # tilting servos
        if not tiltPos > 2500 or tiltPos < 550:
            #servo.set_servo_pulsewidth(tiltServo, tiltPos)
            print('tiltServo: {}'.format(colored(tiltPos, "yellow")))


    # servoların idle değerleri
    idle_tiltPos = tiltPos 
    idle_panPos = panPos


def wristAndElbow(x, y, w, h) -> int:
    """
    :param1: x-axis of the current frame
    :param2: y-axis of the current frame
    :param3: width of the frame (?)
    :param4: height of the frame (?)

    verilen frame değerlerine göre
    tıpkı panning ve tilting fonksiyonunda olduğu gibi
    wrist ve elbow servolarını kontrol eden fonksiyon

    """

    global elbowPos
    global wristPos


    # elbow
    #elbowPos = int(elbowPos + interp(int(x+(w/2)), (360, 640), (minMov, maxMov)))
    elbowPos = int(elbowPos + interp(int(x+(w/2)), (360, 640), (20, 100)))

    # elbow post 2400 değerine geldiğinde duruyor 
    # o andan sonra elin açılması sağla
    if not elbowPos > 2400 or elbowPos < 700:
        #print(f"elbowPos: {colored(elbowPos, 'green')}")
        print(f"dirsek açısı: {colored(elbowPos, 'green')}")
        # kol kapandıktan sonra
        if elbowPos == 2390:
            #print("wrist closed")
            print("bilek kapandı")
            #print("elbow started to close")
            print("dirsek kapanmaya başladı")
            #elbowPos = int(elbowPos - interp(int(x+(w/2)), (360, 640), (20, 100)))
            # elbowPos'u hızlıca kapat
            step = 10
            for _ in range(step):
                # 10 hamle de elbowPos'u sıfırla
                elbowPos = elbowPos / step
                time.sleep(0.3)
                #print(f"elbowPos: {colored(elbowPos, 'green')}")
                print(f"dirsek açısı: {colored(elbowPos, 'green')}")

            # uygulamayı kapat
            from sys import exit
            exit(0)


def is_idle(idle1, curr1, idle2, curr2) -> bool:
    """
    :param1: idle1 value,
    :param2: current1 value,
    :param3: idle2 value,
    :param4: current2 value

    :return: bool 

    iki tane değer döndüreceğim
    eğer iki değerde birbirinin aynısı ise
    dirsek servolarını çalıştırmaya başlayacak

    görev:
        verilen değerlerden bir tanesi bile eğer değişmeyi bıraktıysa
        yavaş yavaş dirsek ve bilek servoları çalışmaya başlasın
        eğer merkezden kayma olacaksa panning ve tilting servoları 
        hatayı kapatmak için gerekli olan hamleleri yapacaktır

    """

    # eğer değerlerden bir tanesi bile hareket etmeyi bırakırsa
    # bool dön
    def idleControl(idle, curr) -> bool:
        # bool to return
        inCenter = None
        if idle == curr:
            #print("value not changing")
            inCenter = True
        else:
            #print(f"{name} == {curr}")
            inCenter = False
    
        return inCenter

    # birinci ve ikinci değerler için   
    if idleControl(idle1, curr1) and idleControl(idle2, curr2):
        return True
