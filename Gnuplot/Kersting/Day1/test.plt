reset
set encoding utf8 

# set terminal epslatex color
# set out 'day34.tex'

# ============================ Plot Settings ============================

set title 'Bode diagram'
set ylabel 'Magnitude (dB)'
set xlabel 'Frequency (Hz)'
# set grid
set xrange [0:2000]
set logscale x 10
# set yrange [-10:10]
set datafile separator ','
set samples 10000




set style line 1 pt 7 ps 0.3 lc rgb 'red'

R = 220
C = 2.2e-6
fc = 1/(2*pi*R*C)
print fc

f(x) = 20*log10(1/sqrt(1+(x/fc)**2))


# Plot
plot \
    f(x) with line ls 2 title 'Theoretical'



# set out