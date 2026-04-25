import os
import torch
import diffusers as Zero123Pipeline
from PIL import Image
from..utils.config import DEVICE
_model=None
def load_zero123():
    global _model
    if _model is None:
        _model=Zero123Pipeline.from_pretrained("cvlab/zero123-xl-diffusers",torch_dtype=torch.float32)
        _model=_model.to(DEVICE).eval()
    return _model
def view_synthesis(concept_img_path:str,session_path:str)->list:
    if not os.path.exists(concept_img_path):
        raise FileNotFoundError(concept_img_path)
    multiview_dir=os.path.join(session_path,"multiview")
    os.makedirs(multiview_dir,exist_ok=True)
    pipe=load_zero123()
    img=Image.open(concept_img_path).convert("RGB")
    azimuths=[360*i/16 for i in range(8)]
    elevation=0
    paths=[]
    with torch.no_grad():
        for i,az in enumerate(azimuths):
            result=pipe(image=img,elevation=elevation,azimuth=az)
            view=result.images[0]
            path=os.path.join(multiview_dir,f"view_{i:02d}.png")
            view.save(path)
            paths.append(path)
    return paths