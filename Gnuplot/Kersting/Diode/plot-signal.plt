reset
set encoding utf8 

# set terminal epslatex color
# set out 'signal.tex'

# ============================ Plot Settings ============================

set title 'Characteristic of Diode'
set ylabel 'I (A)'
set xlabel 'U (V)'
# set grid
set xrange [0:0.5]
set yrange [0:1000]
# set logscale y 10
set datafile separator ','
set samples 10000



# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 pt 7 ps 0.3 lc rgb 'black'
set style line 2 pt 7 ps 0.3 lc rgb 'blue' 
set style line 3 pt 7 ps 0.3 lc rgb 'purple'
set style line 4 pt 7 ps 0.3 lc rgb 'red'

IS = 0.000001
e = 1.602e-19
k = 1.381e-23
T = 300

I_forward(x) = IS*(exp(e*x/(k*T)) - 1) 
I_reverse(x) = -IS*(exp(-e*x/(k*T)) - 1)

# Plot
plot \
    I_forward(x) ls 4 notitle, \
    I_reverse(x) ls 2 notitle

# set out