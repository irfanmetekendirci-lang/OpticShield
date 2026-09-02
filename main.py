import cv2
from ultralytics import YOLO
from utils.alarm import SecurityAlarm

# 1. Modeli yükle
model = YOLO("models/best.pt")

# Alarm nesnesini başlat (Ayrı dosyadan geliyor)    
alarm = SecurityAlarm("alarm/alarm.wav")

# 2. Kamerayı başlat ve çözünürlüğü ayarla (HD)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 3. OpenCV Pencere ayarları
pencere_adi = 'YOLO Canli Tespit'
cv2.namedWindow(pencere_adi, cv2.WINDOW_NORMAL)
cv2.resizeWindow(pencere_adi, 1280, 720)

while cap.isOpened():
    success, frame = cap.read()

    if not success:
        print("Kameradan Görüntü Alınamadı...")
        break

    # Görüntüyü yatayda aynala (Daha doğal bir web kamerası görüntüsü için)
    frame = cv2.flip(frame, 1)

    # YOLO ile tahmin yap (Direkt frame'i gönderiyoruz)
    result = model(frame, verbose=False)

    # Başlangıçta o kare için tespiti False yapıyoruz
    intruder_detected = False

    # Tespit edilen tüm kareleri döndürüp tehlike varsa alarm çaldıracağız:
    for box in result[0].boxes:
        class_id = int(box.cls[0])              # Sınıf ID'sini al (örn: 0, 1, 2...)
        class_name = model.names[class_id]      # ID'yi isme çevir (örn: 'person')

         # Tespit edilen isim aradığımız şeyse:
        if class_name == "Handgun":
            intruder_detected = True
            break    # Bir tane bulmamız alarm için yeterli, döngüden çıkabiliriz

        elif class_name == "Knife":
            intruder_detected = True
            break

        elif class_name == "Rifle":
            intruder_detected = True
            break 

        elif class_name == "Sword":
            intruder_detected = True
            break 
        
    # --- ALARM KOŞULU ---
    if intruder_detected:
        alarm.trigger()  # Ayrı dosyadaki alarmı çal
    else:
        alarm.stop()     # Kimse yoksa alarmı sustur   
        
    # Kutuları çizilmiş görseli al
    annotated_frame = result[0].plot()

    # Ekranda göster
    cv2.imshow(pencere_adi, annotated_frame)

    # 'q' tuşuna basılırsa çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları kapat
cap.release()
cv2.destroyAllWindows()