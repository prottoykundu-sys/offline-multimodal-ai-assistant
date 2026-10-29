from PIL import Image, ImageEnhance, ImageFilter
import io
import os

def preprocess_image(path: str):
    img = Image.open(path)
    img = img.convert("RGB")
    img = img.filter(ImageFilter.SHARPEN)
    return img
