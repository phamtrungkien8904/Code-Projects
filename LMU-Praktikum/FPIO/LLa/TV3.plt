reset
set encoding utf8 

set terminal epslatex color
set out 'TV3.tex' #################

# ============================ Plot Settings ============================

set title 'Photometrisches Abstandsgesetz'
set ylabel 'Beleuchtungsstärke [klx]'
set xlabel 'Abstand [cm]'
# set grid
# set xrange [0:1.5]
# set yrange [0:1.5]
# set size ratio 1
set datafile separator ','
set samples 10000


E0 = 0.060

# Initial guesses for fit parameters (required before first use)
a = 1.0
b = 0.01



set fit quiet
f(x) = a / x**2 + b
fit f(x) 'data-TV3.csv' using 1:($2 - E0) via a,b
print sprintf('f(x) = (%.2f + %.2f) x + (%.2f + %.2f)', a, a_err, b, b_err)  

# f_up(x) = (a + a_err)*x + (b + b_err)
# f_down(x) = (a - a_err)*x + (b - b_err)



# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 1.5 pt 4 lc rgb 'red' 

# Plot
plot \
    'data-TV3.csv' using 1:($2 - E0) with point ls 4 title 'Messdaten',\
    f(x) with lines ls 2 title 'Fit'#,\
    
set out