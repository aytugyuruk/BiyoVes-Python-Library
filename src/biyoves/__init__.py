import cv2
from pathlib import Path

from .remove_bg import BackgroundRemover
from .corrector import FaceOrientationCorrector
from .processor import BiometricIDGenerator
from .layout import PrintLayoutGenerator
import logging

logger = logging.getLogger(__name__)




class BiyoVes:
    
    def __init__(self, image_path=None, verbose=True):

        self.verbose = verbose
        self.image_path = image_path
        
        # Modelleri yükle
        # Model dosyasının yolunu bul (paket içinde)
        package_dir = Path(__file__).parent
        model_path = package_dir / "models" / "modnet.onnx"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model dosyası bulunamadı: {model_path}")
        
        self.bg_remover = BackgroundRemover(str(model_path))
        self.corrector = FaceOrientationCorrector(verbose=self.verbose)
        self.processor = BiometricIDGenerator()
        self.layout_gen = PrintLayoutGenerator()
    
    def create_image(self, photo_type="biyometrik", layout_type="2li", output_path=None):
    
        if self.image_path is None:
            raise ValueError("Fotoğraf yolu belirtilmedi. BiyoVes('foto.jpg') şeklinde başlatın.")
        
        # 1. Resmi Oku
        original_img = cv2.imread(self.image_path)
        if original_img is None:
            raise FileNotFoundError(f"Giriş resmi bulunamadı: {self.image_path}")
        
        # 2. Yüz Yönü Düzeltme (Oryantasyon)
        # Arkaplan temizlemeden önce yapmak daha sağlıklı olabilir (yüz bulucu için)
        # Ayrıca processor.py içinde arkaplan temizleme artık mevcut (kırpılmış resim üzerinde çalışıyor = daha hızlı)
        corrected_img = self.corrector.correct_image(original_img)
        if corrected_img is None:
            # Yüz bulunamazsa orjinali ile devam etmeyi deneyebiliriz veya hata verebiliriz.
            logger.warning("Oryantasyon düzeltme sırasında yüz bulunamadı, orjinal resim kullanılıyor.")
            corrected_img = original_img
        
        # 3. Biyometrik İşleme (Crop & Resize & Background Removal)
        # Processor artık arkaplanı kendisi temizliyor.
        processed_img = self.processor.process_photo(corrected_img, photo_type=photo_type)
        if processed_img is None:
            raise RuntimeError("Yüz bulunamadı veya işlenemedi.")
        
        # 4. Baskı Şablonu (Layout)
        final_layout = self.layout_gen.generate_layout(processed_img, layout_type=layout_type)
        
        if final_layout is None:
            raise RuntimeError("Layout oluşturulamadı.")
        
        # 6. Kaydetme (eğer output_path belirtilmişse)
        if output_path:
            # Dosya uzantısına göre kalite parametreleri - %100 kalite
            output_lower = output_path.lower()
            if output_lower.endswith('.jpg') or output_lower.endswith('.jpeg'):
                # JPEG için maksimum kalite (100 = kayıpsız)
                cv2.imwrite(output_path, final_layout, [cv2.IMWRITE_JPEG_QUALITY, 100])
            elif output_lower.endswith('.png'):
                # PNG için kayıpsız (compression 0 = en yüksek kalite)
                cv2.imwrite(output_path, final_layout, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            else:
                # Diğer formatlar için varsayılan
                cv2.imwrite(output_path, final_layout)
            
            if self.verbose:
                logger.info(f"İşlem tamamlandı: {output_path}")
        
        return final_layout
    
    def set_image(self, image_path):
        """Fotoğraf yolunu değiştir."""
        self.image_path = image_path


# Kolay kullanım için fonksiyon API'si
def create_image(image_path, photo_type="biyometrik", layout_type="2li", output_path=None, verbose=True):
    biyoves = BiyoVes(image_path, verbose=verbose)
    return biyoves.create_image(photo_type, layout_type, output_path)


__version__ = "1.0.0"
__all__ = ["BiyoVes", "create_image"]

