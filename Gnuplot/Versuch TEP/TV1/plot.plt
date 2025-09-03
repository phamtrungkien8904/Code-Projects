reset
set encoding utf8 

# ============================ Plot Settings ============================

set terminal epslatex color
set out 'tv1.tex'

set title 'Isotherme Zustandsänderung bei $\Theta = 90^\circ$C'
set xlabel '$p_0/(p_0 - \Delta p)$'
set ylabel 'x/mm'
# set grid
set datafile separator ','
set samples 10000

# ---------------- Measurement (instrument) uncertainties ----------------


# Linear Regression Fit
f(x) = a*x+b

p0 = 716
xA = 72

set fit quiet
fit f(x) 'data.csv' using 1:(p0/(p0 - $2)) via a,b 
# only 2 Error when linear fit

# Error Bandbound
up(x)   = (a+a_err)*x + (b+b_err)
down(x) = (a-a_err)*x + (b-b_err)

# Compute R^2 and correlation r on transformed data yT = p0/(p0 - y)
# First stats with two expressions for correlation, then separate stats for variance of yT.
stats 'data.csv' using 1:(p0/(p0 - $2)) name 'T' nooutput   # gives T_correlation
stats 'data.csv' using (p0/(p0 - $2)) name 'Yt' nooutput          # single-expression stats (Yt_stddev)
SST = (Yt_records > 1) ? (Yt_records - 1) * Yt_stddev**2 : 0
stats 'data.csv' using (f($1)) - (p0/(p0 - $2)) name 'RES' nooutput
SSE = RES_sumsq
R2 = (SST > 0) ? (1.0 - SSE / SST) : 0/0
if (R2 > 1) R2 = 1
if (R2 < 0) R2 = 0
r  = T_correlation

# Styling
set style line 1 lt 1 lw 2 lc rgb '#d62728'
set style line 2 pt 7 ps 1 lc rgb '#111111'
set style line 3 lt 1 lw 2 lc rgb '#1f77b4' dashtype 2  # upper dashed
set style line 4 lt 1 lw 2 lc rgb '#1f77b4' dashtype 2  # lower dashed

# Plot (data as points instead of connected lines)
set style fill solid 1.0
plot \
	'data.csv' using 1:(p0/(p0 - $2)) with points ls 2 title 'Messdaten', \
	f(x) with lines ls 1 title 'Fitgerade', \
	up(x) with lines ls 3 title 'Fehlergrenze', \
	down(x) with lines ls 4 title 'Fehlergrenze'

###### Test value x ######
# x_test = 5
# dx_test = 0.1
# y_esti = f(x_test)
# dy_esti = a_err * x_test + b_err + a*dx_test

# Print Fit results
print sprintf('============================ OUTPUT y = a*x + b =============================')
print sprintf('Datafile:      %s', 'data.csv')
print sprintf('Fit results:   a = %.6f +- %.6f (%.2f%%)', a,a_err, (a!=0)? 100.0*a_err/abs(a) : 0/0 )
print sprintf('               b = %.6f +- %.6f (%.2f%%)', b,b_err, (b!=0)? 100.0*b_err/abs(b) : 0/0 )
print sprintf('Goodness:      R^2 = %.6f, r = %.6f,  N=%d', R2, r, Y_records)
print sprintf('Analysis:      xA = 1/a = %.6f +- %.6f', 1/a, (a_err!=0)?100.0*(a_err/a)/abs(1/a):0/0)
# print sprintf('================================ Test value =================================')
# print sprintf('Test value:    x_test = %.6f +- %.6f', x_test, dx_test)
# print sprintf('Estimated:     y(%.6f) = %.6f +- %.6f (%.2f%%)', x_test, y_esti, dy_esti, (y_esti!=0)?100.0*dy_esti/abs(y_esti):0/0)
print sprintf('==================================== END ====================================')

set out