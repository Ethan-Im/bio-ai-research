import json
import random

def predict_affinity(smiles):
    """Simulate GNN binding affinity prediction (pChEMBL value)."""
    base_score = 7.5
    # Increase affinity score based on functional groups or scaffold patterns
    if "C(=O)N" in smiles:
        base_score += 1.2
    if "c1ccccc1" in smiles:
        base_score += 0.5
    return round(base_score + random.uniform(-0.3, 0.4), 2)

def predict_admet_risk(smiles):
    """Simulate ADMET toxicity model outputs (hERG & DILI Risk between 0.0 and 1.0)."""
    # Excessive aromatic rings correlate with higher cardiac/hepatic toxicity risk
    aromatic_rings = smiles.count("c1") + smiles.count("C1")
    herg_risk = min(0.9, 0.3 + aromatic_rings * 0.15 + random.uniform(-0.05, 0.05))
    dili_risk = min(0.9, 0.2 + aromatic_rings * 0.18 + random.uniform(-0.05, 0.05))
    return round(herg_risk, 3), round(dili_risk, 3)

def calculate_multi_objective_fitness(smiles):
    """
    Multi-Objective Fitness Function:
    Fitness = Predicted Affinity - (hERG Penalty + DILI Penalty)
    """
    affinity = predict_affinity(smiles)
    herg_risk, dili_risk = predict_admet_risk(smiles)
    
    # Apply heavy penalty if toxicity risk exceeds acceptable safety threshold (> 0.5)
    herg_penalty = max(0.0, (herg_risk - 0.5) * 3.0)
    dili_penalty = max(0.0, (dili_risk - 0.5) * 3.0)
    
    total_fitness = affinity - herg_penalty - dili_penalty
    return {
        "fitness": round(total_fitness, 2),
        "affinity_pchembl": affinity,
        "herg_risk": herg_risk,
        "dili_risk": dili_risk,
        "penalties": round(herg_penalty + dili_penalty, 2)
    }

def run_multiobj_ga():
    print("==================================================")
    print("🧬 STARTING MULTI-OBJECTIVE GA LEAD OPTIMIZATION")
    print("==================================================\n")
    
    # Initial population of seed compounds
    seed_compounds = [
        {"id": "SEED-01", "smiles": "CC(=O)Nc1ccc(cc1)c2nc3c(n2)cccc3"},
        {"id": "SEED-02", "smiles": "C=CC(=O)Nc1cc(Nc2nccc(n2)c3cn(C)c4ccccc34)c(cc1OC)N(C)CCN(C)C"},
        {"id": "SEED-03", "smiles": "Cc1cc(Nc2nccc(n2)c3c[nH]c4ccccc34)ccc1C(=O)N"}
    ]
    
    results = []
    
    for seed in seed_compounds:
        res = calculate_multi_objective_fitness(seed["smiles"])
        res["id"] = seed["id"]
        res["smiles"] = seed["smiles"]
        
        # Verify ADMET safety criteria (both risks must be below 0.5)
        res["admet_passed"] = res["herg_risk"] < 0.5 and res["dili_risk"] < 0.5
        results.append(res)
        
        print(f"📌 Compound [{res['id']}]")
        print(f"  - Affinity (pChEMBL) : {res['affinity_pchembl']}")
        print(f"  - hERG Risk           : {res['herg_risk']} {'✅' if res['herg_risk'] < 0.5 else '❌'}")
        print(f"  - DILI Risk           : {res['dili_risk']} {'✅' if res['dili_risk'] < 0.5 else '❌'}")
        print(f"  - Total Penalty       : -{res['penalties']}")
        print(f"  - Final Fitness       : {res['fitness']}")
        print(f"  - ADMET Safety Verdict: {'[PASSED]' if res['admet_passed'] else '[REJECTED - TOXIC]'}\n")

    # Save output dataset
    output_file = "multiobj_optimization_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"candidates": results}, f, indent=2)
        
    print(f"💾 Multi-Objective Optimization Results saved to '{output_file}'")
    print("==================================================")

if __name__ == "__main__":
    run_multiobj_ga()
