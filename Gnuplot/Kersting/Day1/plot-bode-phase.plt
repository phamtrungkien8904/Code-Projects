reset
set encoding utf8 

# set terminal epslatex color
# set out 'bodephase.tex' ################# n series RC low-pass filter bode plot

# ============================ Plot Settings ============================



set title 'Bode diagram (Phase Difference)'
set ylabel 'Phase Difference $\Delta \phi$ (degree)'
set xlabel 'Frequency $f$ (Hz)'
# set grid
set logscale x 10
set xrange [10:2000]
set yrange [-90:0]
set datafile separator ','
set samples 10000

# Theoretical RC Low-Pass Filter
# R = 220
# dR = 0.01*R
# C = 2.2e-6
# dC = 0.1*C
# fc = 1/(2*pi*R*C)
# dfc = fc*sqrt( (dR/R)**2 + (dC/C)**2 )

# print fc 
# print dfc



# Fit
# Tranmission function
h(x) = -180/pi*atan(x/d)


set fit quiet
fit h(x) 'fft.csv' using ($1*1000):7 via d

fc_fit_phase = d

if (fc_fit_phase==fc_fit_phase) set arrow 1 lw 1 dt 2 from fc_fit_phase, graph 0 to fc_fit_phase, graph 1 nohead lc rgb 'black'
if (fc_fit_phase==fc_fit_phase) set arrow 2 lw 1 dt 2 from graph 0, first h(fc_fit_phase) to graph 1, first h(fc_fit_phase) nohead lc rgb 'black'
if (fc_fit_phase==fc_fit_phase) set label 1 sprintf('$f_c = %.0f$ Hz', fc_fit_phase) at fc_fit_phase, h(fc_fit_phase) offset 2,1



# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 2 pt 7 ps 0.5 lc rgb 'black'
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 2 pt 7 ps 0.5 lc rgb 'red'



# Plot
plot \
    'fft.csv' using ($1*1000):7 with line ls 4 title 'Data points',\
    h(x) with line ls 2 title 'Fitted Curve'


# set out