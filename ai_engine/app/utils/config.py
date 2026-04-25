import torch
import os
PROJECT_ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))
ASSETS_DIR=os.path.join(PROJECT_ROOT,"assets")
SAMPLES_DIR=os.path.join(ASSETS_DIR,"samples")
OUTPUTS_DIR=os.path.join(ASSETS_DIR,"outputs")
LOGS_DIR=os.path.join(ASSETS_DIR,"logs")
CACHE_DIR=os.path.join(ASSETS_DIR,"cache")
DEVICE="cuda" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE=torch.float32
SD_MODEL_ID="runwayml/stable-diffusion-v1-5"
IMAGE_SIZE=512
BASE_OUTPUT_DIR="app/assets/outputs"
CONCEPT_IMAGE_DIR=os.path.join(BASE_OUTPUT_DIR,"concept_images")
MULTIVIEW_DIR=os.path.join(BASE_OUTPUT_DIR,"multiview")
MESH_DIR=os.path.join(BASE_OUTPUT_DIR,"meshes")
STL_DIR=os.path.join(BASE_OUTPUT_DIR,"stl")