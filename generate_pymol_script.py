import os
import sys
import json

def create_pymol_visualization_script(target_pdb, ligand_pdb, output_pml="visualize_docking.pml"):
    """
    Generates an automated PyMOL script (.pml) to visualize
    the protein-ligand complex and Cys797 covalent binding site.
    """
    pml_content = f"""# ==================================================
# Automated PyMOL Rendering Script
# Target: EGFR T790M | Key Residue: Cys797
# ==================================================

# 1. Environment Setup
bg_color white
set ray_shadows, 0
set orthonav, 1

# 2. Load Structures
load {target_pdb}, protein_target
load {ligand_pdb}, ligand_candidate

# 3. Protein Styling
hide everything, protein_target
show cartoon, protein_target
color gray80, protein_target

# 4. Highlight Key Binding Residue Cys797
select cys797, protein_target and resn CYS and resi 797
show sticks, cys797
color yellow, cys797

# 5. Ligand Styling
show sticks, ligand_candidate
color cyan, ligand_candidate

# 6. Interaction & Distance Measurement
distance cys_bond, cys797 and name SG, ligand_candidate and name C*, 2.5
color red, cys_bond
set dash_width, 2.0
set dash_gap, 0.15

# 7. View Orientation and Ray Trace Output
orient
zoom cys797, 8
ray 1200, 900
png egfr_cys797_binding_rendered.png, dpi=300
print "Rendering complete: saved to egfr_cys797_binding_rendered.png"
"""
    with open(output_pml, "w", encoding="utf-8") as f:
        f.write(pml_content)
    print(f"📄 Generated PyMOL automation script: {output_pml}")

def main():
    print("==================================================")
    print("🎨 Generating 3D Structural Visualization Script")
    print("==================================================")
    
    target_pdb = "egfr_t790m.pdb"
    ligand_pdb = "egfr_ai_docked_pose.pdbqt"
    
    create_pymol_visualization_script(target_pdb, ligand_pdb)
    print("==================================================")
    print("✅ PyMOL automation script creation completed.")
    print("📌 To render images in PyMOL, run: pymol -c visualize_docking.pml")
    print("==================================================\n")

if __name__ == "__main__":
    main()
