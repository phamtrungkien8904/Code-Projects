import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
import warnings
warnings.filterwarnings('ignore')

def bremsstrahlung_spectrum_wavelength(wavelength, lambda_min):
    """
    Calculate bremsstrahlung spectrum using the correct formula: I(λ) ~ (λ/λ_min - 1)/λ²
    
    Parameters:
    wavelength: array of wavelengths
    lambda_min: minimum wavelength (maximum energy cutoff)
    """
    intensity = np.zeros_like(wavelength)
    valid_wavelengths = wavelength >= lambda_min
    
    # Apply the correct bremsstrahlung formula
    intensity[valid_wavelengths] = ((wavelength[valid_wavelengths] / lambda_min) - 1) / (wavelength[valid_wavelengths]**2)
    
    return intensity

def bremsstrahlung_spectrum(energy, tube_voltage_kv, z_target=29):
    """
    Calculate bremsstrahlung spectrum in energy space using the wavelength formula.
    Convert energy to wavelength, apply formula, then convert back.
    """
    # Physical constants
    h = constants.h  # Planck constant
    c = constants.c  # Speed of light
    e = constants.e  # Elementary charge
    
    # Convert energy (keV) to wavelength (m)
    energy_j = energy * 1e3 * e  # Convert keV to Joules
    wavelength = h * c / energy_j  # de Broglie wavelength
    
    # Calculate minimum wavelength from maximum energy
    max_energy_j = tube_voltage_kv * 1e3 * e
    lambda_min = h * c / max_energy_j
    
    # Calculate bremsstrahlung intensity using wavelength formula
    intensity = bremsstrahlung_spectrum_wavelength(wavelength, lambda_min)
    
    # Apply atomic number scaling
    intensity *= z_target
    
    # Normalize to prevent extremely large values
    if np.max(intensity) > 0:
        intensity = intensity / np.max(intensity)
    
    return intensity

def characteristic_lines_copper():
    """Define characteristic X-ray lines for copper with realistic intensities."""
    lines = {
        'Ka1': {'energy': 8.048, 'intensity': 1.0, 'width': 0.05},   # Normalized to 1.0
        'Ka2': {'energy': 8.028, 'intensity': 0.51, 'width': 0.05},  # Relative to Ka1
        'Kb1': {'energy': 8.905, 'intensity': 0.17, 'width': 0.06},  
        'Kb3': {'energy': 8.977, 'intensity': 0.09, 'width': 0.06},   
    }
    return lines

def gaussian_peak(energy, center, intensity, width):
    """Generate a Gaussian peak with proper normalization."""
    sigma = width / (2 * np.sqrt(2 * np.log(2)))
    return intensity * np.exp(-0.5 * ((energy - center) / sigma) ** 2)

def create_xray_spectrum(tube_voltage=40, energy_range=(0.5, 45), num_points=1000):
    """Create complete X-ray spectrum with proper scaling."""
    energy = np.linspace(energy_range[0], energy_range[1], num_points)
    
    # Calculate bremsstrahlung spectrum using the correct wavelength formula
    bremsstrahlung = bremsstrahlung_spectrum(energy, tube_voltage)
    
    # Add characteristic lines
    characteristic = np.zeros_like(energy)
    cu_lines = characteristic_lines_copper()
    
    for line_name, line_data in cu_lines.items():
        if line_data['energy'] < tube_voltage:
            characteristic += gaussian_peak(energy, 
                                           line_data['energy'], 
                                           line_data['intensity'], 
                                           line_data['width'])
    
    # Scale characteristic lines to be visible but not overwhelming
    characteristic *= 0.3  # Make characteristic lines 30% of max bremsstrahlung
    
    # Total spectrum
    total_spectrum = bremsstrahlung + characteristic
    
    return energy, total_spectrum, bremsstrahlung, characteristic

