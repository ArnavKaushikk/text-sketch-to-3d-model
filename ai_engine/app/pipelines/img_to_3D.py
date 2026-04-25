import sys
import os
import torch
from PIL import Image
TRIPOSR_PATH=os.path.abspath(os.path.join(os.path.dirname(__file__),"../TripoSR"))
sys.path.append(TRIPOSR_PATH)
from tsr.system import TSR
from..utils.config import DEVICE,IMAGE_SIZE
_model=None
def load_triposr():
    global _model
    if _model is None:
        _model=TSR.from_pretrained("stabilityai/TripoSR",config_name="config.yaml",weight_name="model.ckpt")
        _model=_model.to(DEVICE)
        _model.eval()
    return _model
def img_to_3D(img_input,session_path:str)->str:
    """Converts image(s) to 3D mesh using TripoSR."""
    os.makedirs(session_path,exist_ok=True)
    model=load_triposr()
    if isinstance(img_input,str):
        img_input=[img_input]
    imgs=[]
    for path in img_input:
        img=Image.open(path).convert("RGB")
        img=img.resize((IMAGE_SIZE,IMAGE_SIZE))
        imgs.append(img)
    with torch.no_grad():
        scene=model(imgs,device=DEVICE)
    mesh=model.extract_mesh(scene,has_vertex_color=True,resolution=64)[0]
    output_path=os.path.join(session_path,"mesh.obj")
    mesh.export(output_path)
    return output_path