"""
Visualization Module for Timing Attack Demonstration
Generates graphs and charts to illustrate timing attack vulnerabilities.

FIXED VERSION - Works on Windows/Mac/Linux without absolute paths
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import numpy as np
from timing_attack_demo import timing_attack_simulation, analyze_results
import json
import os

# Set style for professional-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# Create outputs directory if it doesn't exist
OUTPUT_DIR = 'outputs'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"✓ Created '{OUTPUT_DIR}' directory")


def create_comparison_plot(results):
    """
    Create a comparison plot showing timing differences between vulnerable and secure implementations.
    
    Args:
        results (dict): Results from timing_attack_simulation
    """
    num_chars = sorted(results['vulnerable'].keys())
    
    vuln_times = [results['vulnerable'][i]['avg_time'] for i in num_chars]
    secure_times = [results['secure'][i]['avg_time'] for i in num_chars]
    
    vuln_std = [results['vulnerable'][i]['std_dev'] for i in num_chars]
    secure_std = [results['secure'][i]['std_dev'] for i in num_chars]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Vulnerable Implementation
    ax1.errorbar(num_chars, vuln_times, yerr=vuln_std, 
                marker='o', linewidth=2, markersize=8, 
                color='#e74c3c', capsize=5, label='Average Time')
    ax1.set_xlabel('Number of Correct Characters', fontweight='bold')
    ax1.set_ylabel('Execution Time (nanoseconds)', fontweight='bold')
    ax1.set_title('VULNERABLE Implementation\n(Character-by-Character with Early Exit)', 
                 fontweight='bold', color='#e74c3c')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Add trend line
    z = np.polyfit(num_chars, vuln_times, 1)
    p = np.poly1d(z)
    ax1.plot(num_chars, p(num_chars), "--", color='#c0392b', 
            alpha=0.8, linewidth=2, label=f'Trend (slope={z[0]:.2f})')
    ax1.legend()
    
    # Plot 2: Secure Implementation
    ax2.errorbar(num_chars, secure_times, yerr=secure_std,
                marker='s', linewidth=2, markersize=8,
                color='#27ae60', capsize=5, label='Average Time')
    ax2.set_xlabel('Number of Correct Characters', fontweight='bold')
    ax2.set_ylabel('Execution Time (nanoseconds)', fontweight='bold')
    ax2.set_title('SECURE Implementation\n(Constant-Time Comparison)', 
                 fontweight='bold', color='#27ae60')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Add trend line
    z2 = np.polyfit(num_chars, secure_times, 1)
    p2 = np.poly1d(z2)
    ax2.plot(num_chars, p2(num_chars), "--", color='#229954',
            alpha=0.8, linewidth=2, label=f'Trend (slope={z2[0]:.2f})')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'timing_comparison.png'), dpi=300, bbox_inches='tight')
    print("✓ Saved: timing_comparison.png")
    plt.close()


def create_overlay_plot(results):
    """
    Create an overlay plot comparing both implementations directly.
    
    Args:
        results (dict): Results from timing_attack_simulation
    """
    num_chars = sorted(results['vulnerable'].keys())
    
    vuln_times = [results['vulnerable'][i]['avg_time'] for i in num_chars]
    secure_times = [results['secure'][i]['avg_time'] for i in num_chars]
    
    plt.figure(figsize=(14, 8))
    
    plt.plot(num_chars, vuln_times, marker='o', linewidth=3, 
            markersize=10, color='#e74c3c', label='Vulnerable (Early Exit)', 
            alpha=0.8)
    plt.plot(num_chars, secure_times, marker='s', linewidth=3,
            markersize=10, color='#27ae60', label='Secure (Constant-Time)',
            alpha=0.8)
    
    plt.xlabel('Number of Correct Characters', fontweight='bold', fontsize=14)
    plt.ylabel('Average Execution Time (nanoseconds)', fontweight='bold', fontsize=14)
    plt.title('Timing Attack Vulnerability Comparison\nVulnerable vs. Secure Implementation', 
             fontweight='bold', fontsize=16)
    plt.legend(fontsize=12, loc='best')
    plt.grid(True, alpha=0.3)
    
    # Add shaded region to show vulnerability
    plt.fill_between(num_chars, vuln_times, secure_times, 
                    alpha=0.2, color='yellow',
                    label='Timing Leak Zone')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'overlay_comparison.png'), dpi=300, bbox_inches='tight')
    print("✓ Saved: overlay_comparison.png")
    plt.close()


def create_distribution_plot(results):
    """
    Create box plots showing time distribution for different numbers of correct characters.
    
    Args:
        results (dict): Results from timing_attack_simulation
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Vulnerable implementation distribution
    vuln_data = [results['vulnerable'][i]['all_times'] for i in sorted(results['vulnerable'].keys())]
    positions = sorted(results['vulnerable'].keys())
    
    bp1 = ax1.boxplot(vuln_data, positions=positions, widths=0.6,
                     patch_artist=True, showmeans=True,
                     boxprops=dict(facecolor='#e74c3c', alpha=0.7),
                     medianprops=dict(color='#c0392b', linewidth=2),
                     meanprops=dict(marker='D', markerfacecolor='#c0392b', markersize=6))
    
    ax1.set_xlabel('Number of Correct Characters', fontweight='bold')
    ax1.set_ylabel('Execution Time (nanoseconds)', fontweight='bold')
    ax1.set_title('VULNERABLE Implementation - Time Distribution', 
                 fontweight='bold', color='#e74c3c')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Secure implementation distribution
    secure_data = [results['secure'][i]['all_times'] for i in sorted(results['secure'].keys())]
    
    bp2 = ax2.boxplot(secure_data, positions=positions, widths=0.6,
                     patch_artist=True, showmeans=True,
                     boxprops=dict(facecolor='#27ae60', alpha=0.7),
                     medianprops=dict(color='#229954', linewidth=2),
                     meanprops=dict(marker='D', markerfacecolor='#229954', markersize=6))
    
    ax2.set_xlabel('Number of Correct Characters', fontweight='bold')
    ax2.set_ylabel('Execution Time (nanoseconds)', fontweight='bold')
    ax2.set_title('SECURE Implementation - Time Distribution', 
                 fontweight='bold', color='#27ae60')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'distribution_plot.png'), dpi=300, bbox_inches='tight')
    print("✓ Saved: distribution_plot.png")
    plt.close()


