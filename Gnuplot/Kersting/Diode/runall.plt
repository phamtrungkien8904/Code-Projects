# --- Signal ---
set term wxt 0 position 0,0 size 600,400 title "Signal"
load 'signal.plt'

# --- Fit ---
set term wxt 1 position 600,0 size 600,400 title "Fit"
load 'fit-signal.plt'

# --- V-I Diagram ---
set term wxt 2 position 0,487 size 600,400 title "V-I Diagram"
load 'VI.plt'

# --- V_I Fit ---
set term wxt 3 position 600,487 size 600,400 title "V-I Fit"
load 'fit-VI.plt'

pause -1 "Hit Enter to close all plots"