"""
*1.
https://drive.google.com/drive/folders/1nLAgHSuMhNH3ieTT7ZUl4p6LQJ3uCR_J?usp=sharing  +

bu linkteki 2 adet rar dosyasını indirin  +

2 dosyanın içerisinde de düzenlenmemiş datalar bulunmakta.  +

datalar cift halinde her .jpg dosyasının aynı ada sayıh .txt dosyası vardır  

bu dataları 0 dan başlayarak yeni isimler veren bir program yazmanız gerekmektedir.

deneme.jpg, deneme.txt ----->>>>> 0.jpg, 0.txt"""
"""
*1.
https://drive.google.com/drive/folders/1nLAgHSuMhNH3ieTT7ZUl4p6LQJ3uCR_J?usp=sharing  +

bu linkteki 2 adet rar dosyasını indirin  +

2 dosyanın içerisinde de düzenlenmemiş datalar bulunmakta.  +

datalar cift halinde her .jpg dosyasının aynı ada sayıh .txt dosyası vardır  

bu dataları 0 dan başlayarak yeni isimler veren bir program yazmanız gerekmektedir.

deneme.jpg, deneme.txt ----->>>>> 0.jpg, 0.txt
deneme2.jpg, deneme2.txt ----->>>>> 1.jpg, 1.txt

*yeni isimlendirilen dosyalar farklı bir dosyaya alınmalı
*txt ve jpg ler aynı dosya içinde olmalı
*eşi olmayan dosya başka bir not defterine not edilmeli
kafanızda takılan bir sorun varsa bana ulaşın
"""

import os
import shutil


def jpg_txt_ritmik_sirala(jpg_yolu,txt_yolu,generate_yolu):
   
    jpg_list = []
    txt_list = os.listdir(txt_yolu)

    for item_jpg in os.listdir(jpg_yolu): 
     if not item_jpg.startswith('.') and item_jpg[-4:] == ".jpg" and os.path.isfile(os.path.join(jpg_yolu, item_jpg)):
        jpg_list.append(item_jpg)
    
    for i in range(len(jpg_list)):
        if jpg_list[i][:len(jpg_list[i])-4]+".txt" in txt_list:
            shutil.copyfile(jpg_yolu+jpg_list[i],generate_yolu+"{}.jpg".format(i))   
            shutil.copyfile(txt_yolu+jpg_list[i][:len(jpg_list[i])-4]+".txt",generate_yolu+"{}.txt".format(i))
        else:
            shutil.copyfile(jpg_yolu+jpg_list[i],generate_yolu+"{}.jpg".format(i))  
            open(generate_yolu+"{}.txt".format(i),"w")

jpg_txt_ritmik_sirala("/Users/mustafasevinc/Desktop/datas/","/Users/mustafasevinc/Desktop/yolo_label/","/Users/mustafasevinc/Desktop/Tum_Dosyalar/")  #lütfen jpg ve txt leri ayrı klasörlerde bulundurunuz


"""
*2.
herhangi bir similasyon ortamında (gazebo yada mavproxy), 1 adet döner kanata
"""

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil

drone1 = connect("127.0.0.1:14550", wait_ready=True, timeout=30)

#1. pre-arm check
def pre_arm_check():
    while not drone1.is_armable:
        print("Kalkışa Hazır Değiliz.")
        print("Arm Durumu: {}".format(drone1.armed))

#2. takeoff

def takeoff(kac_metre):
   
    drone1.mode = VehicleMode("GUIDED")
    time.sleep(1)
    print("Araç Modu: {}".format(drone1.mode))
    drone1.armed=True
    time.sleep(1)
    print("Drone Armed: {}".format(drone1.armed))
    print("Drone Yükseliyor")
    drone1.simple_takeoff(kac_metre)
    while(drone1.location.global_relative_frame.alt <=kac_metre*0.95):
        time.sleep(1) 

    print("Dron Yerel Yüksekliği: {}".format(drone1.location.global_relative_frame.alt))

