reset
set encoding utf8 

# set terminal epslatex color
# set out 'bode-exp.tex' ################# 

# ============================ Plot Settings ============================



set title 'Bode diagram (Gain)'
set ylabel 'Gain $G$ (dB)'
set xlabel 'Frequency $f$ (kHz)'
# set grid
set logscale x 10
set xrange [1:5]
# set format x "%.0s%c"
set yrange [-10:20]
set datafile separator ','
set samples 10000





# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 2 pt 7 ps 0.5 lc rgb 'black'
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'green'
set style line 4 lw 2 pt 7 ps 0.5 lc rgb 'red'
set style line 5 lw 2 pt 7 ps 0.5 lc rgb 'purple'

set style line 6 lw 2 pt 7 ps 0.5 lc rgb 'red' dt 2
set style line 7 lw 2 pt 7 ps 0.5 lc rgb 'blue' dt 2
set style line 8 lw 2 pt 7 ps 0.5 lc rgb 'green' dt 2
set style line 9 lw 2 pt 7 ps 0.5 lc rgb 'purple' dt 2
set style line 10 lw 2 pt 7 ps 0.5 lc rgb 'black' dt 2

f = 2.25
G_theo(k,x) = 20*log10((k/(5-k))/sqrt(1+(sqrt(2)/(5-k)*(x/f - f/x))**2))

# Vertical marker at f = 2.25
# set arrow 1 from f, graph 0 to f, graph 1 nohead lw 1 dt 2 lc rgb 'black'
# set label 1 'f_0 = 2.25 kHz' at f-0.07, graph 0.32 rotate by 90 center tc rgb 'black'

# Vertical marker at f_exp
f_exp = 2.13
set arrow 1 from f_exp, graph 0 to f_exp, graph 1 nohead lw 1 dt 2 lc rgb 'black'
set label 1 'f_{0,theo} = 2.13 kHz' at f_exp-0.07, graph 0.32 rotate by 90 center tc rgb 'black'

# Plot
plot \
    'fft-35k.csv' using 1:(20*log10($3/$2)) with lines ls 4 title 'R=35kΩ',\
    'fft-30k.csv' using 1:(20*log10($3/$2)) with lines ls 2 title 'R=30kΩ',\
    'fft-25k.csv' using 1:(20*log10($3/$2)) with lines ls 3 title 'R=25kΩ',\
    'fft-20k.csv' using 1:(20*log10($3/$2)) with lines ls 1 title 'R=20kΩ',\
    'fft-10k.csv' using 1:(20*log10($3/$2)) with lines ls 5 title 'R=10kΩ',\

# plot \
#     G_theo(4.5,x) with lines ls 4 title 'R=35kΩ',\
#     G_theo(4.0,x) with lines ls 2 title 'R=30kΩ',\
#     G_theo(3.5,x) with lines ls 3 title 'R=25kΩ',\
#     G_theo(3.0,x) with lines ls 1 title 'R=20kΩ',\
#     G_theo(2.0,x) with lines ls 5 title 'R=10kΩ'




# set out