from PIL import Image
import os
def load_and_resize(img_path:str,size:int):
    img=Image.open(img_path).convert("RGB")
    img=img.resize((size,size))
    return img
def save_img(img,path:str):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    img.save(path)
def normalize_img_tensor(imgt):
    """Normalize tensor to 0–1 range"""
    return imgt/255