#3. simplegoto kullanarak verilen xyz ye gitme(burda kullanılan ortamlar xyz kordinatı kullanmaz gps kullanır verilen xyz yi gps e cevirip fonksiyona o şekilde vermeniz lazım)

def simplegoto(konum_x,konum_z,konum_y):
    
    try:
        move_point = LocationGlobalRelative(konum_x, konum_z, konum_y)
        drone1.simple_goto(move_point)
        
        while not (konum_y-0.01<=drone1.location.global_relative_frame.alt <= konum_y+0.01 and konum_x-0.01<=drone1.location.global_relative_frame.lat<=konum_x+0.01 and konum_z-0.01<=drone1.location.global_relative_frame.lon<=konum_z+0.01):
            print("Konuma Gidiliyor,  {}".format(drone1.location.global_relative_frame))
            time.sleep(1)
        #buraya bi sleep eklemek lazım unutma!
        
    except:
        print("Girilen Kordinatlarda Hata Var.")

#4. dronu vektorel olarak kontrol (ex: x yönüne 4 mt/s ile t saniye ilerle.)

def send_global_velocity(velocity_x, velocity_y, velocity_z, duration):

    msg = drone1.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, # lat_int - X Position in WGS84 frame in 1e7 * meters
        0, # lon_int - Y Position in WGS84 frame in 1e7 * meters
        0, # alt - Altitude in meters in AMSL altitude(not WGS84 if absolute or relative)
        # altitude above terrain if GLOBAL_TERRAIN_ALT_INT
        velocity_x, # X velocity in NED frame in m/s
        velocity_y, # Y velocity in NED frame in m/s
        velocity_z, # Z velocity in NED frame in m/s
        0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    for i in range(0,duration):
        drone1.send_mavlink(msg)
        time.sleep(2)


#5. return to home and land
def rtl():
    drone1.mode = VehicleMode("RTL")
    print("Araç Modu: {}".format(drone1.mode))
    while drone1.armed:
        time.sleep(2)
        print("Kalkış Konumuna Dönülüyor")
    print("İniş Başarılı Gibi Duruyor.")
    print("Drone Arm Durumu: {}".format(drone1.armed))

"""
sıralanan şeyleri yaptırın bunların similasyon ortamında gercek drone gibi hareket etmeleri gerekmektedir. şuanki planlar cercevesinde bunun eğitimi benim tarafımdan verilmesi planlanmaktadır. planda herhangi bir sorun yada erken ilerleme durumunda dronekit dökümantasyonları kullanılarak yapılabilir.
"""
pre_arm_check()
takeoff(10)
simplegoto(drone1.location.global_relative_frame.lat+0.002 , drone1.location.global_relative_frame.lon-0.001 , 5)    
send_global_velocity(3,0,4,5)#çokta güzel bir metod değil çünkü fps e göre aldığı yol değişiyor. 
rtl()


"""
*3.
kısımda yaptığınız şeylerin aynısını sabit kanat ile tekrar deneyin ve farklarına bakın (vektorel hareket kısmı bir miktar farklı araştırma yapmanız gerekmekte)
----------------------------------------------------------------
"""

plane1 = connect("127.0.0.1:14550",wait_ready=True,timeout=30)

def plane_pre_arm_check():
    while not plane1.is_armable:
        print("Kalkışa Hazır Değiliz")
        print("Arm Durumu: {}".format(plane1.armed))

def plane_takeoff():

    plane1.mode = VehicleMode("TAKEOFF")
    time.sleep(1)
    print("Araç Modu: {}".format(plane1.mode))
    plane1.armed=True
    time.sleep(1)
    print("Plane Armed: {}".format(plane1.armed))
    print("Plane Kalkıyor")
    while(plane1.location.global_relative_frame.alt <=50):
        time.sleep(1) 
    print("Kalktı")
        
