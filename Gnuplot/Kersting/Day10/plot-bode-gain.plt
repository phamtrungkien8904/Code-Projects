reset
set encoding utf8 

# set terminal epslatex color
# set out 'bodegain.tex' ################# n series RC low-pass filter bode plot

# ============================ Plot Settings ============================



set title 'Bode diagram (Gain)'
set ylabel 'Gain $G$ (dB)'
set xlabel 'Frequency $f$ (Hz)'
# set grid
set logscale x 10
set xrange [1:3]
# set format x "%.0s%c"
set yrange [0:20]
set datafile separator ','
set samples 10000





# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 2 pt 7 ps 0.5 lc rgb 'black'
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'green'
set style line 4 lw 2 pt 7 ps 0.5 lc rgb 'red'




# Plot
plot \
    'fft1575.csv' using 1:(20*log10($3/$2)) with line ls 4 title 'R=15.75kΩ',\
    'fft1500.csv' using 1:(20*log10($3/$2)) with line ls 2 title 'R=15.00kΩ',\
    'fft1400.csv' using 1:(20*log10($3/$2)) with line ls 3 title 'R=14.00kΩ',\
    'fft1300.csv' using 1:(20*log10($3/$2)) with line ls 1 title 'R=13.00kΩ'

    # f(x) with line ls 2 title 'Theoretical Curve'


# set out