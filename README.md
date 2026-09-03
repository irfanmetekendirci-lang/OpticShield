# OpticShield 🛡️

> **Durum:** 🟡 Aktif Geliştirme / Konsept Kanıtlama (PoC)
> OpticShield, gerçek zamanlı tehdit tespiti ve çevre güvenliği senaryoları için tasarlanmış, aktif olarak geliştirilen bir bilgisayarla görme projesidir. Sistem dönem dönem yeni modüller ve optimizasyonlarla güncellenmektedir.

---

## 📌 Proje Genel Bakışı

OpticShield, uç cihazlarla uyumlu derin öğrenme mimarilerini kullanarak gerçek zamanlı otomatik tehdit tespitini hedefler. Temel amaç; nesne algılama çıktısını gecikmesiz uyarı sistemleriyle (çevre gözetleme, otomatik alarm ve keşif sistemleri) birleştirmektir.

Şu an bir masaüstü prototipi olarak çalışan sistem, ilerleyen aşamalarda hava gözetleme (İHA/Dron) ve otonom güvenlik hatlarına taşınacak şekilde mimarilendirilmiştir.

---

## 🎯 Mevcut Yetenekler ve Mantık

* 🔴 **Hedef Sınıflar:** Eğitilmiş özel model üzerinden gerçek zamanlı tespit:
* `Handgun` (Tabanca)
* `Knife` (Bıçak)
* `Rifle` (Tüfek)
* `Sword` (Kılıç/Uzun Kesici Alet)


* ⚡ **Çift Eşikli Tetikleme Mekanizması:**
* `CRITICAL_CONF`: Yüksek güvenilirlikli ani tehditlerde sayacı beklemeden anında alarm tetikleme.
* `MIN_CONF`: Şüpheli durumları kare bazlı doğrulamaya alan taban güven skoru.


* ⏳ **Zaman Tabanlı Doğrulama ve Sayaç (Decay Counter):**
* Tek karelik anlık yanlış tespitleri (flickering/titreme) önleyen kare sayacı.
* Tehdit kaybolduğunda sesin kesik kesik çalmasını engelleyen kademeli sayaç düşüşü (decay).


* 🧩 **Modüler Mimari:**
* Kamera ve tespit döngüsü (`main.py`), bağımsız ses motoru (`utils/alarm.py`) ve dinamik eşik parametreleri (`config.py`) birbirinden tamamen ayrılmıştır.



---

## 🗂️ Proje Mimarisi

```text
OpticShield/
├── alarm/              # Alarm ses dosyaları (.wav)
├── models/             # Eğitilmiş YOLO ağırlıkları (best.pt)
├── utils/
│   ├── __init__.py
│   └── alarm.py        # Ses motoru ve durum yöneticisi
├── config.py           # Güven eşikleri ve sayaç parametreleri
├── data.yaml           # Veri seti sınıf tanımları
├── main.py             # Kamera döngüsü, çıkarım ve karar mekanizması
└── README.md

```

---

## 🚀 Geliştirme Yol Haritası

Bu proje periyodik olarak güncellenmeye ve genişletilmeye devam edecektir:

* [x] 🟢 Modüler temel mimari ve Pygame tabanlı ses motoru entegrasyonu.
* [x] 🟢 Çift eşikli güven filtresi ve sönümlemeli (decay) sayaç algoritması.
* [ ] 🟡 Ekran üzerine görsel durum paneli (HUD / Telemetri arayüzü).
* [ ] ⚪ Bağlamsal tespit (`Silahlı İnsan` / `Silahsız İnsan` ayrımı).
* [ ] ⚪ Hava gözetleme desteği (İHA/Dron görüntüleri için SAHI dilimleme entegrasyonu).
* [ ] ⚪ Olay kayıt mekanizması (Zaman damgalı log ve şüpheli karelerin diske kaydedilmesi).
* [ ] ⚪ Uç cihaz optimizasyonu (TensorRT / ONNX çıkarımları).

---

## 🛠️ Kullanılan Teknolojiler

* 🐍 **Programlama Dili:** Python 3.12+
* 👁️ **Derin Öğrenme & Bilgisayarla Görme:** Ultralytics YOLO, OpenCV (`cv2`)
* 🔊 **Ses & Donanım Denetimi:** Pygame (Mixer modülü)
* 📁 **Dosya & Dizin Yönetimi:** Python Standard Library (`pathlib`, `os`)

---

*Not: Bu depo aktif bir mühendislik çalışmasıdır; yeni modeller eğitildikçe ve sistem genişletildikçe düzenli aralıklarla güncellenecektir.*