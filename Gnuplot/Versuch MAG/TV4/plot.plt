reset

# ============================ Plot Settings ============================


set title 'Spannung auf Rohspule vs. Gradient'
set xlabel 'Gradient $dV/dt$ (mV/s)'
set ylabel '$V_\text{out}$ (mV)'
set grid
set datafile separator ','

# ---------------- Measurement uncertainties ----------------
# Gradient in col 4 derived from Delta_V / t. Assume d(Delta_V)=0.1 mV, dt=0.1 s.
dV = 0.1      # mV
dt = 0.1      # s
# Propagate: G = ΔV / t => σ_G^2 = (∂G/∂ΔV)^2 σ_ΔV^2 + (∂G/∂t)^2 σ_t^2 = (1/t)^2 dV^2 + (ΔV/t^2)^2 dt^2
# Use average t to get a representative X error (or could compute point-wise if needed)
stats 'data.csv' using 1 name 'T' nooutput
T_mean = T_mean
stats 'data.csv' using 2 name 'DV' nooutput
DV_mean = DV_mean
X_ERR = sqrt( (dV/T_mean)**2 + (DV_mean*dt/T_mean**2)**2 )
Y_ERR = 2.0   # mV output uncertainty (instrument)

# Linear Regression Fit
f(x) = a*x+b

set fit quiet
fit f(x) 'data.csv' using 4:3:(X_ERR):(Y_ERR) xyerrors via a,b 
# only 2 Error when linear fit

# Error Bandbound
up(x)   = (a+a_err)*x + (b+b_err)
down(x) = (a-a_err)*x + (b-b_err)

# Compute R^2 and correlation r (unweighted)
stats 'data.csv' using 3 name 'Y' nooutput
SST = (Y_records > 1) ? (Y_records - 1) * Y_stddev**2 : 0
stats 'data.csv' using (f($4)-$3) name 'E' nooutput
SSE = E_sumsq
R2 = (SST > 0) ? (1.0 - SSE / SST) : 0/0
R2 = (R2 > 1) ? 1 : ((R2 < 0) ? 0 : R2)
r  = (R2 >= 0) ? sqrt(R2) : 0/0

# Styling
set style line 1 lt 1 lw 2 lc rgb '#d62728'
set style line 2 pt 7 ps 1 lc rgb '#111111'
set style line 3 lt 1 lw 2 lc rgb '#1f77b4' dashtype 2  # upper dashed
set style line 4 lt 1 lw 2 lc rgb '#1f77b4' dashtype 2  # lower dashed

# Plot
plot \
	'data.csv' using 4:3:(X_ERR):(Y_ERR) with xyerrorbars ls 2 title 'Daten', \
	f(x) with lines ls 1 title 'Fitgerade', \
	up(x) with lines ls 3 notitle, \
	down(x) with lines ls 4 notitle

###### Test value x ######
# x_test = 5
# dx_test = 0.1
# y_esti = f(x_test)
# dy_esti = a_err * x_test + b_err + a*dx_test

# Print Fit results
print sprintf('============================ OUTPUT y = a*x + b =============================')
print sprintf('Datafile:      %s', 'data.csv')
print sprintf('Uncertainties (avg): dGradient = %.3f mV/s, dV_out = %.3f mV', X_ERR, Y_ERR)
print sprintf('Fit results:   a = %.6f +- %.6f (%.2f%%)', a,a_err, (a!=0)? 100.0*a_err/abs(a) : 0/0 )
print sprintf('               b = %.6f +- %.6f (%.2f%%)', b,b_err, (b!=0)? 100.0*b_err/abs(b) : 0/0 )
print sprintf('Goodness:      R^2 = %.6f, r = %.6f,  N=%d', R2, r, Y_records)
# print sprintf('================================ Test value =================================')
# print sprintf('Test value:    x_test = %.6f +- %.6f', x_test, dx_test)
# print sprintf('Estimated:     y(%.6f) = %.6f +- %.6f (%.2f%%)', x_test, y_esti, dy_esti, (y_esti!=0)?100.0*dy_esti/abs(y_esti):0/0)
print sprintf('==================================== END ====================================')


