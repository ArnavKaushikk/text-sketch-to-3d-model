import trimesh
import trimesh.smoothing as smoothing
import numpy as np
from pathlib import Path
import os

def clean_and_export(mesh_path: str, session_path: str) -> str:
    """
    Enhanced cleaning and export pipeline using Taubin smoothing 
    to preserve volume and high-res subdivision for smooth curves.
    """
    print(f"--- Loading Mesh: {mesh_path} ---")
    
    # force='mesh' prevents it from loading as a Scene, which causes errors
    mesh = trimesh.load(mesh_path, force='mesh')
    
    # 1. Basic Cleaning & Merging
    # Merging vertices is key for complex geometries—it welds facets into a single skin
    mesh.remove_infinite_values()
    mesh.remove_unreferenced_vertices()
    mesh.merge_vertices()
    
    # 2. Fill gaps (Crucial for watertightness in 3D printing)
    if not mesh.is_watertight:
        print("Closing gaps in mesh...")
        mesh.fill_holes()

    # 3. HIGH-RES UP-SAMPLING (The 'Anti-Blocky' Fix)
    # Subdividing turns large flat triangles into a fine grid for better smoothing
    print("Boosting mesh resolution for smooth curves...")
    mesh = mesh.subdivide()
    mesh = mesh.subdivide()

    # 4. TAUBIN SMOOTHING (The 'Hard Surface' Specialist)
    # Taubin preserves volume (hood, trunk, roof) better than Laplacian
    print("Applying Taubin Feature-Preserving Smoothing...")
    smoothing.filter_taubin(mesh, iterations=40)

    # 5. SMART OPTIMIZATION (Decimation)
    # Reduce face count back down while keeping high density on edges
    target_faces = 45000 
    current_faces = len(mesh.faces)
    
    if current_faces > target_faces:
        reduction = 1.0 - (target_faces / current_faces)
        print(f"Optimizing: Reducing by {reduction*100:.1f}%...")
        mesh = mesh.simplify_quadric_decimation(reduction)

    # 6. Final Polish & Normals
    mesh.fix_normals()
    _ = mesh.face_normals # Force calculation for shading
    
    mesh.apply_translation(-mesh.centroid)
    
    # Scale to 100mm (10cm) for standard viewing/printing
    scale = mesh.extents.max()
    if scale > 0:
        mesh.apply_scale(100.0 / scale)

    # 7. Export
    os.makedirs(session_path, exist_ok=True)
    output_path = Path(session_path) / "refined_car_model.stl"
    
    # Exporting as binary STL for faster loading in viewers
    mesh.export(str(output_path), file_type='stl')
    
    print(f"--- SUCCESS ---")
    print(f"Final Vertices: {len(mesh.vertices)} | Final Faces: {len(mesh.faces)}")
    return str(output_path)