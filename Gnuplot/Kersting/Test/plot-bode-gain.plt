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
set xrange [10:2000]
set yrange [-20:20]
set datafile separator ','
set samples 10000

# Theoretical RC Low-Pass Filter
R = 220
dR = 0.01*R
C = 2.2e-6
dC = 0.1*C
fc = 1/(2*pi*R*C)
dfc = fc*sqrt( (dR/R)**2 + (dC/C)**2 )

print sprintf('Cutoff Frequency (theoretical): (%.2f +- %.2f) Hz', fc, dfc)



# Fit
# Tranmission function
h(x) = 20*log10(1/sqrt(1+(x/b)**2))
h_theo(x) = 20*log10(1/sqrt(1+(x/fc)**2))





set fit quiet
# Use absolute values for magnitudes so log10 never receives a negative argument.
# Treat zero values as invalid (NaN) to avoid division-by-zero.
fit h(x) 'fft.csv' using 1:(20*log10(abs($3)/abs($2))) via b

fc_fit_gain = b 


if (fc_fit_gain==fc_fit_gain) set arrow 1 lw 1 from fc_fit_gain, graph 0 to fc_fit_gain, graph 1 nohead lc rgb 'black' dt 2
if (fc_fit_gain==fc_fit_gain) set arrow 2 lw 1 from graph 0, first -3 to graph 1, first -3 nohead lc rgb 'black' dt 2
if (fc_fit_gain==fc_fit_gain) set label 1 sprintf('$f_c = %.0f$ Hz', fc_fit_gain) at fc_fit_gain, -3 offset 2,1




# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 2 pt 7 ps 0.5 lc rgb 'black'
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'green'
set style line 4 lw 2 pt 7 ps 0.5 lc rgb 'red'




# Plot
plot \
    'fft.csv' using 1:( ($2<=0 || $3<=0) ? NaN : 20*log10($3/$2) ) with line ls 4 title 'Data points',\
    h(x) with line ls 2 title 'Fitted Curve',\
    h_theo(x) with line ls 3 title 'Theoretical Curve'


    # f(x) with line ls 2 title 'Theoretical Curve'


# set out