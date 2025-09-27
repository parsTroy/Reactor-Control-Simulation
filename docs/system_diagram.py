#!/usr/bin/env python3
"""
System Diagram Generator
Creates a professional system architecture diagram for the reactor control simulation.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_system_diagram():
    """Create a professional system architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Define colors
    colors = {
        'cpp': '#4472C4',      # Blue
        'python': '#70AD47',   # Green
        'safety': '#C5504B',   # Red
        'data': '#FFC000',     # Orange
        'config': '#7030A0'    # Purple
    }
    
    # C++ Core Components
    cpp_rect = FancyBboxPatch((1, 6), 2.5, 2.5, boxstyle="round,pad=0.1", 
                             facecolor=colors['cpp'], alpha=0.8, edgecolor='black', linewidth=2)
    ax.add_patch(cpp_rect)
    ax.text(2.25, 7.5, 'C++ Core\nLibrary', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white')
    
    # Kinetics Solver
    kinetics_rect = FancyBboxPatch((0.5, 6.8), 1.2, 0.6, boxstyle="round,pad=0.05", 
                                  facecolor='white', alpha=0.9, edgecolor='black')
    ax.add_patch(kinetics_rect)
    ax.text(1.1, 7.1, 'Kinetics\nSolver', ha='center', va='center', fontsize=10)
    
    # PID Controller
    pid_rect = FancyBboxPatch((1.8, 6.8), 1.2, 0.6, boxstyle="round,pad=0.05", 
                             facecolor='white', alpha=0.9, edgecolor='black')
    ax.add_patch(pid_rect)
    ax.text(2.4, 7.1, 'PID\nController', ha='center', va='center', fontsize=10)
    
    # Safety Systems
    safety_rect = FancyBboxPatch((1, 4), 2.5, 1.5, boxstyle="round,pad=0.1", 
                                facecolor=colors['safety'], alpha=0.8, edgecolor='black', linewidth=2)
    ax.add_patch(safety_rect)
    ax.text(2.25, 4.8, 'Safety Systems', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white')
    
    # Overpower Protection
    overpower_rect = FancyBboxPatch((0.5, 4.2), 1.2, 0.6, boxstyle="round,pad=0.05", 
                                   facecolor='white', alpha=0.9, edgecolor='black')
    ax.add_patch(overpower_rect)
    ax.text(1.1, 4.5, 'Overpower\nProtection', ha='center', va='center', fontsize=9)
    
    # Coolant Loss Protection
    coolant_rect = FancyBboxPatch((1.8, 4.2), 1.2, 0.6, boxstyle="round,pad=0.05", 
                                 facecolor='white', alpha=0.9, edgecolor='black')
    ax.add_patch(coolant_rect)
    ax.text(2.4, 4.5, 'Coolant Loss\nProtection', ha='center', va='center', fontsize=9)
    
    # Python Dashboard
    python_rect = FancyBboxPatch((5, 6), 3.5, 2.5, boxstyle="round,pad=0.1", 
                                facecolor=colors['python'], alpha=0.8, edgecolor='black', linewidth=2)
    ax.add_patch(python_rect)
    ax.text(6.75, 7.5, 'Python Dashboard', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white')
    
    # Visualization
    viz_rect = FancyBboxPatch((5.2, 6.8), 1.5, 0.6, boxstyle="round,pad=0.05", 
                             facecolor='white', alpha=0.9, edgecolor='black')
    ax.add_patch(viz_rect)
    ax.text(5.95, 7.1, 'Real-time\nVisualization', ha='center', va='center', fontsize=10)
    
    # Data Logging
    data_rect = FancyBboxPatch((6.8, 6.8), 1.5, 0.6, boxstyle="round,pad=0.05", 
                              facecolor='white', alpha=0.9, edgecolor='black')
    ax.add_patch(data_rect)
    ax.text(7.55, 7.1, 'Data\nLogging', ha='center', va='center', fontsize=10)
    
    # Configuration
    config_rect = FancyBboxPatch((5.2, 6.2), 1.5, 0.6, boxstyle="round,pad=0.05", 
                                facecolor='white', alpha=0.9, edgecolor='black')
    ax.add_patch(config_rect)
    ax.text(5.95, 6.5, 'JSON\nConfiguration', ha='center', va='center', fontsize=10)
    
    # Event Monitoring
    event_rect = FancyBboxPatch((6.8, 6.2), 1.5, 0.6, boxstyle="round,pad=0.05", 
                               facecolor='white', alpha=0.9, edgecolor='black')
    ax.add_patch(event_rect)
    ax.text(7.55, 6.5, 'Event\nMonitoring', ha='center', va='center', fontsize=10)
    
    # Pybind11 Bindings
    bindings_rect = FancyBboxPatch((4, 5), 1.5, 1, boxstyle="round,pad=0.1", 
                                  facecolor=colors['config'], alpha=0.8, edgecolor='black', linewidth=2)
    ax.add_patch(bindings_rect)
    ax.text(4.75, 5.5, 'Pybind11\nBindings', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='white')
    
    # Data Flow
    data_flow_rect = FancyBboxPatch((1, 2), 7.5, 1.5, boxstyle="round,pad=0.1", 
                                   facecolor=colors['data'], alpha=0.6, edgecolor='black', linewidth=2)
    ax.add_patch(data_flow_rect)
    ax.text(4.75, 2.8, 'Data Flow: Simulation Data → Logging → Visualization → Analysis', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Add arrows to show data flow
    # C++ to Safety
    arrow1 = ConnectionPatch((2.25, 6), (2.25, 5.5), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5, 
                           mutation_scale=20, fc="black", linewidth=2)
    ax.add_patch(arrow1)
    
    # C++ to Python
    arrow2 = ConnectionPatch((3.5, 7.25), (5, 7.25), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5, 
                           mutation_scale=20, fc="black", linewidth=2)
    ax.add_patch(arrow2)
    
    # Safety to Python
    arrow3 = ConnectionPatch((2.25, 4), (4, 5.5), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5, 
                           mutation_scale=20, fc="black", linewidth=2)
    ax.add_patch(arrow3)
    
    # Python to Data Flow
    arrow4 = ConnectionPatch((6.75, 6), (6.75, 3.5), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5, 
                           mutation_scale=20, fc="black", linewidth=2)
    ax.add_patch(arrow4)
    
    # Add title
    ax.text(5, 9.5, 'Nuclear Reactor Control Simulation - System Architecture', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Add legend
    legend_elements = [
        patches.Patch(color=colors['cpp'], label='C++ Core Components'),
        patches.Patch(color=colors['python'], label='Python Dashboard'),
        patches.Patch(color=colors['safety'], label='Safety Systems'),
        patches.Patch(color=colors['config'], label='Integration Layer'),
        patches.Patch(color=colors['data'], label='Data Flow')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    plt.tight_layout()
    plt.savefig('docs/system_architecture.png', dpi=300, bbox_inches='tight')
    print("System architecture diagram saved as docs/system_architecture.png")
    plt.show()

if __name__ == "__main__":
    create_system_diagram()
