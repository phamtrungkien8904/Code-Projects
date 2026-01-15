reset
set encoding utf8 


set title "FFT Data"
set xlabel "Frequency (Hz)"
set ylabel "Amplitude"
set xrange [-500000:500000]
set yrange [0:5]
set sample 10000
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'green'

plot "fft_data_full.csv" using 1:4 with lines linestyle 1 notitle
    #  "fft_data_full.csv" using 1:3 with lines linestyle 2 title "FFT-Reference Signal", \
    #  "fft_data_full.csv" using 1:4 with lines linestyle 3 title "FFT-Mix Signal", \
    #  "fft_data_full.csv" using 1:5 with lines lt 1 lw 2 lc rgb 'black' title "FFT-Output Signal"

