reset
set encoding utf8 

# set terminal epslatex color
# set out 'TV3.tex' #################

# ============================ Plot Settings ============================

set title ' Eigenfrequenzen einer Luftsäule'
set ylabel 'Resonanzfrequenz (Hz)'
set xlabel 'Ordnungszahl'
# set grid
set xrange [0:10]
set yrange [0:4000]
set datafile separator ','
set samples 10000





set fit quiet
f(x) = a*x + b
fit f(x) 'data-3.csv' using 1:2:(15) yerrors via a,b
print sprintf('f(x) = (%.2f + %.2f) x + (%.2f + %.2f)', a, a_err, b, b_err)  

f_up(x) = (a + a_err)*x + (b + b_err)
f_down(x) = (a - a_err)*x + (b - b_err)



# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 1.5 pt 4 lc rgb 'red' 




# Plot
plot \
    'data-3.csv' using 1:2 with point ls 4 title 'Messdaten', \
    f(x) with line ls 4 title 'Fitgerade'
    # f_up(x) with line ls 1 title 'Fehler', \
    # f_down(x) with line ls 1 title 'Fehler'
    
# set out