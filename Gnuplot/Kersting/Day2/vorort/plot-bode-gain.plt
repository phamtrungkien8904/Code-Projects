reset
set encoding utf8 

# set terminal epslatex color
# set out 'bodegain.tex' ################# n series RC low-pass filter bode plot

# ============================ Plot Settings ============================



set title 'Bode diagram (Gain)'
set ylabel 'Gain $G$ (dB)'
set xlabel 'Frequency $f$ (Hz)'
# set grid
set logscale x 10
set xrange [100:1000000]
set format x "%.0s%c"
set yrange [-50:0]
set datafile separator ','
set samples 10000

# Read theoretical bandwidth from CSV (hardcoded from theory_output.csv)
bandwidth = 6763.387901877438708
f_lower_theo = 50786.31260521382501
f_upper_theo = 57549.70050709126372
print sprintf('Bandwidth (theory): %.2f Hz', bandwidth)

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







# print sprintf('Cutoff Frequency (theoretical): (%.2f +- %.2f) Hz', fc, dfc)
# print sprintf('Bandwidth (theoretical): %.2f Hz', bw)





# Tranmission function
G_theo(x) = 20*log10(1/sqrt((1 + Q*QL/(QL**2 + (x/fc)**2))**2 + (Q*x/fc)**2 *(1-1/(QL**2 + (x/fc)**2))**2))
G_fit(x) = 20*log10(1/sqrt((1 + q*qL/(qL**2 + (x/c)**2))**2 + (q*x/c)**2 *(1-1/(qL**2 + (x/c)**2))**2))
G_drop = 20*log10(1/sqrt(1+ (Q*QL)**2 + 2*Q*QL/(1+QL**2)))
G_0 = 20*log10(1/(1 + Q/QL))
G_inf(x) = 20*log10(1/(Q*x/fc)) 


set fit quiet
set fit errorvariables

q = Q
qL = QL
c = fc

fit[10000:100000] G_fit(x) 'fft.csv' using 1:(20*log10($3/$2)) via q, qL, c




# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 2 pt 7 ps 0.5 lc rgb 'black'
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'green'
set style line 4 lw 2 pt 7 ps 0.5 lc rgb 'red'
set style line 5 lw 1.5 dt 2 lc rgb 'gray50'  # Dashed gray for reference lines

# Draw transparent gray rectangle between f_lower and f_upper
set obj 1 rect from f_lower_theo, graph 0 to f_upper_theo, graph 1 fc rgb 'gray' fs transparent solid 0.3 noborder


# Draw vertical dashed lines at resonance frequency, f_lower, and f_upper
set arrow from fc, graph 0 to fc, graph 1 nohead ls 5
set arrow from f_lower_theo, graph 0 to f_lower_theo, graph 1 nohead ls 5
set arrow from f_upper_theo, graph 0 to f_upper_theo, graph 1 nohead ls 5

# Draw horizontal dashed line through G_0
set arrow from graph 0, first G_0 to graph 0.3, first G_0 nohead ls 5



# Plot
plot \
    'fft.csv' using 1:( ($1>=10000 && $1<=100000) ? 20*log10($3/$2) : 1/0 ) with line ls 4 title 'Data points',\
    G_fit(x) with line ls 2 title 'Fit',\
    G_theo(x) with line ls 1 title 'Theoretical curve',\
    G_inf(x) with line ls 5 notitle



# set out