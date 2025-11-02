reset
set encoding utf8 

# set terminal epslatex color
# set out 'bodephase.tex' ################# n series RC low-pass filter bode plot

# ============================ Plot Settings ============================



set title 'Bode diagram (Phase Shift)'
set ylabel 'Phase Shift $\Delta \phi$ (degree)'
set xlabel 'Frequency $f$ (Hz)'
# set grid
set logscale x 10
set xrange [1000:10000]
set format x "%.0s%c"
set yrange [-90:90]
set datafile separator ','
set samples 10000

# Theoretical RC Low-Pass Filter
R = 100
dR = 0.01*R
C = 100e-9
dC = 0.1*C
L = 0.03
dL = 0.01*L
fc = 1/(2*pi*sqrt(L*C))
dfc = fc*sqrt( (dR/R)**2 + (dC/C)**2 + (dL/L)**2 )
Q = sqrt(L/C)/R
dQ = Q*sqrt( (dR/R)**2 + (dC/C)**2 + (dL/L)**2 )
delta_f = fc/Q
ddelta_f = delta_f*sqrt( (dfc/fc)**2 + (dQ/Q)**2 )
sigma = 1/(2*Q)

# print fc 
# print dfc



# Fit
# Tranmission function
p(x) = -180/pi*atan(Q*(x/d - d/x))
p_theo(x) = -180/pi*atan(Q*(x/fc - fc/x))

set fit quiet
fit p(x) 'fft.csv' using 1:7 via d

fc_fit_phase = d

if (fc_fit_phase==fc_fit_phase) set arrow 1 lw 1 dt 2 from fc_fit_phase, graph 0 to fc_fit_phase, graph 1 nohead lc rgb 'black'
if (fc_fit_phase==fc_fit_phase) set arrow 2 lw 1 dt 2 from graph 0, first p(fc_fit_phase) to graph 1, first p(fc_fit_phase) nohead lc rgb 'black'
if (fc_fit_phase==fc_fit_phase) set label 1 sprintf('$f_c = %.0f$ Hz', fc_fit_phase) at fc_fit_phase, p(fc_fit_phase) offset 2,1



# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 2 pt 7 ps 0.5 lc rgb 'black'
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'green'
set style line 4 lw 2 pt 7 ps 0.5 lc rgb 'red'



# Plot
plot \
    'fft.csv' using 1:7 with line ls 4 title 'Data points',\
    p(x) with line ls 2 title 'Fitted Curve',\
    p_theo(x) with line ls 3 title 'Theoretical Curve'


# set out