def plane_simplegoto(konum_x,konum_z,konum_y):

    plane1.mode=VehicleMode("GUIDED")
    try: 
        move_point=LocationGlobalRelative(konum_x,konum_z,konum_y)
        plane1.simple_goto(move_point)

        while not (konum_x-0.001<=plane1.location.global_relative_frame.lat <= konum_x+0.001 and konum_z-0.001<=plane1.location.global_relative_frame.lon<=konum_z+0.001):
            print("Konumda Gidiliyor...")
            time.sleep(2)
        print("Konuma Varıldı, Taktiksel Dönüş Yapılıyor :D")
        print("Araç Modu: {}".format(plane1.mode))

    except:
        print("Girilen Kordinatlarda Hata Var.")


def plane_send_global_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = plane1.message_factory.set_position_target_global_int_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, # lat_int - X Position in WGS84 frame in 1e7 * meters
        0, # lon_int - Y Position in WGS84 frame in 1e7 * meters
        0, # alt - Altitude in meters in AMSL altitude(not WGS84 if absolute or relative)
        # altitude above terrain if GLOBAL_TERRAIN_ALT_INT
        velocity_x, # X velocity in NED frame in m/s
        velocity_y, # Y velocity in NED frame in m/s
        velocity_z, # Z velocity in NED frame in m/s
        0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    # send command to vehicle on 1 Hz cycle
    for x in range(0,duration):
        plane1.send_mavlink(msg)
        time.sleep(1)

def plane_rtl():

    plane1.mode = VehicleMode("RTL")
    print("RTL Moduna Geçildi, Launch yerine dönülüyor")


plane_pre_arm_check()
plane_takeoff()
plane_simplegoto(-35.37141241,149.17475423,100)
plane_send_global_velocity(10,0,10,20)
plane_rtl()


"""
Python temelleri kısmının final kısmı
https://www.teknofest.org/upload/diger/ULUSLARARASI%20İHA%20YARIŞMASI%20KURALLAR%20KİTAPÇIĞI%20GÜNCEL.pdf linkteki döner kanat görev 1 ve görev 2(sayfa 53) yi similasyon ortamında gercekleştiriniz

*wp noktalarını kendiniz belirleyin (su alma ve su bırakma alanlarını bulmanıza gerek yok her nokta daha önceden belirlenmiş olsun ve tek tek o noktalar ile görevi simüle edin)
*su alma ve su bırakma kısmında 3 er saniye bekleyin 
*görev 1 ve görev 2 arasında yere inmeyip tek seferde bitirin. 
"""


# Görev 1: Dönmeli Hareketler

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

drone1 = connect("127.0.0.1:14550", wait_ready=True, timeout=30)

def pre_arm_check():
    while not drone1.is_armable:
        print("Kalkışa Hazır Değiliz.")
        print("Arm Durumu: {}".format(drone1.armed))

def takeoff(kac_metre):
    global baslangic_konumu
    drone1.mode = VehicleMode("GUIDED")
    time.sleep(1)
    print("Araç Modu: {}".format(drone1.mode))
    drone1.armed=True
    time.sleep(1)
    print("Drone Armed: {}".format(drone1.armed))
    print("Drone Yükseliyor")
    drone1.simple_takeoff(kac_metre)
    while(drone1.location.global_relative_frame.alt <=kac_metre*0.98):
        time.sleep(1) 

    print("Dron Yerel Yüksekliği: {}".format(drone1.location.global_relative_frame.alt))
    baslangic_konumu=drone1.location.global_relative_frame

def saga_git(saniye):
    
    donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat,drone1.location.global_relative_frame.lon+0.1,drone1.location.global_relative_frame.alt)
    drone1.simple_goto(donus)
    time.sleep(saniye)

def sola_git(saniye):
    
    donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat,drone1.location.global_relative_frame.lon-0.1,drone1.location.global_relative_frame.alt)
    drone1.simple_goto(donus)
    time.sleep(saniye)

