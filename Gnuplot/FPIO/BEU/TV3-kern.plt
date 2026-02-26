reset
set encoding utf8 

# set terminal epslatex color
# set out 'plot-off.tex' #################

# ============================ Plot Settings ============================



set title "Intensitätsprofil"
set ylabel 'Intensität/Imax'
set xlabel 'Pixel'
# set grid
set xrange [0:2048]
set yrange [0:100]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000


lambda = 632.8e-9
b = 0.20e-3
r = 0.25
p = 0.028/2048 #m/pixel
k = 1.0*pi*b*p/(lambda*r)
c = 1.0
a = 100.0
d = 1175.0


sinc(z) = (abs(z) < 1e-12 ? 1.0 : sin(z)/z)
f(x) = a*(sinc(k*(x-d)))**2 + c

set fit quiet
fit f(x) 'TV3.csv' using 1:2 via a,c,k,d


print sprintf("k = %4f +- %4f", k, k_err)

b = k*lambda*r/(pi*p)
db = k_err*lambda*r/(pi*p)
print sprintf("b = %4f +- %4f mm", b*1e3, db*1e3)

r_new = pi*(0.2e-3)*p/(k*lambda)
print sprintf("r = %4f mm", r_new*1e3)
# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 pt 4 lc rgb 'red' 



# Plot
plot \
    'TV3.csv' using 1:2 with lines ls 4 title 'Data',\
    f(x) with lines ls 2 title 'Fit'



# set out