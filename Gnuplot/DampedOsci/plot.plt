################################################################################
# Example: Generate synthetic damped oscillation data, fit parameters, and plot
# Data columns: time (s), position (m)
################################################################################

reset


# ============================ Plot Settings ============================

set title 'Damped Oscillation Fit'
set xlabel 'Time (s)'
set ylabel 'Position (m)'
set grid
set datafile separator ','
set xrange [0:6]

# ---------------- Measurement (instrument) uncertainties ----------------
# Constant timing uncertainty (s) and position uncertainty (m)
X_ERR = 0.05   # dt
Y_ERR  = 0.05   # dx (used as y error because data column 2 is position)
print sprintf('Measurement uncertainties: dt = %.3f s, dx = %.3f m', X_ERR, Y_ERR)



f(x) = A * sin(w*x + phi) * exp(-gamma*x)

set fit quiet
fit f(x) 'data.csv' using 1:2:(Y_ERR) yerrors via A,w,gamma,phi

# Print fit results
print sprintf('Fit results: A=%.6f  w=%.6f  gamma=%.6f  phi=%.6f', A,w,gamma,phi)

# Compute R^2 and correlation r (unweighted)
stats 'data.csv' using 2 name 'Y' nooutput
SST = (Y_records > 1) ? (Y_records - 1) * Y_stddev**2 : 0
stats 'data.csv' using (f($1)-$2) name 'E' nooutput
SSE = E_sumsq
R2 = (SST > 0) ? (1.0 - SSE / SST) : 0/0
R2 = (R2 > 1) ? 1 : ((R2 < 0) ? 0 : R2)
r  = (R2 >= 0) ? sqrt(R2) : 0/0
print sprintf('Goodness: R^2=%.6f  r=%.6f  N=%d', R2, r, Y_records)

# Styling
set style line 1 lt 1 lw 2 lc rgb '#d62728'
set style line 2 pt 7 ps 1 lc rgb '#111111'

# Annotate fitted parameters on the plot

plot \
	'data.csv' using 1:2:(X_ERR):(Y_ERR) with xyerrorbars ls 2 title 'Data', \
	f(x) with lines ls 1 title sprintf('A=%.3f w=%.3f gamma=%.3f phi=%.3f R^2=%.4f',A,w,gamma,phi,R2)
