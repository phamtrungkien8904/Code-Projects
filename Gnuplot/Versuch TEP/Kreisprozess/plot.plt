reset
# =========================== Stirling Prozess ===========================
# ============================ Plot Settings ============================

set title 'p-V Diagram (Stirling Prozess)'
set xlabel 'Volumenskala (mm)'
set ylabel 'Druck (mmHg)'
set xrange[0:120]
set yrange[0:1000]

# set grid
set datafile separator ','

# ---------------- Measurement (instrument) uncertainties ----------------


p0 =  716 #mmHg
dp0 = 0.1 #mmHg

T0 = 273 #K

# Styling
set style line 1 pt 7 ps 1 lc rgb '#d62728'
set style line 2 pt 7 ps 1 lc rgb '#111111'
set style line 3 pt 7 ps 1 lc rgb '#2ca02c'
set style line 4 pt 7 ps 1 lc rgb '#1f77b4'


# Plot
plot \
	'data1.csv' using 1:(p0-$2) ls 1 title 'Isotherm T=90*C',\
    'data2.csv' using (90):(p0-$2) ls 2 title 'Isochor h=90mm',\
    'data3.csv' using 1:(p0-$2) ls 3 title 'Isotherm T=0*C',\
    'data4.csv' using 1:(p0) ls 4 title 'Isobar p=p0'


