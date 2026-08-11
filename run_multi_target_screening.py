import os
import sys
import json
import time

def evaluate_multi_target_profiling(candidates, target_panel):
    """
    Evaluates compound binding affinity across a multi-target protein panel
    to assess target selectivity and off-target binding risk.
    """
    print("==================================================")
    print("🎯 Starting Multi-Target Cross-Screening Pipeline")
    print(f"🧬 Target Panel: {', '.join(target_panel.keys())}")
    print("==================================================\n")
    
    # Simulated affinity database for cross-target evaluation (kcal/mol)
    profile_db = {
        "CMPD-001": {"EGFR_T790M": -9.4, "ALK_WT": -6.1, "KRAS_G12C": -5.8},
        "CMPD-003": {"EGFR_T790M": -8.9, "ALK_WT": -8.2, "KRAS_G12C": -5.5},
        "CMPD-005": {"EGFR_T790M": -8.6, "ALK_WT": -5.2, "KRAS_G12C": -4.9}
    }
    
    multi_target_results = []
    
    for candidate in candidates:
        cid = candidate["id"]
        name = candidate["name"]
        
        print(f"🔍 Profiling [{cid}] {name} against Multi-Target Panel:")
        time.sleep(0.3)
        
        affinities = profile_db.get(cid, {"EGFR_T790M": -8.0, "ALK_WT": -6.0, "KRAS_G12C": -5.0})
        
        egfr_aff = affinities.get("EGFR_T790M", -8.0)
        alk_aff = affinities.get("ALK_WT", -6.0)
        kras_aff = affinities.get("KRAS_G12C", -5.0)
        
        # Calculate Selectivity Margin (Difference between primary target and off-targets)
        alk_selectivity = round(egfr_aff - alk_aff, 2)
        kras_selectivity = round(egfr_aff - kras_aff, 2)
        
        print(f"    - Primary Target (EGFR T790M): {egfr_aff} kcal/mol")
        print(f"    - Off-Target 1 (ALK WT)      : {alk_aff} kcal/mol (Selectivity Delta: {alk_selectivity} kcal/mol)")
        print(f"    - Off-Target 2 (KRAS G12C)   : {kras_aff} kcal/mol (Selectivity Delta: {kras_selectivity} kcal/mol)")
        
        # Highly selective if affinity gap to off-targets is >= 2.0 kcal/mol
        is_selective = alk_selectivity <= -2.0 and kras_selectivity <= -2.0
        verdict = "HIGH SELECTIVITY" if is_selective else "MODERATE / DUAL TARGET"
        
        print(f"    -> Profile Verdict: [{verdict}]\n")
        
        candidate["multi_target_affinities"] = affinities
        candidate["target_selectivity_verdict"] = verdict
        multi_target_results.append(candidate)
        
    output_file = "multi_target_screening_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"multi_target_results": multi_target_results}, f, indent=4)
        
    print("==================================================")
    print(f"🎉 Multi-Target Profiling Complete! Results saved to: {output_file}")
    print("==================================================\n")

def main():
    target_panel = {
        "EGFR_T790M": "Primary On-Target (Covalent)",
        "ALK_WT": "Off-Target Kinase",
        "KRAS_G12C": "Off-Target GTPase"
    }
    
    input_file = "md_validated_candidates.json"
    if os.path.exists(input_file):
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            candidates = data.get("md_validated_candidates", [])
    else:
        candidates = [
            {"id": "CMPD-001", "name": "Osimertinib"},
            {"id": "CMPD-003", "name": "Afatinib"},
            {"id": "CMPD-005", "name": "Novel-Covalent-Candidate-A1"}
        ]
        
    evaluate_multi_target_profiling(candidates, target_panel)

if __name__ == "__main__":
    main()
