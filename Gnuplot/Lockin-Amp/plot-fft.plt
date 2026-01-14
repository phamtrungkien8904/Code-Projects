reset
set encoding utf8 


set title "FFT Data"
set xlabel "Frequency (Hz)"
set ylabel "Amplitude"
set xrange [-1000:1000]
set yrange [0:5]
set sample 10000
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'green'

plot "fft_data.csv" using 1:2 with lines linestyle 1 title "FFT"