def plot_xray_spectrum(tube_voltage=40, save_plot=False, filename='xray_spectrum.png'):
    """Create and display X-ray spectrum plot with proper scaling."""
    energy, total, bremsstrahlung, characteristic = create_xray_spectrum(tube_voltage)
    
    plt.figure(figsize=(12, 8))
    
    # Plot with better scaling
    plt.plot(energy, total, 'k-', linewidth=2.5, label='Total Spectrum')
    plt.plot(energy, bremsstrahlung, 'b--', linewidth=1.5, label='Bremsstrahlung', alpha=0.7)
    plt.plot(energy, characteristic, 'r-', linewidth=2, label='Characteristic X-rays')
    
    # Add characteristic line markers
    cu_lines = characteristic_lines_copper()
    max_intensity = np.max(total)
    
    for line_name, line_data in cu_lines.items():
        if line_data['energy'] < tube_voltage:
            plt.axvline(x=line_data['energy'], color='red', linestyle=':', alpha=0.6, linewidth=1)
            # Position labels better
            label_height = max_intensity * (0.7 + 0.1 * (line_data['intensity']))
            plt.annotate(f'Cu {line_name}\n{line_data["energy"]:.3f} keV', 
                        xy=(line_data['energy'], label_height),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=9, ha='left',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # Better formatting
    plt.xlabel('Energy (keV)', fontsize=14, fontweight='bold')
    plt.ylabel('Relative Intensity', fontsize=14, fontweight='bold')
    plt.title(f'X-ray Spectrum of Copper Anode (Tube Voltage: {tube_voltage} kV)\nUsing Correct Bremsstrahlung Formula: I(λ) ∝ (λ/λ_min - 1)/λ²', 
              fontsize=16, fontweight='bold', pad=20)
    
    plt.legend(loc='upper right', fontsize=12, framealpha=0.9)
    plt.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    
    # Set reasonable axis limits
    plt.xlim(0, min(tube_voltage + 5, 50))
    plt.ylim(0, max_intensity * 1.15)
    
    # Add informative text box
    info_text = (f"Key Features:\n"
                f"• Continuous bremsstrahlung spectrum\n"
                f"• Formula: I(λ) ∝ (λ/λ_min - 1)/λ²\n"
                f"• Sharp characteristic peaks\n"
                f"• Maximum energy = {tube_voltage} keV\n"
                f"• Cu Kα lines dominate")
    
    plt.text(0.98, 0.98, info_text, transform=plt.gca().transAxes, 
             verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
             fontsize=10)
    
    plt.tight_layout()
    
    if save_plot:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Plot saved as {filename}")
    
    plt.show()

def compare_tube_voltages():
    """Compare X-ray spectra at different tube voltages with proper scaling."""
    voltages = [25, 35, 45]
    colors = ['blue', 'red', 'green']
    
    plt.figure(figsize=(14, 8))
    
    for i, voltage in enumerate(voltages):
        energy, total, _, _ = create_xray_spectrum(voltage, energy_range=(0.5, 50))
        # Normalize each spectrum for comparison
        total_normalized = total / np.max(total) if np.max(total) > 0 else total
        plt.plot(energy, total_normalized, color=colors[i], linewidth=2.5, 
                label=f'{voltage} kV', alpha=0.8)
    
    plt.xlabel('Energy (keV)', fontsize=14, fontweight='bold')
    plt.ylabel('Normalized Intensity', fontsize=14, fontweight='bold')
    plt.title('X-ray Spectra Comparison at Different Tube Voltages\n(Copper Anode) - Correct Bremsstrahlung Formula', 
              fontsize=16, fontweight='bold', pad=20)
    plt.legend(fontsize=12, framealpha=0.9)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 20)
    plt.ylim(0, 1.1)
    plt.tight_layout()
    plt.show()

# Main execution
if __name__ == "__main__":
    print("X-ray Spectrum Generator for Copper Anode")
    print("Using Correct Bremsstrahlung Formula: I(λ) ∝ (λ/λ_min - 1)/λ²")
    print("=" * 60)
    
    # Create standard spectrum plot
    print("Generating X-ray spectrum plot...")
    plot_xray_spectrum(tube_voltage=40, save_plot=True)
    
    # Create comparison plot
    print("\nGenerating comparison plot for different tube voltages...")
    compare_tube_voltages()
    
    # Print characteristic line information
    print("\nCopper Characteristic X-ray Lines:")
    print("-" * 35)
    cu_lines = characteristic_lines_copper()
    for line_name, line_data in cu_lines.items():
        print(f"Cu {line_name}: {line_data['energy']:.3f} keV "
              f"(Relative intensity: {line_data['intensity']:.2f})")
    
    print("\nPhysics Notes:")
    print("-" * 15)
    print("• Bremsstrahlung: I(λ) ∝ (λ/λ_min - 1)/λ² formula used")
    print("• Characteristic X-rays: Discrete lines from electron transitions") 
    print("• Copper K-absorption edge: ~8.98 keV")
    print("• Maximum X-ray energy equals tube voltage")