# precision-landing-drone

DroneKit + OpenCV tabanlı hassas iniş (precision landing) projesinin sürüm arşividir.  
Bu README, özellikle **v0.4.4** sürümünün amacını, akışını ve dosya sorumluluklarını GitHub projesi standardında açıklar.

---

## Projenin Amacı

Bu projenin ana hedefi, bir hava aracının iniş sırasında görsel bir marker (işaretleyici) tespiti yaparak:

1. hedefi görüntüden bulması,
2. hedefe göre yatay eksende (X-Y) hizalanması,
3. kontrollü şekilde alçalması,
4. güvenli iniş/disarm tamamlamasıdır.

Sistem, klasik “tek komutla in” yaklaşımı yerine görüntü geri beslemesiyle son yaklaşmayı iyileştirir.

---

## Hangi Sürüm Anlatılıyor?

Analiz edilen çalışma ağacı:

- `Hassas İniş Kodlar/ver_0.4.4/ver_0.4.3`

> Not: klasör adı `ver_0.4.3` olsa da bunun üst paket sürümü `ver_0.4.4` olarak tutulmuştur.

---

## Sistem Ne Yapar? (Uçtan Uca Süreç)

Program akışı `Main.py` ile başlar ve aşağıdaki sırayı izler:

1. **Init aşaması**  
   Araç bağlantısı, lidar ve kamera kontrol edilir.

2. **Mission Stage 1**  
   Uçuş modunda `LAND` tetiklenmesi beklenir, görüldüğünde kontrol `GUIDED` moda alınır.

3. **Mission Stage 2**  
   Araç, hassas iniş okumalarının başlayacağı irtifaya (`precisionReadingAltitude`) indirilir.  
   İsteğe bağlı olarak önce GPS iniş noktasına (`landingPoint`) gider.

4. **Mission Stage 3**  
   Kamera görüntüsünden marker tespiti yapılır, merkez hatası hesaplanır, araç X-Y ekseninde marker üstüne taşınır, ardından alçalma hızı dinamik ayarlanır.

5. **Final / Emniyet**  
   İniş irtifası eşiği geçildiğinde disarm/land yapılır.  
   Hata durumunda emniyet prosedürü (`Emergency.SafeLand`) devreye girer.

---

## Mimari Özeti

Proje modülerdir ve sorumluluklar ayrılmıştır:

- **Orkestrasyon**: `Main.py`, `MissionStage_*`
- **Başlatma/bağlantı**: `init.py`, `Parameters.py`
- **Görüntü**: `Camera.py`, `Detect.py`
- **Kontrol**: `MotionControl.py`
- **Emniyet**: `Emergency.py`
- **Yardımcı/deneme**: `Logging.py`, `Test_Class.py`

---

## Dosya Dosya Ne İşe Yarıyor?

### `Main.py`
- Programın ana giriş noktasıdır.
- `init()`, `MissionStage_1()`, `MissionStage_2()`, `MissionStage_3()` sıralı çalıştırılır.
- Stage’lerden biri hata verirse kamera kapatılır, emniyet inişi çağrılır, süreç sonlandırılır.

### `Parameters.py`
- Tüm sistem ayarlarının tek merkezidir.
- Bağlantı bilgileri (`vehicleConnectionIP`, baudrate, timeout), kamera seçimi (`vehicleCameraType`), görev modu (`missionMode`, `landMode`) ve kontrol kazançları burada tutulur.
- İniş davranışını belirleyen ana parametreler:
  - `precisionReadingAltitude`
  - `landingAltitude`
  - `detectionTimeout`
  - `xAxisProportionalGain`, `yAxisProportionalGain`
  - `velocitySaturation`

### `init.py`
- Araç bağlantısını (DroneKit) açar.
- Lidar ve kamera erişimini doğrular.
- Gerekli durumları global parametre alanına (`p.vehicle`, `p.capture`) yazar.

### `MissionStage_1.py`
- `LAND` tetiğini bekler.
- Tetik geldiğinde aracı `GUIDED` moduna alır.

### `MissionStage_2.py`
- `landMode` değerine göre davranır:
  - `0`: doğrudan hassas iniş okuma irtifasına iner.
  - `1`: GPS iniş noktasına gider, sonra irtifa düşürür.
  - `2`: tanımlı değil (hata üretir).

### `MissionStage_3.py`
- Görüntüden noktaları çıkarır (`Detect.Color`), marker üretir (`Detect.Marker`).
- Marker merkezini referans merkeze göre hizalar (`TrackCoordinates`).
- Hata küçüldükçe alçalma hızını düzenler (`DecreaseAltitude`).
- Marker kaybolursa timeout yönetimi yapar.
- İniş eşiğinde disarm/land ile süreci kapatır.

### `Camera.py`
- Kamera kaynağını `INTERNAL / SIM / TEST` modlarına göre yönetir.
- Frame alma (`GetNextFrame`) ve kaynak kapama (`CloseCam`) fonksiyonlarını sağlar.

### `Detect.py`
- Görüntüyü threshold ile ikili forma çevirir.
- Kontur merkezlerini çıkarır.
- Marker çıkarımı için `BASIC` ve `T` şekil mantıkları içerir.

### `MotionControl.py`
- MAVLink hız komutları üretir (`SetVelocity`).
- Marker merkez hatasını hız komutuna çevirir (`TrackCoordinates`).
- Alçalma hızını X-Y hata büyüklüğüne göre uyarlamaya çalışır (`DecreaseAltitude`).
- İniş/disarm kontrol yardımcıları içerir.

### `Emergency.py`
- Emniyet durumda aracı `RTL` moduna geçirir.
- Disarm olana kadar durumu izler ve kapanışı tamamlar.

### `Logging.py`
- Zaman damgalı CSV üretimi yapan prototip bir log denemesidir.
- Çekirdek görev akışına doğrudan entegre değildir.

### `Mission.py`
- Boş dosyadır, aktif görev akışında kullanılmaz.

### `Test_Class.py`
- Basit bir görüntü test dosyasıdır (`Detect.Color` çağrısı).

---

## v0.4.4 Teknik Durum (Önemli)

Bu sürümde `MotionControl.py` içinde kritik bir sentaks problemi vardır:

```python
0,rra 0)
```

Bu satır nedeniyle v0.4.4 kaynak ağacı mevcut haliyle doğrudan çalıştırılabilir değildir.

---

## Kullanılan Teknolojiler

- Python
- DroneKit
- pymavlink
- OpenCV (`cv2`)
- NumPy

---

## Kısa Sonuç

v0.4.4, proje mimarisini netleştiren ve logging tarafını genişletmeye başlayan bir sürümdür;  
ancak mevcut kaynakta bulunan sentaks hatası nedeniyle koşum öncesi düzeltme gerektirir.
