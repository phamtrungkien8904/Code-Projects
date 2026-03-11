reset
set encoding utf8 

# set terminal epslatex color
# set out 'TV2.tex' #################

# ============================ Plot Settings ============================



set title " Auftreffpunkte und Landeskreis"
set ylabel 'y (cm)'
set xlabel 'x (cm)'
# set grid
set xrange [-10:30]
set yrange [-20:20]
set size ratio 1
# set format x "%.0s%c"
set datafile separator ','
set samples 10000


R = 13.75;
up(x) = sqrt(R**2 - (x-11.95)**2)
down(x) = -sqrt(R**2 - (x-11.95)**2)

# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 4 lc rgb 'blue' 
set style line 3 lw 2.5 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 2 pt 4 lc rgb 'red' 
set style line 5 lw 2 pt 4 lc rgb 'black' 



# Plot
plot \
    'data-TV2.csv' using 2:3 with points ls 4 title 'Auftreffpunkte (Projektile)',\
    'data-TV2.csv' using 4:5 with points ls 2 title 'Auftreffpunkte (Target)',\
     up(x) with lines ls 3 title 'Landekreis',\
        down(x) with lines ls 3 notitle,\
        0.0 with lines ls 1 notitle



# set out