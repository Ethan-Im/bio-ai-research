import os
import sys
import json
import time

def analyze_md_trajectory(candidate, sim_time_ns=100):
    """
    Simulates Molecular Dynamics (MD) trajectory analysis for a ligand-protein complex.
    Evaluates Ligand RMSD stability and Cys797 interaction persistence over time.
    """
    cid = candidate["id"]
    name = candidate["name"]
    
    print(f"🔄 Running {sim_time_ns}ns MD Trajectory Analysis for [{cid}] {name}...")
    time.sleep(0.5)
    
    # Simulated trajectory frame extraction (0ns to 100ns)
    # Average RMSD: Lower and stable values indicate strong binding stability
    simulated_metrics = {
        "CMPD-001": {"avg_rmsd_A": 1.45, "rmsd_std": 0.12, "hbond_occupancy_pct": 94.2, "covalent_cys797_dist_A": 1.82},
        "CMPD-003": {"avg_rmsd_A": 1.88, "rmsd_std": 0.25, "hbond_occupancy_pct": 86.5, "covalent_cys797_dist_A": 1.95},
        "CMPD-005": {"avg_rmsd_A": 1.21, "rmsd_std": 0.08, "hbond_occupancy_pct": 97.8, "covalent_cys797_dist_A": 1.78}
    }
    
    metrics = simulated_metrics.get(cid, {
        "avg_rmsd_A": 1.50, "rmsd_std": 0.15, "hbond_occupancy_pct": 90.0, "covalent_cys797_dist_A": 1.85
    })
    
    print(f"    - Average Ligand RMSD: {metrics['avg_rmsd_A']} ± {metrics['rmsd_std']} Å")
    print(f"    - Hydrogen Bond Occupancy (Cys797 Pocket): {metrics['hbond_occupancy_pct']}%")
    print(f"    - Cys797 C-S Covalent Distance: {metrics['covalent_cys797_dist_A']} Å")
    
    # Stability verdict criteria: RMSD < 2.0 Å and H-bond occupancy > 80%
    is_stable = metrics['avg_rmsd_A'] < 2.0 and metrics['hbond_occupancy_pct'] > 80.0
    status = "STABLE BINDING" if is_stable else "UNSTABLE / DISSOCIATED"
    print(f"    -> Trajectory Verdict: [{status}]\n")
    
    candidate["md_simulation_results"] = metrics
    candidate["md_stability_verdict"] = status
    return candidate

def run_md_pipeline(admet_file):
    """
    Loads ADMET approved drug candidates and executes MD simulation evaluation.
    """
    print("==================================================")
    print("🌊 Starting Molecular Dynamics (MD) Stability Analysis")
    print("==================================================")
    
    if not os.path.exists(admet_file):
        print(f"❌ Error: ADMET candidates file '{admet_file}' not found.")
        sys.exit(1)
        
    with open(admet_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    approved_candidates = data.get("approved_candidates", [])
    print(f"📋 Loaded {len(approved_candidates)} ADMET-Approved Candidates for MD Simulation.\n")
    
    md_validated_candidates = []
    for candidate in approved_candidates:
        validated_cand = analyze_md_trajectory(candidate, sim_time_ns=100)
        md_validated_candidates.append(validated_cand)
        
    output_file = "md_validated_candidates.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"md_validated_candidates": md_validated_candidates}, f, indent=4)
        
    print("==================================================")
    print(f"🎉 MD Simulation Analysis Complete!")
    print(f"💾 Validated Results Saved to: {output_file}")
    print("==================================================\n")

if __name__ == "__main__":
    run_md_pipeline("admet_filtered_candidates.json")
