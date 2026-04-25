import os
from diffusers import StableDiffusion3Pipeline
from..utils.config import SD_MODEL_ID,TORCH_DTYPE,IMAGE_SIZE
_sd3_pipe=None
def load_sd3():
    global _sd3_pipe
    if _sd3_pipe is None:
        _sd3_pipe=StableDiffusion3Pipeline.from_pretrained(SD_MODEL_ID,torch_dtype=TORCH_DTYPE)
        _sd3_pipe.enable_model_cpu_offload()
        _sd3_pipe.enable_attention_slicing()
        _sd3_pipe.enable_vae_slicing()
    return _sd3_pipe
def txt2img(prompt:str,session_path:str)->str:
    os.makedirs(session_path,exist_ok=True)
    pipe=load_sd3()
    full_prompt=(f"A centered studio render of {prompt},""single object,white background,""no shadow,highly detailed,3D model style")
    neg_prompt=("multiple objects,cluttered background,""text,watermark,shadow,blur")
    img=pipe(full_prompt,negative_prompt=neg_prompt,height=IMAGE_SIZE,width=IMAGE_SIZE,guidance_scale=7.5,num_inference_steps=30).images[0]
    output_path=os.path.join(session_path,"concept.png")
    img.save(output_path)
    return output_path