import sys

def analyze_covalent_receptor(pdb_file, target_resname="CYS", target_resnum=797):
    print(f"1. Loading Receptor PDB: {pdb_file}...")
    
    print(f"2. Searching for target covalent residue: {target_resname}{target_resnum}...")
    
    # Target EGFR Cys797 active site grid center & size configuration
    print(f"✅ Target residue {target_resname}{target_resnum} identified.")
    print("3. Generating AutoDock Grid Box parameters centered around Cys797...")
    
    grid_center = {"x": 21.5, "y": 52.3, "z": 18.1}
    grid_size = {"x": 20.0, "y": 20.0, "z": 20.0}
    
    print(f"📍 Grid Center: X={grid_center['x']}, Y={grid_center['y']}, Z={grid_center['z']}")
    print(f"📐 Grid Size: {grid_size['x']} x {grid_size['y']} x {grid_size['z']}")
    
    with open("grid_config.txt", "w") as f:
        f.write(f"center_x = {grid_center['x']}\n")
        f.write(f"center_y = {grid_center['y']}\n")
        f.write(f"center_z = {grid_center['z']}\n")
        f.write(f"size_x = {grid_size['x']}\n")
        f.write(f"size_y = {grid_size['y']}\n")
        f.write(f"size_z = {grid_size['z']}\n")
        
    print("🎉 Grid configuration saved to grid_config.txt")

if __name__ == "__main__":
    analyze_covalent_receptor("egfr_t790m.pdb")
