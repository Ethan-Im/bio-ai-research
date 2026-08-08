import matplotlib.pyplot as plt
import numpy as np

def generate_performance_plots():
    """
    Generates comparison plots between Physics-based (AutoDock Vina) 
    and AI-based (DiffDock) docking performances.
    """
    # Set visual design theme
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Benchmark metrics data
    methods = ['AutoDock Vina\n(Physics-based)', 'DiffDock\n(AI Generative)']
    comp_time = [45.2, 1.5]  # Computation time in seconds
    rmsd_vals = [2.1, 1.2]   # Positional error RMSD in Angstroms

    colors = ['#4A90E2', '#50E3C2']

    # Subplot 1: Computation Time Comparison
    bars1 = ax1.bar(methods, comp_time, color=colors, width=0.5, edgecolor='black', linewidth=0.8)
    ax1.set_ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
    ax1.set_title('1. Computation Speed Comparison\n(Lower is Faster)', fontsize=14, fontweight='bold', pad=15)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Annotate bar values
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 1.0, f'{yval}s', ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Add speedup highlight annotation
    ax1.annotate('30.1x Speedup!', xy=(1, 1.5), xytext=(0.5, 25),
                 arrowprops=dict(facecolor='crimson', shrink=0.08, width=2, headwidth=8),
                 fontsize=12, fontweight='bold', color='crimson', ha='center')

    # Subplot 2: Structural Accuracy (RMSD)
    bars2 = ax2.bar(methods, rmsd_vals, color=colors, width=0.5, edgecolor='black', linewidth=0.8)
    ax2.set_ylabel('RMSD (Angstroms, Å)', fontsize=12, fontweight='bold')
    ax2.set_title('2. Structural Accuracy (RMSD)\n(Lower is More Accurate)', fontsize=14, fontweight='bold', pad=15)
    ax2.axhline(y=2.0, color='r', linestyle='--', label='Success Threshold (2.0 Å)')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    ax2.legend(loc='upper right')

    # Annotate bar values
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.05, f'{yval} Å', ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.tight_layout()
    output_filename = 'docking_performance_comparison.png'
    plt.savefig(output_filename, dpi=300)
    print(f"📊 Visualization plot saved as: {output_filename}")

if __name__ == "__main__":
    generate_performance_plots()
