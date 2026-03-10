reset
set encoding utf8 

# set terminal epslatex color
# set out 'peaks.tex' #################

# ============================ Plot Settings ============================



set title " Auftreffpunkte und Landeskreis"
set ylabel 'y (cm)'
set xlabel 'x (cm)'
# set grid
# set xrange [0:0.4]
# set yrange [0:1.5]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000

# f(x) = a*x + b
# set fit quiet
# fit f(x) 'data-TV4.csv' using (($1)**2):2 via a,b
# f_up(x) = (a + a_err)*x + (b + b_err)
# f_down(x) = (a - a_err)*x + (b - b_err)

# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 1.5 pt 4 lc rgb 'red' 
set style line 5 lw 2 pt 4 lc rgb 'black' 



# Plot
plot \
    'data-TV1.csv' using 2:3 with points ls 4 title 'Messdaten'
    #  f(x) with lines ls 2 title 'Fitsgerade'

# stats 'data-TV4.csv' using 2 name 'Y' nooutput
# stats 'data-TV4.csv' using (($2 - f(($1)**2))**2) name 'E' nooutput
# R2 = 1 - E_sum / Y_ssd
# print sprintf("Fit-Parameter: a = %.4f ± %.4f, b = %.4f ± %.4f, R^2 = %.4f", a, a_err, b, b_err, R2)
# print sprintf("Gravitationsbeschleunigung g = (%.4f ± %.4f) m/s^2", 2*a, 2*a_err)



# set out