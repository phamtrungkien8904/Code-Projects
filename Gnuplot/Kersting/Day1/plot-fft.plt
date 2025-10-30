reset
set encoding utf8 

# set terminal epslatex color
# set out 'day34.tex'

# ============================ Plot Settings ============================



set title 'Bode diagram'
# set ylabel 'Amplitude (V)'
set ylabel 'Magnitude $G$ (dB)'
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

print fc 
print dfc

f(x) = 20*log10(1/sqrt(1+(x/fc)**2))

# Fit
g(x) = 20*log10(a/sqrt(1+(x/b)**2))
a = 1

set fit quiet
fit g(x) 'fft.csv' using ($1*1000):( ($2<=0 || $3<=0) ? NaN : 20*log10($3/$2) ) via a,b 

if (a > 0) \
    fc_fit = b * sqrt(10**((3 + 20*log10(a))/10.0) - 1) \
else \
    fc_fit = NaN

if (fc_fit==fc_fit) set arrow 1 lw 1 from fc_fit, graph 0 to fc_fit, graph 1 nohead lc rgb 'black' dt 2
if (fc_fit==fc_fit) set arrow 2 lw 1 from graph 0, first -3 to graph 1, first -3 nohead lc rgb 'black' dt 2
if (fc_fit==fc_fit) set label 1 sprintf('fc = %.1f Hz', fc_fit) at fc_fit, -3 offset 2,1

# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 2 pt 7 ps 0.5 lc rgb 'black'
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 2 pt 7 ps 0.5 lc rgb 'red'




# Plot
# plot \
#     'fft.csv' using ($1*1000):2 with line ls 2 title 'Input Signal',\
#     'fft.csv' using ($1*1000):3 with line ls 4 title 'Output Signal'
    

plot \
    'fft.csv' using ($1*1000):( ($2<=0 || $3<=0) ? NaN : 20*log10($3/$2) ) with line ls 4 title 'Data points',\
    g(x) with line ls 2 title 'Fitted Curve'

    # f(x) with line ls 2 title 'Theoretical Curve',\


# set out