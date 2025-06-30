"""
Загрузка предобученной модели SCHP из /opt/schp  (клон уже есть в Dockerfile).
"""
import torch
import os
from torchvision import transforms
from PIL import Image
import numpy as np

# path до скриптов репозитория
SCHP_ROOT = "/opt/schp"

import sys
sys.path.append(os.path.join(SCHP_ROOT, "models"))
sys.path.append(os.path.join(SCHP_ROOT, "utils"))

from model.resnet101 import Resnet101
from utils.transforms import get_affine_transform, affine_transform


# ------------------ загрузка сети ------------------
_device = "cuda" if torch.cuda.is_available() else "cpu"
_net = Resnet101(n_classes=20)
state_dict = torch.hub.load_state_dict_from_url(
    "https://github.com/GoGoDuck912/Self-Correction-Human-Parsing/releases/download/v1.0/schp_resnet101.pth",
    map_location=_device,
)
_net.load_state_dict(state_dict, strict=False)
_net.to(_device).eval()
# ---------------------------------------------------


def _preprocess(pil: Image.Image):
    img = np.array(pil)[:, :, ::-1]  # RGB→BGR
    height, width = img.shape[:2]
    # аффинное преобразование так же, как в оригинальном скрипте evaluate.py
    center, scale = np.array([width / 2, height / 2]), max(height, width) * 1.0
    trans = get_affine_transform(center, scale, 0, (512, 512))
    input_img = cv2.warpAffine(img, trans, (512, 512), flags=cv2.INTER_LINEAR)
    input_img = transforms.ToTensor()(input_img).unsqueeze(0)
    return input_img.to(_device), trans, (height, width)


def predict_mask(pil_img: Image.Image) -> np.ndarray:
    """Возвращает маску размера исходного изображения, значения 0-19."""
    inp, trans_inv, orig_hw = _preprocess(pil_img)
    with torch.no_grad():
        out = _net(inp)["out"]
        parsing = out.argmax(1).squeeze(0).cpu().numpy().astype(np.uint8)
    # обратное affine → исходный масштаб
    parsing = cv2.warpAffine(
        parsing,
        trans_inv,
        (orig_hw[1], orig_hw[0]),
        flags=cv2.INTER_NEAREST,
        borderValue=0,
    )
    return parsing
