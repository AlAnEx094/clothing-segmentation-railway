"""Вспомогательные функции: преобразование маски в PNG, раздельные слои."""
from typing import Dict
import cv2
import numpy as np
from PIL import Image

# линейка классов (LIP‑ладдер)
LIP_CLASSES = {
    5: "upper",   # upper‑clothes / coat
    6: "lower",   # pants / skirt
    7: "full",    # dress
}

PALETTE = [
    0,  0,  0,      # 0 — фон (чёрный)
    128, 0, 0,      # 1 — skin / голова (неважно)
    # … полный список можно оставить, пока не критично
]


def mask_to_color(mask: np.ndarray) -> Image.Image:
    """Псевдо‑цветная карта для отладки."""
    h, w = mask.shape
    color = np.zeros((h, w, 3), dtype=np.uint8)
    for cls, name in LIP_CLASSES.items():
        color[mask == cls] = (0, 255, 0) if name == "upper" else (255, 0, 0) if name == "lower" else (0, 0, 255)
    return Image.fromarray(color)


def split_masks(mask: np.ndarray) -> Dict[str, Image.Image]:
    """Разбиваем общую маску на 3 PNG с альфой."""
    out = {}
    for cls, label in LIP_CLASSES.items():
        alpha = (mask == cls).astype(np.uint8) * 255
        if alpha.sum() == 0:
            continue
        rgba = np.zeros((*mask.shape, 4), dtype=np.uint8)
        rgba[..., 3] = alpha
        out[label] = Image.fromarray(rgba)
    return out
