




# Values
stats 'theory_output.csv' using 1 name 'fc' nooutput
f_c = fc_min

stats 'theory_output.csv' using 2 name 'flower' nooutput
f_lower = flower_min

stats 'theory_output.csv' using 3 name 'fupper' nooutput
f_upper = fupper_min

bandwidth = f_upper - f_lower

stats 'theory_output.csv' using 5 name 'Gres' nooutput
G_peak = Gres_min
G_3dB_level = G_peak - 3
G_inf(x) = -20*log10(1/(Q*x/f_c))


set obj rect from f_lower, graph 0.12 to f_upper, graph 1 fc rgb 'gray' fs transparent solid 0.3 noborder

set arrow from fc, graph 0.12 to fc, graph 1 nohead ls 5
set arrow from f_lower, graph 0.12 to f_lower, graph 1 nohead ls 5
set arrow from f_upper, graph 0.12 to f_upper, graph 1 nohead ls 5

set arrow from graph 0, first G_0 to graph 0.5, first G_0 nohead ls 5
set arrow from graph 0, first G_peak to graph 1, first G_peak nohead ls 5
set arrow from graph 0, first G_3dB_level to graph 1, first G_3dB_level nohead ls 5

# Two-way arrow showing -3 dB difference
set arrow from graph 0.05, first G_peak to graph 0.05, first G_3dB_level heads lc rgb 'black' lw 1.5



# Component values
R = 51
dR = 0.01*R
C = 1e-6
dC = 0.2*C
L = 8.7e-6
dL = 0.2*L
Q = R*sqrt(C/L)

# Use valid color syntax and distinct colors per dataset
set style line 1 lw 2 pt 7 ps 0.5 lc rgb 'black'
set style line 2 lw 1.5 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'green'
set style line 4 lw 2 pt 7 ps 0.5 lc rgb 'red'
set style line 5 lc rgb 'black' lw 1.1 dt 2

# Labels
set label 1 sprintf('$f_c$ = %.0f Hz', fc) at sqrt(f_lower*f_upper), graph 0.09 center tc rgb 'black' font ',10'
set label 2 sprintf('$\Delta f$ = %.0f Hz', bandwidth) at sqrt(f_lower*f_upper), graph 0.05 center tc rgb 'black' font ',10'
set label 3 sprintf('$G_0$ = %.2f dB', G_0) at graph 0.45, first G_0 - 1 right tc rgb 'black' font ',10'
set label 4 '$\Delta G_\infty$/dec = -20' at 200000, G_inf(200000)-2 center tc rgb 'black' font ',10' rotate by -45
set label 5 '-3 dB' at graph 0.07, first ((G_peak + G_3dB_level)/2) left tc rgb 'black' font ',10'

# Plot
set title 'Theoritical Bode diagram (Gain)'
set ylabel 'Gain $G$ (dB)'
set xlabel 'Frequency $f$ (Hz)'
# set grid
set logscale x 10
set xrange [100:1000000]
set format x "10^%.0T"
set yrange [-50:0] 
set datafile separator ','
set samples 10000

plot \
    'theory.csv' using 1:5 with line ls 4 notitle,\
    [70000:*]G_inf(x) with line lc rgb 'black' lw 1 dt 2 notitle
