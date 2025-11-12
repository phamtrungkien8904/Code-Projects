reset
set encoding utf8 

set terminal epslatex color
set out 'bodegainideal.tex' #################


# Component values
R = 51
dR = 0.01*R
C = 1e-6
dC = 0.2*C
L = 8.7e-6
dL = 0.2*L
Q = R*sqrt(C/L)
fc = 1/(2*pi*sqrt(L*C))
f_lower = fc*(-1/(2*Q) + sqrt( (1/(2*Q))**2 +1 ))
f_upper = fc*(1/(2*Q) + sqrt( (1/(2*Q))**2 +1 ))
bandwidth = f_upper - f_lower

set datafile separator ','

G(x) = 20*log10(1/sqrt(1 + Q**2 * (x/fc - fc/x)**2))
G_peak = G(fc)
G_3dB_level = G_peak - 3.0
G_inf(x) = -20*log10(Q) - 20*log10(x/fc)

p(x) = -180/pi*atan(Q*(x/fc - fc/x))







# Use valid color syntax and distinct colors per dataset
set style line 1 lw 2 pt 7 ps 0.5 lc rgb 'black'
set style line 2 lw 1.5 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'green'
set style line 4 lw 2 pt 7 ps 0.5 lc rgb 'red'
set style line 5 lc rgb 'black' lw 1.1 dt 2

set obj rect from f_lower, graph 0.12 to f_upper, graph 1 fc rgb 'gray' fs transparent solid 0.3 noborder

set arrow from fc, graph 0.12 to fc, graph 1 nohead ls 5
set arrow from f_lower, graph 0.12 to f_lower, graph 1 nohead ls 5
set arrow from f_upper, graph 0.12 to f_upper, graph 1 nohead ls 5

set arrow from graph 0, first G_peak to graph 1, first G_peak nohead ls 5
set arrow from graph 0, first G_3dB_level to graph 1, first G_3dB_level nohead ls 5

# Two-way arrow showing -3 dB difference
set arrow from graph 0.05, first G_peak to graph 0.05, first G_3dB_level heads lc rgb 'black' lw 1.5
# Labels
set label 1 sprintf('$f_c$ = %.0f Hz', fc) at sqrt(f_lower*f_upper), graph 0.09 center tc rgb 'black' font ',10'
set label 2 sprintf('$\Delta f$ = %.0f Hz', bandwidth) at sqrt(f_lower*f_upper), graph 0.05 center tc rgb 'black' font ',10'
set label 5 '-3 dB' at graph 0.07, first ((G_peak + G_3dB_level)/2) left tc rgb 'black' font ',10'

# # Draw dashed line at fc where phase crosses zero
# set arrow from fc, graph 0 to fc, graph 1 nohead ls 5
# # Draw horizontal dashed line at 0 degrees
# set arrow from graph 0, first 0 to graph 1, first 0 nohead ls 5


# Plot
set title 'Bode diagram of ideal BPF (Gain)'
set ylabel 'Gain $G$ (dB)'
set xlabel 'Frequency $f$ (Hz)'
# set grid
set logscale x 10
set xrange [1000:1000000]
set format x "10^%.0T"
set yrange [-50:20] 
# set yrange [-90:90]

set samples 100000

plot \
    G(x) with line ls 4 notitle

# plot \
#     p(x) with line ls 4 notitle
set out