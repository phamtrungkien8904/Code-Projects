reset
set encoding utf8 

# set terminal epslatex color
# set out 'fft.tex' ################# n series RC low-pass filter bode plot

# ============================ Plot Settings ============================



set title 'FFT of Sweep Signal'
set ylabel 'Amplitude $A$ (a.u.)'
set xlabel 'Frequency $f$ (Hz)'
# set grid
set xrange [10:2000]
set datafile separator ','
set samples 10000




# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 2 pt 7 ps 0.5 lc rgb 'black'
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 2 pt 7 ps 0.5 lc rgb 'red'



# Plot
plot \
    'fft.csv' using 1:2 with line ls 2 title 'Input Signal',\
    'fft.csv' using 1:3 with line ls 4 title 'Output Signal'


# set out