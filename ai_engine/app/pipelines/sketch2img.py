import os
import torch
import numpy as np
import cv2
from PIL import Image
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, DPMSolverMultistepScheduler
from ..utils.config import SD_MODEL_ID, TORCH_DTYPE, IMAGE_SIZE, DEVICE

_cnet_pipe = None

def load_cnet():
    global _cnet_pipe
    if _cnet_pipe is None:  
        controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-scribble", torch_dtype=TORCH_DTYPE)
        _cnet_pipe = StableDiffusionControlNetPipeline.from_pretrained(SD_MODEL_ID, controlnet=controlnet, torch_dtype=TORCH_DTYPE)
        _cnet_pipe.scheduler = DPMSolverMultistepScheduler.from_config(_cnet_pipe.scheduler.config)
        _cnet_pipe.enable_attention_slicing()
        _cnet_pipe.to(DEVICE) 
    return _cnet_pipe

def sketch2img(sketch_path: str, session_path: str) -> str:
    os.makedirs(session_path, exist_ok=True)
    pipe = load_cnet()

    sketch = Image.open(sketch_path).convert("RGB")
    sketch = sketch.resize((IMAGE_SIZE, IMAGE_SIZE))

    image_np = np.array(sketch)
    canny_edges = cv2.Canny(image_np, 100, 200)
    canny_edges = np.stack([canny_edges] * 3, axis=-1)
    canny_image = Image.fromarray(canny_edges)
    
    prompt = (
        "full view of a single object, (isolated on pure white background:1.5), "
        "orthographic front view, professional 3D game asset, high-resolution texture, "
        "flat lighting, zero shadows, sharp geometry, high contrast edges, "
        "masterpiece, unreal engine 5 render, neutral lighting"
    )
    neg_prompt = (
        "floor, ground, surface, shadow, reflection, table, platform, pedestal, "
        "depth of field, blurry, vignette, dark background, multiple views, "
        "perspective distortion, volumetric lighting"
    )

    print(f"Generating Technical Concept for 3D Reconstruction...")
    
    
    output_image = pipe(
        prompt=prompt,
        negative_prompt=neg_prompt,
        image=canny_image,
        num_inference_steps=30, 
        guidance_scale=9.0,
        controlnet_conditioning_scale=0.7 
    ).images[0]

    output_path = os.path.join(session_path, "concept.png")
    output_image.save(output_path)
    return output_path