reset
set encoding utf8 

set terminal epslatex color
set out 'bodephasetheory.tex' ################# n series RC low-pass filter bode plot

# ============================ Plot Settings ============================



set title 'Bode diagram (Phase Shift)'
set ylabel 'Phase Shift $\Delta \phi$ (degree)'
set xlabel 'Frequency $f$ (Hz)'
# set grid
set logscale x 10
set xrange [100:1000000]
set format x "10^%.0T"
set yrange [-90:90]
set datafile separator ','
set samples 10000


# Theoretical RC Low-Pass Filter
R = 51
dR = 0.01*R
C = 1e-6
dC = 0.2*C
L = 8.7e-6
dL = 0.2*L
RS = 50  # Source resistance
RL = 0.2 # Inductor resistance
fc = 1/(2*pi*sqrt(L*C))
dfc = fc*sqrt( (dR/R)**2 + (dC/C)**2 + (dL/L)**2 )
Q = R*sqrt(C/L)
dQ = Q*sqrt( (dR/R)**2 + (dC/C)**2 + (dL/L)**2 )
QL = RL*sqrt(C/L)
delta_f = fc/Q
ddelta_f = delta_f*sqrt( (dfc/fc)**2 + (dQ/Q)**2 )
f_lower = fc*(1/(2*Q) + sqrt( (1/(2*Q))**2 +1 ))
f_upper = fc*( -1/(2*Q) + sqrt( (1/(2*Q))**2 +1 ))



p_theo(x) = -180/pi*atan((Q*x/fc*((x/fc)**2 + QL**2 -1))/((x/fc)**2 + QL**2 + Q*QL))



# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 2 pt 7 ps 0.5 lc rgb 'black'
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'green'
set style line 4 lw 2 pt 7 ps 0.5 lc rgb 'red'
set style line 5 lc rgb 'black' lw 1.1 dt 2

# Draw dashed line at fc where phase crosses zero
set arrow from fc, graph 0 to fc, graph 1 nohead ls 5
# Draw horizontal dashed line at 0 degrees
set arrow from graph 0, first 0 to graph 1, first 0 nohead ls 5

# Plot
plot \
    p_theo(x) with line ls 4 title 'Theoretical Curve'


set out