def simple_olmayan_turnleft():
    
    for i in range(21):
        if(i<=10):
            donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat+i/10,drone1.location.global_relative_frame.lon+(10-i)/2,drone1.location.global_relative_frame.alt)
            drone1.simple_goto(donus)
            time.sleep(1)
        elif(i<=20):
            donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat+(20-i)/10,drone1.location.global_relative_frame.lon+(10-i)/2,drone1.location.global_relative_frame.alt)
            drone1.simple_goto(donus)
            time.sleep(1)

def simple_olmayan_turnright():
    
    for i in range(21):
        if(i<=10):
            donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat-i/10,drone1.location.global_relative_frame.lon-(10-i)/2,drone1.location.global_relative_frame.alt)
            drone1.simple_goto(donus)
            time.sleep(1)
        elif(i<=20):
            donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat-(20-i)/10,drone1.location.global_relative_frame.lon-(10-i)/2,drone1.location.global_relative_frame.alt)
            drone1.simple_goto(donus)
            time.sleep(1)

def direk_dansi():

    for i in range (5):
        if(i == 0 or i == 4):
            donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat,drone1.location.global_relative_frame.lon-1,drone1.location.global_relative_frame.alt)
            drone1.simple_goto(donus)
            time.sleep(5.5)
        elif(i == 1):
            donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat+1,drone1.location.global_relative_frame.lon,drone1.location.global_relative_frame.alt)
            drone1.simple_goto(donus)
            time.sleep(5.5)
        elif(i == 2):
            donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat,drone1.location.global_relative_frame.lon+1,drone1.location.global_relative_frame.alt)
            drone1.simple_goto(donus)
            time.sleep(5.5)
        elif(i == 3):
            donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat-1,drone1.location.global_relative_frame.lon,drone1.location.global_relative_frame.alt)
            drone1.simple_goto(donus)
            time.sleep(5.5)

def baslangica_don():
    drone1.simple_goto(baslangic_konumu)
    while not (baslangic_konumu.lon-0.000008 <=drone1.location.global_relative_frame.lon <= baslangic_konumu.lon+0.000008):
        time.sleep(1)

def yere_in():
    print("İniş Yapılıyor..")
    drone1.mode = VehicleMode("LAND")
    drone1.disarm()
    print("İniş Tamamlandı, Drone Arm Durumu: {}".format(drone1.armed))


pre_arm_check()
takeoff(100)
for i in range(2):
    print("{}. Dönüş".format(i+1))
    saga_git(8)
    simple_olmayan_turnleft()
    sola_git(4)
    direk_dansi()
    sola_git(3)
    simple_olmayan_turnright() 
    baslangica_don()

yere_in()



# Görev 2: Yangın Söndürme

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

drone1 = connect("127.0.0.1:14550", wait_ready=True, timeout=30)

def pre_arm_check():
    while not drone1.is_armable:
        print("Kalkışa Hazır Değiliz.")
        print("Arm Durumu: {}".format(drone1.armed))


def takeoff(kac_metre):
    global ilk_konum
    drone1.mode = VehicleMode("GUIDED")
    time.sleep(1)
    print("Araç Modu: {}".format(drone1.mode))
    drone1.armed=True
    time.sleep(1)
    print("Drone Armed: {}".format(drone1.armed))
    print("Drone Yükseliyor")
    drone1.simple_takeoff(kac_metre)
    drone1.wait_for_alt(kac_metre)
    print("Dron Yerel Yüksekliği: {}".format(drone1.location.global_relative_frame.alt))
    ilk_konum=drone1.location.global_relative_frame

def saga_ilerle(saniye):
    
    donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat,drone1.location.global_relative_frame.lon+0.1,drone1.location.global_relative_frame.alt)
    drone1.simple_goto(donus)
    time.sleep(saniye)
    

def sola_ilerle(saniye):
    
    donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat,drone1.location.global_relative_frame.lon-0.1,drone1.location.global_relative_frame.alt)
    drone1.simple_goto(donus)
    time.sleep(saniye)

