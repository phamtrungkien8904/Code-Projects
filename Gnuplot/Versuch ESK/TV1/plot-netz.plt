reset
set encoding utf8 

# ============================ Plot Settings ============================

set terminal epslatex color
set out 'tv1-netz.tex'

set title 'Belastungskurve des Netzgerätes'
set ylabel 'Klemmenspannung $U$/V'
set xlabel 'Belastungsstrom $I$/mA'
set yrange [0:11]
# set grid
set datafile separator ','
set samples 10000


set style line 2 lt 1 lw 2 lc rgb 'black' dt 3

# Plot
plot 'data-netz.csv' using 2:1 with points ls 2 title 'Messdaten'





set out