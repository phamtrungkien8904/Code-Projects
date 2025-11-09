reset
set encoding utf8 

# set terminal epslatex color
# set out 'bodegain.tex' ################# n series RC low-pass filter bode plot

# ============================ Plot Settings ============================




# set samples 10000

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



set datafile separator ','
stats 'theory_output.csv' using 4 name 'bw' nooutput
print sprintf("Theoritical bandwidth = %.2f Hz", bw_min)


# print sprintf('Cutoff Frequency (theoretical): (%.2f +- %.2f) Hz', fc, dfc)
# print sprintf('Bandwidth (theoretical): %.2f Hz', bw)





# Gain (theory)
G_theo(x) = 20*log10(1/sqrt((1 + Q*QL/(QL**2 + (x/fc)**2))**2 + (Q*x/fc)**2 *(1-1/(QL**2 + (x/fc)**2))**2))
G_drop = 20*log10(1/sqrt(1+ (Q*QL)**2 + 2*Q*QL/(1+QL**2)))
G_0 = 20*log10(1/(1 + Q/QL))
G_inf(x) = 20*log10(1/(Q*x/fc)) 

# Gain (fit) - initialize fit parameters first
set fit quiet
set fit errorvariables

q = Q
qL = QL
c = fc

G_fit(x) = 20*log10(1/sqrt((1 + q*qL/(qL**2 + (x/c)**2))**2 + (q*x/c)**2 *(1-1/(qL**2 + (x/c)**2))**2))
G_drop_fit = 20*log10(1/sqrt(1+ (q*qL)**2 + 2*q*qL/(1+qL**2)))
G_0_fit = 20*log10(1/(1 + q/qL))
G_inf_fit(x) = 20*log10(1/(q*x/c))

fit[10000:100000] G_fit(x) 'fft.csv' using 1:8 via q, qL, c


# Find resonance frequency (peak) and -3dB frequencies from the fitted curve
fc_fit = c

stats 'fft.csv' using 8 name 'G' nooutput
G_peak_fit = G_max 
G_3dB_level = G_peak_fit - 3.0

stats 'fft.csv' using 1:( ( $8 >= G_3dB_level) ? $8 : 1/0 ) name 'Gbw' nooutput
f_lower_fit = Gbw_min_x
f_upper_fit = Gbw_max_x
bandwidth_fit = f_upper_fit - f_lower_fit




print sprintf('Fitted resonance frequency: %.2f Hz', fc_fit)
print sprintf('Fitted G_peak: %.2f dB', G_peak_fit)
print sprintf('Fitted f_lower: %.2f Hz', f_lower_fit)
print sprintf('Fitted f_upper: %.2f Hz', f_upper_fit)
print sprintf('Fitted bandwidth: %.2f Hz', bandwidth_fit)

# Read theoretical and fitted gain at specific frequencies if needed




# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 2 pt 7 ps 0.5 lc rgb 'black'
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'green'
set style line 4 lw 2 pt 7 ps 0.5 lc rgb 'red'




set obj 1 rect from f_lower_fit, graph 0 to f_upper_fit, graph 1 fc rgb 'gray' fs transparent solid 0.3 noborder

set arrow from fc_fit, graph 0 to fc_fit, graph 1 lw 1 dt 2 nohead lc rgb 'black'
set arrow from f_lower_fit, graph 0 to f_lower_fit, graph 1 lw 1 dt 2 nohead lc rgb 'black'
set arrow from f_upper_fit, graph 0 to f_upper_fit, graph 1 lw 1 dt 2 nohead lc rgb 'black'

set arrow from graph 0, first G_0_fit to graph 0.3, first G_0_fit nohead lc rgb 'black'

# Plot
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
plot \
    'fft.csv' using 1:8 with line ls 4 title 'Data points',\
    G_fit(x) with line ls 2 title 'Fit',\
    G_inf_fit(x) with line ls 3 title 'Asymptotic curve',\
    G_theo(x) with line ls 1 title 'Theoretical curve'






# set out