import cv2
from ultralytics import YOLO
from utils.alarm import SecurityAlarm
import config

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

# Alarm sayacını oluşturalım:
alarm_counter = 0

while cap.isOpened():
    success, frame = cap.read()

    if not success:
        print("Kameradan Görüntü Alınamadı...")
        break

    # Görüntüyü yatayda aynala (Daha doğal bir web kamerası görüntüsü için)
    frame = cv2.flip(frame, 1)

    # YOLO ile tahmin yap (Direkt frame'i gönderiyoruz)
    result = model(frame, verbose=False)

    # Her kare için tehdit kontrol bayraklarını sıfırlayalım
    threat_found = False        # Tehdit Bulundu mu?
    is_critical = False         # Tehdit Kritik mi?

    # Her kareyi döndürüp arama yapacağız ve tespit edeceğiz:
    for box in result[0].boxes:
        class_id = int(box.cls[0])              # Sınıf ID'sini al (örn: 0, 1, 2...)
        class_name = model.names[class_id]      # ID'yi isme çevir (örn: 'person')
        conf = float(box.conf[0])               # O anki kutunun güveni

         # Tespit edilen isim aradığımız şeyse:
        if class_name == "Handgun" or class_name == "Knife" or class_name == "Rifle" or class_name == "Sword":
            if conf >= config.CRITICAL_CONF:
                threat_found = True
                is_critical = True
                break  # En yüksek seviye zaten bulundu, diğer kutuları boşuna dönme
            elif conf >= config.MIN_CONF:
                threat_found = True

        
    # --- ALARM KOŞULU ---
    if is_critical:
        alarm_counter = config.ALARM_THRESHOLD
        alarm.trigger()

    elif threat_found:
        alarm_counter += 1
        print(f"Tehdit şüphesi... Sayaç: {alarm_counter}/{config.ALARM_THRESHOLD}")

        if alarm_counter >= config.ALARM_THRESHOLD:
            alarm.trigger()

    else:
        ''' 3. Tehdit yok: Sayacı yavaşça sıfıra doğru düşür (Decay)
         Direkt 0 yaparsan model tek kare kaçırınca alarm anında susar, o yüzden 1 azaltırız:'''
        if alarm_counter > 0:
            alarm_counter -= 1
        
        if alarm_counter == 0:
            alarm.stop()
        
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