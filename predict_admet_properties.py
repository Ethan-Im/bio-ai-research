import os
import sys
import json

def evaluate_lipinski_rule_of_five(mw, logp, hbd, hba):
    """
    Evaluates Lipinski's Rule of Five for drug-likeness.
    - MW <= 500 Da
    - LogP <= 5.0
    - H-Bond Donors (HBD) <= 5
    - H-Bond Acceptors (HBA) <= 10
    """
    violations = 0
    if mw > 500:
        violations += 1
    if logp > 5.0:
        violations += 1
    if hbd > 5:
        violations += 1
    if hba > 10:
        violations += 1
    return violations

def run_admet_profiling(screening_file):
    """
    Simulates AI-based ADMET prediction and Lipinski rule screening
    on virtual screening top hits.
    """
    print("==================================================")
    print("🧪 Starting AI-driven ADMET & Drug-Likeness Profiling")
    print("==================================================")
    
    if not os.path.exists(screening_file):
        print(f"❌ Error: Screening file '{screening_file}' not found.")
        sys.exit(1)
        
    with open(screening_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    top_hits = data.get("top_hits", [])
    print(f"📋 Loaded {len(top_hits)} Top Candidates from Virtual Screening.\n")
    
    # Pre-defined ADMET property dictionary for demonstration candidates
    admet_database = {
        "CMPD-001": {
            "molecular_weight": 469.52,
            "logP": 3.8,
            "hbd": 2,
            "hba": 6,
            "herg_toxicity_risk": "Low",
            "bbb_permeability": "Moderate",
            "cyp3a4_inhibition": "Low"
        },
        "CMPD-003": {
            "molecular_weight": 485.94,
            "logP": 4.2,
            "hbd": 2,
            "hba": 7,
            "herg_toxicity_risk": "Low",
            "bbb_permeability": "High",
            "cyp3a4_inhibition": "Moderate"
        },
        "CMPD-005": {
            "molecular_weight": 354.36,
            "logP": 2.9,
            "hbd": 1,
            "hba": 5,
            "herg_toxicity_risk": "Low",
            "bbb_permeability": "Moderate",
            "cyp3a4_inhibition": "Low"
        }
    }
    
    passed_drug_candidates = []
    
    for candidate in top_hits:
        cid = candidate["id"]
        name = candidate["name"]
        props = admet_database.get(cid, {
            "molecular_weight": 450.0, "logP": 3.5, "hbd": 2, "hba": 6,
            "herg_toxicity_risk": "Low", "bbb_permeability": "Moderate", "cyp3a4_inhibition": "Low"
        })
        
        mw = props["molecular_weight"]
        logp = props["logP"]
        hbd = props["hbd"]
        hba = props["hba"]
        
        violations = evaluate_lipinski_rule_of_five(mw, logp, hbd, hba)
        herg_risk = props["herg_toxicity_risk"]
        
        print(f"🔍 Analyzing [{cid}] {name}:")
        print(f"    - MW: {mw} Da | LogP: {logp} | HBD: {hbd} | HBA: {hba}")
        print(f"    - Lipinski Violations: {violations}")
        print(f"    - hERG Cardiac Toxicity Risk: {herg_risk}")
        
        # Filtering criteria: 0 or 1 Lipinski violation and Low hERG toxicity risk
        if violations <= 1 and herg_risk == "Low":
            print("    ✅ PASSED ADMET & Drug-Likeness Filters\n")
            candidate["admet_properties"] = props
            candidate["lipinski_violations"] = violations
            passed_drug_candidates.append(candidate)
        else:
            print("    ❌ REJECTED due to ADMET/Lipinski failure\n")
            
    # Save ADMET profiler report
    output_file = "admet_filtered_candidates.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"approved_candidates": passed_drug_candidates}, f, indent=4)
        
    print("==================================================")
    print(f"🎉 ADMET Profiling Complete! Approved Candidates: {len(passed_drug_candidates)}/{len(top_hits)}")
    print(f"💾 Report saved to: {output_file}")
    print("==================================================\n")

if __name__ == "__main__":
    run_admet_profiling("virtual_screening_results.json")
