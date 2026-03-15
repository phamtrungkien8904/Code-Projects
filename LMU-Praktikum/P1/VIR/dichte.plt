reset
set encoding utf8 

# set terminal epslatex color
# set out 'TV3.tex' #################

# ============================ Plot Settings ============================

set title 'Analyse des Aräometers'
set ylabel 'Senklänge [mm]'
set xlabel 'Anzahl der Murmeln'
# set grid
set xrange [0:8]
set yrange [0:100]
set datafile separator ','
set samples 1000

set fit quiet
f(x) = a*x + b
fit f(x) 'dichte.csv' using 1:2 via a,b
print sprintf('Fitergebnis: y = (%.2f + %.2f) x + (%.2f + %.2f)', a, a_err, b, b_err)  
f_up(x) = (a + a_err)*x + (b + b_err)
f_down(x) = (a - a_err)*x + (b - b_err)

##### Auswertung #####
m = 5.5e-3 # Masse einer Murmel in kg
d = 31.4e-3 # Durchmesser des Gefäßes in m
d_err = 1e-3 # Fehler des Durchmessers in m

rho0 = 4*m/(a*pi*d**2) # Dichte der Flüssigkeit in kg/m^3
rho0_err = rho0 * sqrt((a_err/a)**2 + (2* d_err/d)**2) # Fehler der Dichte in kg/m^3

print sprintf('Dichte der Spülmittel: rho0_exp = (%.2f ± %.2f) kg/m^3', rho0, rho0_err)

# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 2 pt 4 ps 1.5 lc rgb 'red' 

# Plot
plot \
    'dichte.csv' using 1:2 with point ls 4 title 'Messdaten', \
    f(x) with line ls 2 title 'Fitgerade',\
    f_up(x) with line ls 1 title 'Fehler', \
    f_down(x) with line ls 1 title 'Fehler'
    
# set out