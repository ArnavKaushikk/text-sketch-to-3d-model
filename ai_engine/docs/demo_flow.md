# Demo Flow

This document demonstrates how the AI → 3D pipeline runs.

## Step 1 — Input

User provides:

• text prompt
• sketch
• image

Example:

"a futuristic drone"

---

## Step 2 — Concept Generation

txt2img.py or sketch2img.py generates a concept image.

Output:
concept.png

---

## Step 3 — Multiview Generation

view_synthesis.py generates multiple views.

Outputs:

view_1.png
view_2.png
view_3.png
view_4.png

---

## Step 4 — 3D Reconstruction

img_to_3D.py reconstructs a mesh.

Output:

mesh.obj

---

## Step 5 — Mesh Cleaning

mesh_utils.py exports final model.

Final output:

model.stl