import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.append(project_root)


from app.pipelines.txt2img import txt2img

import time
import argparse
import sys
import shutil
import os
from app.pipelines.txt2img import txt2img
from app.pipelines.sketch2img import sketch2img
from app.pipelines.view_synthesis import view_synthesis
from app.pipelines.img_to_3D import img_to_3D
from app.utils.mesh_utils import clean_and_export
from app.utils.session_utils import create_session_folder
from app.utils.metadata_utils import save_metadata

def run_pipeline(input_type:str, data:str, use_multiview:bool=True, custom_output:str=None) -> str:
    """Orchestrates full 2D → 3D generation pipeline."""
    start = time.time()
    if not data:
        raise ValueError("No input data provided")
    
    try:
        # 1. Setup Session
        session_id, session_path = create_session_folder()
        print(f"[INFO] Created session {session_id}")

        # 2. Concept Generation
        if input_type == "text":
            concept_path = txt2img(data, session_path)
        elif input_type == "sketch":
            concept_path = sketch2img(data, session_path)
        else:
            raise ValueError("input_type must be either 'text' or 'sketch'")
        
        print("[INFO] Concept image generated")

        
        if use_multiview:
            multiview_paths = view_synthesis(concept_path, session_path)
            mesh_input = multiview_paths
            views_generated = len(multiview_paths)
            print(f"[INFO] Generated {views_generated} views using Zero123++")
        else:
            mesh_input = concept_path
            views_generated = 1

        # 4. 3D Reconstruction (TripoSR)
        mesh_path = img_to_3D(mesh_input, session_path)
        print("[INFO] 3D mesh generated")

        # 5. Refinement and Export
        final_stl_path = clean_and_export(mesh_path, session_path)
        
        
        if custom_output:
            
            os.makedirs(os.path.dirname(custom_output), exist_ok=True)
            shutil.copy(final_stl_path, custom_output)
            final_stl_path = custom_output

        print("[INFO] STL export completed")

        # 6. Metadata Update
        save_metadata(session_path=session_path,
                      input_type=input_type,
                      input_data=data,
                      multiview=use_multiview,
                      final_output=final_stl_path,
                      start_time=start,
                      views_generated=views_generated,
                      model_info={"text_model":"StableDiffusion3",
                                  "view_model":"Zero123++",
                                  "mesh_model":"TripoSR"})

        total = round(time.time() - start, 2)
        print(f"[INFO] Pipeline finished successfully in {total}s")
        return final_stl_path

    except Exception as e:
        print(f"[ERROR] Pipeline failed: {e}")
        # Return 1 to tell Node.js that the process failed
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SketchTo3D CLI")
    
    # Node.js will pass these arguments
    parser.add_argument("--input", type=str, required=True, help="Path to input file")
    parser.add_argument("--output", type=str, required=True, help="Path for final STL")
    parser.add_argument("--type", type=str, default="sketch", help="text or sketch")
    
    # NEW: Handle the multiview flag as a string to avoid boolean conversion bugs
    parser.add_argument("--multiview", type=str, default="False", help="True or False")
    
    args = parser.parse_args()
    
    # Logic to convert the string "True"/"False" to a real Python Boolean
    use_mv = True if args.multiview.lower() == "true" else False
    
    print(f"[DEBUG] Multiview enabled: {use_mv}")

    # Trigger the function
    run_pipeline(
        input_type=args.type, 
        data=args.input, 
        custom_output=args.output,
        use_multiview=use_mv  # Now correctly passing False
    )