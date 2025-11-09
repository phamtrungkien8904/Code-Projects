# --- Signal ---
set term wxt 0 position 0,0 size 600,400 title "Signal"
load 'plot-signal.plt'

# --- FFT ---
set term wxt 1 position 600,0 size 600,400 title "FFT"
load 'plot-fft.plt'

# --- Bode Gain ---
set term wxt 2 position 0,487 size 600,400 title "Bode Gain"
load 'plot-bode-gain.plt'

# --- Bode Phase ---
set term wxt 3 position 600,487 size 600,400 title "Bode Phase"
load 'plot-bode-phase.plt'

set term wxt 4 position 1200,0 size 600,400 title "Bode Gain Theory"
load 'plot-bode-gain-theory.plt'

set term wxt 5 position 1200,487 size 600,400 title "Bode Phase Theory"
load 'plot-bode-phase-theory.plt'


pause -1 "Hit Enter to close all plots"

