import json
import random

def predict_affinity(smiles):
    """Simulate GNN binding affinity prediction (pChEMBL value)."""
    base_score = 7.5
    if "C(=O)N" in smiles:
        base_score += 1.2
    if "c1ccccc1" in smiles:
        base_score += 0.5
    if "O" in smiles:
        base_score += 0.2
    return round(base_score + random.uniform(-0.2, 0.3), 2)

def predict_admet_risk(smiles):
    """Simulate ADMET toxicity model outputs (hERG & DILI Risk between 0.0 and 1.0)."""
    aromatic_rings = smiles.count("c1") + smiles.count("C1")
    # Decreased toxicity when solubilizing or non-aromatic groups are introduced
    polar_atoms = smiles.count("O") + smiles.count("N")
    
    herg_risk = max(0.1, 0.3 + aromatic_rings * 0.12 - polar_atoms * 0.05 + random.uniform(-0.03, 0.03))
    dili_risk = max(0.1, 0.2 + aromatic_rings * 0.14 - polar_atoms * 0.04 + random.uniform(-0.03, 0.03))
    return round(herg_risk, 3), round(dili_risk, 3)

def mutate_smiles(smiles):
    """Simulate molecular structure mutation to optimize toxicity profile."""
    mutations = [
        lambda s: s.replace("c1ccccc1", "C1CCNCC1"),  # Replace benzene with piperidine (reduces hERG risk)
        lambda s: s + "O",                             # Add hydroxyl/ether group to improve solubility
        lambda s: s.replace("C1", "CC1") if "C1" in s else s + "C",
        lambda s: s.replace("c2nc3c(n2)cccc3", "c2nc3c(n2)cc(O)cc3") if "c2nc3" in s else s
    ]
    mutator = random.choice(mutations)
    return mutator(smiles)

def calculate_multi_objective_fitness(smiles):
    """Compute overall fitness using affinity minus ADMET toxicity penalties."""
    affinity = predict_affinity(smiles)
    herg_risk, dili_risk = predict_admet_risk(smiles)
    
    herg_penalty = max(0.0, (herg_risk - 0.5) * 3.0)
    dili_penalty = max(0.0, (dili_risk - 0.5) * 3.0)
    
    total_fitness = affinity - herg_penalty - dili_penalty
    return {
        "fitness": round(total_fitness, 2),
        "affinity_pchembl": affinity,
        "herg_risk": herg_risk,
        "dili_risk": dili_risk,
        "penalties": round(herg_penalty + dili_penalty, 2),
        "admet_passed": herg_risk < 0.5 and dili_risk < 0.5
    }

def run_evolutionary_optimization(generations=5, population_size=4):
    print("==================================================")
    print("🧬 STARTING MULTI-GENERATION GA EVOLUTION LOOP")
    print("==================================================\n")
    
    # Initial seed population
    population = [
        {"id": "GEN0-01", "smiles": "CC(=O)Nc1ccc(cc1)c2nc3c(n2)cccc3"},
        {"id": "GEN0-02", "smiles": "C=CC(=O)Nc1cc(Nc2nccc(n2)c3cn(C)c4ccccc34)c(cc1OC)N(C)CCN(C)C"}
    ]
    
    passed_candidates = []

    for gen in range(1, generations + 1):
        print(f"--- GENERATION {gen} ---")
        next_population = []
        
        for idx, parent in enumerate(population):
            # Generate mutant derivative
            mutated_smiles = mutate_smiles(parent["smiles"])
            cand_id = f"GEN{gen}-0{idx+1}"
            
            res = calculate_multi_objective_fitness(mutated_smiles)
            res["id"] = cand_id
            res["smiles"] = mutated_smiles
            
            verdict = "[PASSED]" if res["admet_passed"] else "[REJECTED - TOXIC]"
            print(f"[{cand_id}] Affinity: {res['affinity_pchembl']} | hERG: {res['herg_risk']} | DILI: {res['dili_risk']} | Fitness: {res['fitness']} -> {verdict}")
            
            if res["admet_passed"]:
                passed_candidates.append(res)
                
            next_population.append(res)
            
        population = next_population
        print()

    # Save evolution results
    output_file = "multiobj_evolved_candidates.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"passed_candidates": passed_candidates}, f, indent=2)
        
    print(f"🎉 EVOLUTION COMPLETE. Found {len(passed_candidates)} safe candidates.")
    print(f"💾 Evolved Candidates saved to '{output_file}'")
    print("==================================================")

if __name__ == "__main__":
    run_evolutionary_optimization()
