# 🧬 Bio-AI Covalent Drug Discovery & Optimization Pipeline

An end-to-end AI-driven drug discovery workflow targeting EGFR T790M (Cys797), integrating molecular docking benchmarking, high-throughput virtual screening, ADMET profiling, molecular dynamics stability testing, automated 3D visualization, multi-target selectivity profiling, and AI de novo lead optimization.

---

## 📌 Pipeline Architecture & Modules (7 Stages)

1. `compare_docking_results.py`: Compares physics-based (AutoDock Vina) vs AI generative (DiffDock) docking performance.
2. `run_virtual_screening.py`: High-throughput screening across candidate compound libraries to select top hits.
3. `predict_admet_properties.py`: Evaluates drug-likeness (Lipinski's Rule of 5) and hERG cardiac toxicity risk.
4. `run_md_simulation_analysis.py`: Analyzes 100ns Molecular Dynamics trajectories for RMSD stability and Cys797 interaction persistence.
5. `generate_pymol_script.py`: Automatically generates PyMOL `.pml` scripts for high-resolution 3D pose rendering.
6. `run_multi_target_screening.py` & `plot_multi_target_results.py`: Evaluates off-target binding affinity (ALK/KRAS) and generates a multi-target selectivity heatmap.
7. `run_molecule_optimization.py`: Generates optimized de novo lead analogs (v2 generation) using AI-driven R-group modification.

---

## 📊 Summary Benchmark & Multi-Stage Results

| Pipeline Stage | Primary Output / Metric | Status |
|---|---|---|
| **1. Docking Benchmark** | ~30.1x Speedup with AI (1.5s vs 45.2s), RMSD 1.2 Å | ✅ Passed |
| **2. Virtual Screening** | Top Hits Selected (Osimertinib, Afatinib, Novel-A1) | ✅ Passed |
| **3. ADMET Profiling** | 0 Lipinski Violations, Low hERG Cardiac Risk | ✅ Passed |
| **4. MD Simulation** | Stable Trajectory (Avg RMSD 1.21~1.45 Å, >94% H-Bond) | ✅ Passed |
| **5. 3D Visualization** | `visualize_docking.pml` PyMOL Script Generated | ✅ Passed |
| **6. Multi-Target Profiling** | High Selectivity Delta (>3.3 kcal/mol gap vs ALK/KRAS) | ✅ Passed |
| **7. Lead Optimization** | `CMPD-005-v2A` Generated (Affinity: -9.2 kcal/mol, logS: -3.1) | ✅ Passed |

---

## 🚀 How to Run the Complete Pipeline

### Option 1. One-Click Pipeline Execution
```bash
python main.py
'''

Option 2. Step-by-Step Execution
Bash
# 1. Docking Benchmark
python compare_docking_results.py

# 2. Virtual Screening
python run_virtual_screening.py

# 3. ADMET Profiling
python predict_admet_properties.py

# 4. MD Simulation Analysis
python run_md_simulation_analysis.py

# 5. PyMOL 3D Visualization Script
python generate_pymol_script.py

# 6. Multi-Target Selectivity Screening & Heatmap Plot
python run_multi_target_screening.py
python plot_multi_target_results.py

# 7. AI De Novo Lead Optimization
python run_molecule_optimization.py

# Integrated Report Generation
python pipeline_summary_report.py
📁 Key Project Artifacts
docking_performance_comparison.png: Visual benchmark plot (Vina vs DiffDock).

multi_target_selectivity_heatmap.png: Multi-target selectivity heatmap plot.

virtual_screening_results.json: Screened top hits library data.

admet_filtered_candidates.json: ADMET filtered drug candidates.

md_validated_candidates.json: 100ns MD trajectory validation data.

multi_target_screening_results.json: Off-target selectivity evaluation data.

optimized_lead_analogs.json: AI generated optimized v2 lead compounds.

visualize_docking.pml: PyMOL automated rendering command file.
md_validated_candidates.json: 100ns MD trajectory validation data.

multi_target_screening_results.json: Off-target selectivity evaluation data.

optimized_lead_analogs.json: AI generated optimized v2 lead compounds.

visualize_docking.pml: PyMOL automated rendering command file.

