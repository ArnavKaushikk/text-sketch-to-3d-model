import os
import json
import time
import torch
from datetime import datetime
def save_metadata(session_path:str,input_type:str,input_data:str,multiview:bool,final_output:str,start_time:float,model_info:dict=None,views_generated:int=None)->None:
    """Saves detailed pipeline metadata into metadata.json.
    Args:
        session_path (str):Path to session folder
        input_type (str):'text' or 'sketch'
        input_data (str):Prompt or sketch path
        multiview (bool):Whether multiview was used
        final_output (str):Path to final STL
        start_time (float):Pipeline start time
        model_info (dict):Optional model names
        views_generated (int):Number of generated views"""
    gen_time=round(time.time()-start_time,2)
    metadata={"timestamp":datetime.now().isoformat(),
              "input_type":input_type,
              "input_data":input_data,
              "multiview_enabled":multiview,
              "views_generated":views_generated,
              "final_output":final_output,
              "gen_time_seconds":gen_time,
              "device":"cuda" if torch.cuda.is_available() else "cpu",
              "gpu_name":torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
              "models_used":model_info or {}}
    metadata_path=os.path.join(session_path,"metadata.json")
    with open(metadata_path,"w")as f:
        json.dump(metadata,f,indent=4)
    print(f"[INFO] Metadata saved at {metadata_path}")