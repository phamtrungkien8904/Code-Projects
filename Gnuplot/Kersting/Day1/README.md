

This folder contains tools for generating signals, performing Fourier transforms, and visualizing results using both Python and Gnuplot.

## Files Overview

### Python Scripts
- **`signal-gen.py`** - Generates a synthetic signal with multiple frequency components
- **`fft.py`** - Performs Fast Fourier Transform analysis on input/output signals from `day1.csv`
- **`test.py`** - Implements Fourier transform using Euler's method (manual DFT implementation)

### Gnuplot Scripts
- **`plot-signal.plt`** - Plots time-domain signals (input vs output)
- **`plot-fft.plt`** - Plots frequency-domain amplitude spectrum

### Data Files
- **`signal.csv`** - Generated signal data (time, value)
- **`day1.csv`** - Input/output signal data for comparison
- **`fft.csv`** - FFT results (frequency, amplitudes, phases)
- **`fft-test.csv`** - FFT results from Euler's method implementation

## Usage

### 1. Generate a Test Signal
```powershell
python signal-gen.py
```
Creates `signal.csv` with a composite sine wave (5 Hz + 10 Hz components).

### 2. Perform FFT Analysis

**Option A: Using scipy FFT (faster, recommended)**
```powershell
python fft.py
```
Analyzes `day1.csv`, computes amplitude and phase spectra, outputs `fft.csv`.

**Option B: Using Euler's method (educational)**
```powershell
python test.py
```
Implements DFT from scratch using Euler's formula, analyzes `signal.csv`, outputs `fft-test.csv` and displays a plot.

### 3. Visualize with Gnuplot

**Plot time-domain signals:**
```powershell
gnuplot -persist plot-signal.plt
```

**Plot frequency-domain (FFT) amplitudes:**
```powershell
gnuplot -persist plot-fft.plt
```

## Typical Workflow

1. Start with existing data (`day1.csv`) or generate new signals (`signal-gen.py`)
2. Run FFT analysis (`fft.py` or `test.py`)
3. Visualize results using Gnuplot scripts
4. Analyze amplitude/phase relationships between input and output signals

## Requirements

- Python 3.x with numpy, scipy, matplotlib
- Gnuplot (for visualization)

## Notes

- `fft.py` compares input vs output signals and computes phase differences
- Frequencies are in kHz for `day1.csv` analysis, Hz for generated signals
- Phase unwrapping is applied to avoid discontinuities
- `test.py` demonstrates the mathematical foundations of DFT using complex exponentials