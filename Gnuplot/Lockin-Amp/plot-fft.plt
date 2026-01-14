set datafile separator ","

set output "fft_plot.png"
set title "FFT Data"
set xlabel "Frequency (Hz)"
set ylabel "Magnitude"
set grid
plot "fft_data.csv" using 1:2 with lines title "FFT"