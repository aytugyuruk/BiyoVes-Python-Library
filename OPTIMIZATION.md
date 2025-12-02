## 📦 Kurulum - Minimal vs Tam

### Minimal Kurulum (Önerilen - Daha Hafif)
```bash
pip install biyoves
```
Bu, sadece gerekli paketleri indirir:
- OpenCV (~100MB)
- NumPy (~60MB)
- MediaPipe (~100-150MB - sadece Face Detection/Mesh modelleri)
- ONNX Runtime (~50MB)

**Toplam boyut: ~320-360MB**

### Tam Kurulum (Tüm MediaPipe özellikleri)
```bash
pip install biyoves[full]
```
Bu, tüm MediaPipe özelliklerini indirir (örneğin pose detection, hand detection vb.).

---

## ⚡ Optimizasyon Detayları

BiyoVes, sadece aşağıdaki MediaPipe özelliklerini kullanır:

1. **Face Detection** - Yüz tespiti
2. **Face Mesh** - Yüz landmark'ları
3. **Selfie Segmentation** - Arka plan segmentasyonu

Diğer MediaPipe modelleri (el tespiti, poz tespiti vb.) **yüklenmez**.

### MediaPipe Model Boyutları
```
Face Detection:       ~912 KB
Face Landmark:        ~3.6 MB
Selfie Segmentation:  ~500 KB
```

---

## 🔍 Model Durumunu Kontrol Et

```python
from biyoves.mediapipe_config import print_model_info

# Gerekli modellerin kurulu olup olmadığını kontrol et
print_model_info()
```

**Çıktı örneği:**
```
=== BiyoVes MediaPipe Model Durumu ===

✓ face_detection: Yuz tespit modeli
✓ face_mesh: Yuz mesh modeli
✓ selfie_segmentation: Selfie segmentasyon modeli

========================================

✓ Tum gerekli modeller hazir!
```

---

## 🚀 Kullanım

### Yöntem 1: Sınıf Kullanımı (Önerilen)

```python
from biyoves import BiyoVes

# Fotoğraf yolunu belirt
img = BiyoVes("foto.jpg")

# Vesikalık fotoğraf oluştur (2li layout)
vesikalik = img.create_image("vesikalik", "2li", "sonuc_vesikalik.jpg")
```

### Yöntem 2: Fonksiyon Kullanımı

```python
from biyoves import create_image

# Tek satırda işlem
vesikalik = create_image("foto.jpg", "vesikalik", "2li", "sonuc.jpg")
```

---

## 📋 Desteklenen Fotoğraf Tipleri

- `"biyometrik"` - Standart biyometrik fotoğraf (50x60mm)
- `"vesikalik"` - Vesikalık fotoğraf (45x60mm)
- `"abd_vizesi"` - ABD vizesi için (50x50mm)
- `"schengen"` - Schengen vizesi için (35x45mm)

---

## 📊 Paket Karşılaştırması

| Paket | Boyut | Kullanım |
|-------|-------|----------|
| OpenCV | ~100MB | Görüntü işleme |
| NumPy | ~60MB | Sayısal işlemler |
| MediaPipe | ~100-150MB | Yüz tespiti, mesh, segmentasyon |
| ONNX Runtime | ~50MB | Arka plan silme modeli |
| **TOPLAM** | **~320-360MB** | |

---

## 🔧 Sorun Giderme

### MediaPipe Modellerini Yeniden Yükle

```bash
pip install --force-reinstall 'mediapipe>=0.10.0'
```

### Modeller Manuel Kontrol

```python
from biyoves.mediapipe_config import check_mediapipe_models

status = check_mediapipe_models()
print(status)
```

---

## 📝 Lisans

MIT License
