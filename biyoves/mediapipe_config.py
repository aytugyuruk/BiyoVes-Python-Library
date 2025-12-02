"""
MediaPipe Model Manager
Sadece gerekli modelleri kontrol eder ve indirir.
Face Detection ve Face Mesh modelleri optimization icin.
"""

import os
from pathlib import Path


def get_required_models():
    """Biyoves icin gerekli olan modelleri listeler"""
    return {
        "face_detection": {
            "files": [
                "face_detection_short_range.tflite",
                "face_detection_full_range_sparse.tflite",
            ],
            "path": "modules/face_detection/",
            "description": "Yuz tespit modeli"
        },
        "face_mesh": {
            "files": [
                "face_landmark.tflite",
                "face_landmark_with_attention.tflite",
            ],
            "path": "modules/face_landmark/",
            "description": "Yuz mesh modeli"
        },
        "selfie_segmentation": {
            "files": [
                "selfie_segmentation.tflite",
                "selfie_segmentation_landscape.tflite",
            ],
            "path": "modules/selfie_segmentation/",
            "description": "Selfie segmentasyon modeli"
        }
    }


def check_mediapipe_models():
    """MediaPipe modellerinin kurulu olup olmadığını kontrol eder"""
    try:
        import mediapipe
        mediapipe_path = Path(mediapipe.__file__).parent
        
        models_status = {}
        for model_name, model_info in get_required_models().items():
            model_path = mediapipe_path / model_info["path"]
            
            if not model_path.exists():
                models_status[model_name] = {
                    "installed": False,
                    "path": str(model_path),
                    "description": model_info["description"]
                }
            else:
                # Model dosyalarini kontrol et
                missing_files = []
                for file in model_info["files"]:
                    if not (model_path / file).exists():
                        missing_files.append(file)
                
                models_status[model_name] = {
                    "installed": len(missing_files) == 0,
                    "missing_files": missing_files if missing_files else None,
                    "path": str(model_path),
                    "description": model_info["description"]
                }
        
        return models_status
    except ImportError:
        return {"error": "MediaPipe yuklenmemis"}


def print_model_info():
    """Model durumunu kullaniciya gosterir"""
    print("\n=== BiyoVes MediaPipe Model Durumu ===\n")
    
    status = check_mediapipe_models()
    
    if "error" in status:
        print(f"⚠️  {status['error']}")
        print("   Kurulum: pip install 'mediapipe>=0.10.0'")
        return
    
    all_installed = True
    for model_name, info in status.items():
        if info["installed"]:
            print(f"✓ {model_name}: {info['description']}")
        else:
            print(f"✗ {model_name}: {info['description']}")
            if info.get("missing_files"):
                for file in info["missing_files"]:
                    print(f"  - Eksik: {file}")
            all_installed = False
    
    print("\n" + "="*40 + "\n")
    
    if not all_installed:
        print("⚠️  Bazı modeller eksik!")
        print("   MediaPipe'i yeniden kurun: pip install --force-reinstall 'mediapipe>=0.10.0'")
    else:
        print("✓ Tum gerekli modeller hazir!")


if __name__ == "__main__":
    print_model_info()
