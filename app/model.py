"""Однократная загрузка предобученной модели SCHP без обрезки классов."""
import torch
from clothing_segmentation.predict import ClothingSegmentationPredictor

# модель грузится при импорте, чтобы не держать её в каждом воркере
_predictor = None

def get_predictor():
    global _predictor
    if _predictor is None:
        _predictor = ClothingSegmentationPredictor(device="cuda" if torch.cuda.is_available() else "cpu")
    return _predictor
