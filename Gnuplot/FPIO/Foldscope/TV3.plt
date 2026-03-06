reset
set encoding utf8 

# set terminal epslatex color
# set out 'peaks.tex' #################

# ============================ Plot Settings ============================



set title "Vergrößerung des Foldscopes (Analyse)"
set ylabel 'Bildgröße $B$ (mm)'
set xlabel 'Gegenstandsgröße $G$ (mm)'
# set grid
set xrange [0.75:1.50]
set yrange [100:200]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000

f(x) = a*x + b
set fit quiet
fit f(x) 'data.csv' using 1:2 via a,b
f_up(x) = (a + a_err)*x + (b + b_err)
f_down(x) = (a - a_err)*x + (b - b_err)
g(x) = 140.0*x

# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 

set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 1.5 pt 4 lc rgb 'red' 
set style line 5 lw 2 pt 4 lc rgb 'black' 



# Plot
plot \
    'data.csv' using 1:2 with points ls 4 title 'Messdaten',\
     f(x) with lines ls 2 title 'Fitsgerade',\
        f_up(x) with lines ls 1 title 'Fit-Fehler',\
        f_down(x) with lines ls 1 notitle,\
        g(x) with lines ls 3 title 'Theoretische Gerade'

stats 'data.csv' using 2 name 'Y' nooutput
# FIT_WSSR is the residual sum of squares from the preceding fit command.
R2 = 1 - FIT_WSSR / Y_ssd
print sprintf("Fit-Parameter: a = %.4f ± %.4f, b = %.4f ± %.4f, R^2 = %.4f", a, a_err, b, b_err, R2)
print sprintf("Vergrößerung VT = %.4f ± %.4f", a, a_err)



# set out