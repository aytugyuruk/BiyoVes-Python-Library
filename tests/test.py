
import os
import sys
import cv2

# Add src to path to ensure we can import the package
# We use insert(0) to prioritize local src over installed packages
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import biyoves

def main():
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, "image.png")
    output_path = os.path.join(base_dir, "test_result_4lu_biyometrik.jpg")
    
    # Check input
    if not os.path.exists(input_path):
        print(f"Hata: Örnek dosya bulunamadı: {input_path}")
        return

    print("BiyoVes Kütüphanesi Test Ediliyor...")

    try:
        # High-level API kullanımı (Corrector + Processor + Layout hepsini içerir)
        # Arkaplan temizleme, yön düzeltme, kırpma ve yerleştirme otomatik yapılır.
        result = biyoves.create_image(
            image_path=input_path,
            photo_type="biyometrik", # 50x60mm
            layout_type="4lu",       # 10x15cm kağıda 4'lü
            output_path=output_path,
            verbose=True
        )

        if result is not None:
            print(f"Başarılı! Sonuç kaydedildi: {output_path}")
        else:
            print("İşlem başarısız.")
        
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    main()
