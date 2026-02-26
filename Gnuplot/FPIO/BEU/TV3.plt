reset
set encoding utf8 

# set terminal epslatex color
# set out 'plot-off.tex' #################

# ============================ Plot Settings ============================



set title "Intensity"
set ylabel 'Intensity/Imax'
set xlabel 'Pixel'
# set grid
set xrange [0:2048]
set yrange [0:100]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000


lambda = 632.8e-9
r = 0.20e5

u(x) = k*(x-d)
sinc2(x) = (abs(u(x)) < 1e-12 ? 1.0 : (sin(u(x))/u(x))**2)
f(x) = a*sinc2(x) + c

stats 'TV3.csv' using 2 nooutput
ymax = STATS_max
c = STATS_min
a = ymax - c
d = 1180.0

k = 0.04
set fit quiet
fit [1080:1280] f(x) 'TV3.csv' using 1:2 via a,c,d
fit f(x) 'TV3.csv' using 1:2 via a,k,c,d

b = k*lambda*r/pi
print sprintf("b = %7f mm", b*1e3)




# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 pt 7 lc rgb 'red' 



# Plot
plot \
    'TV3.csv' using 1:2 with lines ls 4 title 'Data',\
    f(x) with lines ls 2 title 'Fit'



# set out