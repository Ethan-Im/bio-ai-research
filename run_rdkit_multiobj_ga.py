import json
import random
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, QED

def compute_rdkit_properties(smiles):
    """Parse SMILES string and calculate real molecular descriptors using RDKit."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    qed_score = QED.qed(mol)
    h_donors = Lipinski.NumHDonors(mol)
    h_acceptors = Lipinski.NumHAcceptors(mol)
    aromatic_rings = Lipinski.NumAromaticRings(mol)
    
    # Proxy hERG / DILI risk based on lipophilicity (LogP) and aromatic ring count
    herg_risk = min(1.0, max(0.1, 0.15 * aromatic_rings + 0.1 * max(0.0, logp - 3.0)))
    dili_risk = min(1.0, max(0.1, 0.12 * aromatic_rings + 0.05 * (mw / 200.0)))
    
    return {
        "mw": round(mw, 2),
        "logp": round(logp, 2),
        "qed": round(qed_score, 3),
        "h_donors": h_donors,
        "h_acceptors": h_acceptors,
        "aromatic_rings": aromatic_rings,
        "herg_risk": round(herg_risk, 3),
        "dili_risk": round(dili_risk, 3)
    }

def calculate_fitness(smiles):
    """Compute multi-objective fitness combining QED, Lipinski rules, and ADMET penalties."""
    props = compute_rdkit_properties(smiles)
    if props is None:
        return {"fitness": -999.0, "valid": False}
    
    # Scale QED score (0.0 to 1.0) to base fitness score
    base_fitness = props["qed"] * 10.0
    
    # Lipinski Rule of 5 penalty calculation
    lipinski_violations = 0
    if props["mw"] > 500:
        lipinski_violations += 1
    if props["logp"] > 5.0:
        lipinski_violations += 1
    if props["h_donors"] > 5:
        lipinski_violations += 1
    if props["h_acceptors"] > 10:
        lipinski_violations += 1
        
    lipinski_penalty = lipinski_violations * 1.5
    
    # Toxicity Penalties
    herg_penalty = max(0.0, (props["herg_risk"] - 0.5) * 4.0)
    dili_penalty = max(0.0, (props["dili_risk"] - 0.5) * 4.0)
    
    total_fitness = base_fitness - lipinski_penalty - herg_penalty - dili_penalty
    
    props["fitness"] = round(total_fitness, 2)
    props["lipinski_violations"] = lipinski_violations
    props["total_penalty"] = round(lipinski_penalty + herg_penalty + dili_penalty, 2)
    props["admet_passed"] = (props["herg_risk"] < 0.5 and 
                             props["dili_risk"] < 0.5 and 
                             lipinski_violations <= 1)
    props["valid"] = True
    return props

def mutate_smiles_rdkit(smiles):
    """Perform structure modifications maintaining valid SMILES representation."""
    mutations = [
        lambda s: s.replace("c1ccccc1", "C1CCNCC1"),  # Replace benzene ring with piperidine
        lambda s: s + "O",                             # Add hydroxyl/ether oxygen
        lambda s: s.replace("C1", "CC1") if "C1" in s else s + "C",
        lambda s: s.replace("N", "NC") if "N" in s else s
    ]
    for _ in range(5):
        mutated = random.choice(mutations)(smiles)
        if Chem.MolFromSmiles(mutated) is not None:
            return mutated
    return smiles

def run_rdkit_ga_optimization(generations=3):
    print("==================================================")
    print("🧬 STARTING RDKIT-INTEGRATED MULTI-OBJECTIVE GA")
    print("==================================================\n")
    
    population = [
        "CC(=O)Nc1ccc(cc1)c2nc3c(n2)cccc3",
        "Cc1cc(Nc2nccc(n2)c3c[nH]c4ccccc34)ccc1C(=O)N"
    ]
    
    all_results = []
    
    for gen in range(1, generations + 1):
        print(f"--- GENERATION {gen} ---")
        next_gen = []
        
        for idx, parent in enumerate(population):
            cand_smiles = mutate_smiles_rdkit(parent)
            res = calculate_fitness(cand_smiles)
            cand_id = f"RDKIT-GEN{gen}-0{idx+1}"
            
            if res["valid"]:
                res["id"] = cand_id
                res["smiles"] = cand_smiles
                verdict = "[PASSED]" if res["admet_passed"] else "[REJECTED]"
                
                print(f"[{cand_id}] SMILES: {cand_smiles[:30]}...")
                print(f"  MW: {res['mw']} | LogP: {res['logp']} | QED: {res['qed']} | Violations: {res['lipinski_violations']}")
                print(f"  hERG Risk: {res['herg_risk']} | DILI Risk: {res['dili_risk']} | Fitness: {res['fitness']} -> {verdict}\n")
                
                all_results.append(res)
                next_gen.append(cand_smiles)
                
        population = next_gen

    output_file = "rdkit_multiobj_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"candidates": all_results}, f, indent=2)
        
    print(f"💾 Real RDKit optimization complete. Results saved to '{output_file}'")
    print("==================================================")

if __name__ == "__main__":
    run_rdkit_ga_optimization()
