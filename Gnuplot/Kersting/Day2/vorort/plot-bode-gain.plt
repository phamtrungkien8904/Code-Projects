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
set xrange [10000:100000]
set format x "%.0s%c"
set yrange [-40:20]
set datafile separator ','
set samples 10000

# Theoretical RC Low-Pass Filter
R = 51
dR = 0.01*R
C = 1e-6
dC = 0.1*C
L = 8.7e-6
dL = 0.01*L
fc = 1/(2*pi*sqrt(L*C))
dfc = fc*sqrt( (dR/R)**2 + (dC/C)**2 + (dL/L)**2 )
Q = R*sqrt(C/L)
dQ = Q*sqrt( (dR/R)**2 + (dC/C)**2 + (dL/L)**2 )
delta_f = fc/Q
ddelta_f = delta_f*sqrt( (dfc/fc)**2 + (dQ/Q)**2 )
f_lower = fc*(1/(2*Q) + sqrt( (1/(2*Q))**2 +1 ))
f_upper = fc*( -1/(2*Q) + sqrt( (1/(2*Q))**2 +1 ))

print sprintf('Cutoff Frequency (theoretical): (%.2f +- %.2f) Hz', fc, dfc)
print sprintf('Quality Factor (theoretical): (%.2f +- %.2f)', Q, dQ)
print sprintf('Bandwidth (theoretical): (%.2f +- %.2f) Hz', delta_f, ddelta_f)

# Numerical resonance and bandwidth imported from theory.py
stats 'theory_bandwidth.csv' using 1 name 'resStats' nooutput
stats 'theory_bandwidth.csv' using 2 name 'lowStats' nooutput
stats 'theory_bandwidth.csv' using 3 name 'highStats' nooutput
stats 'theory_bandwidth.csv' using 4 name 'bwStats' nooutput
f_res_num = resStats_max
f_lower_num = lowStats_max
f_upper_num = highStats_max
delta_f_num = bwStats_max

# Include the signal source's internal resistance when comparing gain.
Rs_theory = 50.0



# Tranmission function




if (f_lower_num==f_lower_num && f_upper_num==f_upper_num) {
    set arrow 6 lw 1 dt 4 lc rgb '#555555' from f_lower_num, graph 0 to f_lower_num, graph 0.9 nohead
    set arrow 7 lw 1 dt 4 lc rgb '#555555' from f_upper_num, graph 0 to f_upper_num, graph 0.9 nohead
    set arrow 8 lw 0.7 dt 4 heads lc rgb '#555555' from f_lower_num, graph 0.88 to f_upper_num, graph 0.88
}

if (f_res_num==f_res_num) {
    set arrow 9 lw 1 dt 4 lc rgb '#555555' from f_res_num, graph 0 to f_res_num, graph 0.9 nohead
}

label_y = 0.88
if (f_res_num==f_res_num) {
    set label 20 sprintf('Numerical f_res = %.0f Hz', f_res_num) at graph 0.02, graph label_y left tc rgb '#555555'
    label_y = label_y - 0.06
}
if (f_lower_num==f_lower_num) {
    set label 21 sprintf('Numerical f_lower = %.0f Hz', f_lower_num) at graph 0.02, graph label_y left tc rgb '#555555'
    label_y = label_y - 0.06
}
if (f_upper_num==f_upper_num) {
    set label 22 sprintf('Numerical f_upper = %.0f Hz', f_upper_num) at graph 0.02, graph label_y left tc rgb '#555555'
    label_y = label_y - 0.06
}
if (delta_f_num==delta_f_num) {
    set label 23 sprintf('Numerical bandwidth = %.0f Hz', delta_f_num) at graph 0.02, graph label_y left tc rgb '#555555'
}




# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 2 pt 7 ps 0.5 lc rgb 'black'
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'green'
set style line 4 lw 2 pt 7 ps 0.5 lc rgb 'red'




# Plot
plot \
    'fft.csv' using 1:(20*log10($3/$2)) with line ls 4 title 'Data points',\
    'theory.csv' using 1:5 with line ls 3 title 'Theoretical Curve'
    # h_theo(x) with line ls 3 title 'Theoretical Curve'



# set out