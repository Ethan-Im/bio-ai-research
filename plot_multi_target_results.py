import os
import json
import matplotlib.pyplot as plt
import numpy as np

def generate_selectivity_heatmap():
    input_file = "multi_target_screening_results.json"
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = data.get("multi_target_results", [])
    
    compounds = [f"{c['id']}\n({c['name']})" for c in results]
    targets = ["EGFR_T790M\n(On-Target)", "ALK_WT\n(Off-Target)", "KRAS_G12C\n(Off-Target)"]
    
    matrix = []
    for c in results:
        affs = c.get("multi_target_affinities", {})
        matrix.append([
            affs.get("EGFR_T790M", 0.0),
            affs.get("ALK_WT", 0.0),
            affs.get("KRAS_G12C", 0.0)
        ])
        
    matrix = np.array(matrix)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    cax = ax.matshow(matrix, cmap="YlOrRd_r")
    
    fig.colorbar(cax, label="Binding Affinity (kcal/mol)")
    
    ax.set_xticks(range(len(targets)))
    ax.set_yticks(range(len(compounds)))
    ax.set_xticklabels(targets)
    ax.set_yticklabels(compounds)
    
    for i in range(len(compounds)):
        for j in range(len(targets)):
            ax.text(j, i, f"{matrix[i, j]:.1f}", ha='center', va='center', color='black', fontweight='bold')
            
    plt.title("Multi-Target Binding Affinity & Selectivity Heatmap", pad=20, fontsize=12, fontweight='bold')
    plt.tight_layout()
    
    output_img = "multi_target_selectivity_heatmap.png"
    plt.savefig(output_img, dpi=300)
    print(f"📊 Multi-target heatmap plot saved to: {output_img}")

if __name__ == "__main__":
    generate_selectivity_heatmap()