def simple_olmayan_turnupway():
    
    for i in range(21):
        if(i<=10):
            donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat+i/10,drone1.location.global_relative_frame.lon+(10-i)/2,drone1.location.global_relative_frame.alt)
            drone1.simple_goto(donus)
            time.sleep(1)
        elif(i<=20):
            donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat+(20-i)/10,drone1.location.global_relative_frame.lon+(10-i)/2,drone1.location.global_relative_frame.alt)
            drone1.simple_goto(donus)
            time.sleep(1)

def simple_olmayan_turndownway():
    
    for i in range(21):
        if(i<=10):
            donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat-i/10,drone1.location.global_relative_frame.lon-(10-i)/2,drone1.location.global_relative_frame.alt)
            drone1.simple_goto(donus)
            time.sleep(1)
        elif(i<=20):
            donus =LocationGlobalRelative(drone1.location.global_relative_frame.lat-(20-i)/10,drone1.location.global_relative_frame.lon-(10-i)/2,drone1.location.global_relative_frame.alt)
            drone1.simple_goto(donus)
            time.sleep(1)

def su_almaya_git():
    
    drone1.simple_goto(LocationGlobalRelative(drone1.location.global_relative_frame.lat,drone1.location.global_relative_frame.lon-0.0005,drone1.location.global_relative_frame.alt))
    time.sleep(6)
    """
    kordinatlar= LocationGlobalRelative(konum_x,konum_z,drone1.location.global_relative_frame.alt)
    drone1.simple_goto(kordinatlar)
    while not (konum_x-0.01<=drone1.location.global_relative_frame.lat<=konum_x+0.01 and konum_z-0.01<=drone1.location.global_relative_frame.lon<=konum_z+0.01):
            print("Konuma Gidiliyor,  {}".format(drone1.location.global_relative_frame))
            time.sleep(1)
    print("Konuma Varıldı.")
    """

def su_al():
    
    time.sleep(5)
    print("Su Alındı.")

def su_bosaltmaya_git():
   
    drone1.simple_goto(LocationGlobalRelative(drone1.location.global_relative_frame.lat,drone1.location.global_relative_frame.lon-0.0006,drone1.location.global_relative_frame.alt))
    time.sleep(6)
    """
    kordinatlar= LocationGlobalRelative(konum_x,konum_z,drone1.location.global_relative_frame.alt)
    drone1.simple_goto(kordinatlar)
    while not (konum_x-0.01<=drone1.location.global_relative_frame.lat<=konum_x+0.01 and konum_z-0.01<=drone1.location.global_relative_frame.lon<=konum_z+0.01):
            print("Konuma Gidiliyor,  {}".format(drone1.location.global_relative_frame))
            time.sleep(1)
    print("Konuma Varıldı.")  
    """


def su_bosalt():
    
    time.sleep(5)
    print("Su Boşaltıldı.")


def kalkisa_don():
    drone1.simple_goto(ilk_konum)
    while not (ilk_konum.lon-0.000008 <=drone1.location.global_relative_frame.lon <= ilk_konum.lon+0.000008):
        time.sleep(1)

def inis_yap():
    print("İniş Yapılıyor..")
    drone1.mode = VehicleMode("LAND")
    drone1.disarm()
    print("İniş Tamamlandı, Drone Arm Durumu: {}".format(drone1.armed))


pre_arm_check()
takeoff(100)

saga_ilerle(6)
simple_olmayan_turnupway()
sola_ilerle(12)
simple_olmayan_turndownway() 
kalkisa_don()
print("Su Alma ve Su Bırakma Yerleri Tespit Edildi.")
saga_ilerle(6)
simple_olmayan_turnupway()
su_almaya_git()
su_al()
su_bosaltmaya_git()
su_bosalt()
sola_ilerle(3)
simple_olmayan_turndownway()
kalkisa_don()
inis_yap()