def create_correlation_plot(results):
    """
    Create a scatter plot showing correlation between correct characters and timing.
    
    Args:
        results (dict): Results from timing_attack_simulation
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    num_chars = sorted(results['vulnerable'].keys())
    
    # Vulnerable - scatter all measurements
    for i in num_chars:
        times = results['vulnerable'][i]['all_times']
        x = [i] * len(times)
        ax1.scatter(x, times, alpha=0.3, s=10, color='#e74c3c')
    
    # Add average line
    vuln_avgs = [results['vulnerable'][i]['avg_time'] for i in num_chars]
    ax1.plot(num_chars, vuln_avgs, 'o-', color='#c0392b', 
            linewidth=3, markersize=10, label='Average', zorder=5)
    
    ax1.set_xlabel('Number of Correct Characters', fontweight='bold')
    ax1.set_ylabel('Execution Time (nanoseconds)', fontweight='bold')
    ax1.set_title('VULNERABLE - Correlation Analysis\n(High Correlation = Information Leak)', 
                 fontweight='bold', color='#e74c3c')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Secure - scatter all measurements
    for i in num_chars:
        times = results['secure'][i]['all_times']
        x = [i] * len(times)
        ax2.scatter(x, times, alpha=0.3, s=10, color='#27ae60')
    
    # Add average line
    secure_avgs = [results['secure'][i]['avg_time'] for i in num_chars]
    ax2.plot(num_chars, secure_avgs, 's-', color='#229954',
            linewidth=3, markersize=10, label='Average', zorder=5)
    
    ax2.set_xlabel('Number of Correct Characters', fontweight='bold')
    ax2.set_ylabel('Execution Time (nanoseconds)', fontweight='bold')
    ax2.set_title('SECURE - Correlation Analysis\n(Low Correlation = No Information Leak)', 
                 fontweight='bold', color='#27ae60')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'correlation_analysis.png'), dpi=300, bbox_inches='tight')
    print("✓ Saved: correlation_analysis.png")
    plt.close()


def create_summary_chart(analysis):
    """
    Create a summary bar chart comparing key metrics.
    
    Args:
        analysis (dict): Analysis results from analyze_results
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    metrics = ['Correlation\nCoefficient', 'Time Increase/\nVariance (%)']
    vulnerable_values = [
        analysis['vulnerable_correlation'],
        analysis['time_increase_percentage']
    ]
    secure_values = [
        abs(analysis['secure_correlation']),
        analysis['secure_variance_percentage']
    ]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, vulnerable_values, width, 
                   label='Vulnerable', color='#e74c3c', alpha=0.8)
    bars2 = ax.bar(x + width/2, secure_values, width,
                   label='Secure', color='#27ae60', alpha=0.8)
    
    ax.set_ylabel('Value', fontweight='bold', fontsize=12)
    ax.set_title('Security Metrics Comparison\n(Lower is Better)', 
                fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=11)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'metrics_summary.png'), dpi=300, bbox_inches='tight')
    print("✓ Saved: metrics_summary.png")
    plt.close()


def generate_all_visualizations():
    """
    Main function to run simulation and generate all visualizations.
    """
    print("\n" + "="*70)
    print("GENERATING VISUALIZATIONS")
    print("="*70 + "\n")
    
    # Run simulation
    print("Running timing attack simulation...")
    results, correct_pwd = timing_attack_simulation(password_length=8)
    
    # Analyze results
    print("\nAnalyzing results...")
    analysis = analyze_results(results)
    
    # Save raw results to JSON
    results_serializable = {}
    for impl in ['vulnerable', 'secure']:
        results_serializable[impl] = {}
        for key, value in results[impl].items():
            results_serializable[impl][key] = {
                'avg_time': value['avg_time'],
                'std_dev': value['std_dev']
            }
    
    json_path = os.path.join(OUTPUT_DIR, 'results_data.json')
    with open(json_path, 'w') as f:
        json.dump({
            'results': results_serializable,
            'analysis': analysis,
            'password_length': results['password_length']
        }, f, indent=2)
    
    print(f"\n✓ Saved: results_data.json\n")
    
    # Create all plots
    print("Generating plots...")
    print("-" * 70)
    
    create_comparison_plot(results)
    create_overlay_plot(results)
    create_distribution_plot(results)
    create_correlation_plot(results)
    create_summary_chart(analysis)
    
    print("-" * 70)
    print("\n" + "="*70)
    print("ALL VISUALIZATIONS COMPLETED SUCCESSFULLY!")
    print("="*70)
    print(f"\nAll files saved to: {os.path.abspath(OUTPUT_DIR)}/")
    print("\nGenerated files:")
    print("  1. timing_comparison.png - Side-by-side comparison")
    print("  2. overlay_comparison.png - Direct overlay comparison")
    print("  3. distribution_plot.png - Box plots showing distributions")
    print("  4. correlation_analysis.png - Scatter plots with correlation")
    print("  5. metrics_summary.png - Bar chart of key metrics")
    print("  6. results_data.json - Raw numerical data")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    generate_all_visualizations()