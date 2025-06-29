import tempfile
from typing import Tuple
from PIL import Image
import numpy as np
from app.model import get_predictor
from app.utils import split_masks


def segment_bytes(image_bytes: bytes) -> Tuple[str, dict]:
    """Принимает bytes → возвращает путь к общей PNG + dict отдельных слоёв."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name

    predictor = get_predictor()
    mask = predictor.predict_single(tmp_path)  # ndarray H×W, classes 0‑19
    # сохраняем full‑map для наглядности
    full_path = tmp_path.replace(".png", "_mask.png")
    Image.fromarray(mask.astype(np.uint8)).save(full_path)

    parts = split_masks(mask)  # dict label→PIL
    for label, pil_img in parts.items():
        save_path = full_path.replace("_mask.png", f"_{label}.png")
        pil_img.save(save_path)
        parts[label] = save_path

    return full_path, parts
