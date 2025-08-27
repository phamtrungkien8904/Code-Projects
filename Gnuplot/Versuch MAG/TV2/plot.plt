reset

# ============================ Plot Settings ============================

set title 'Title'
set xlabel 'x()'
set ylabel 'y()'
# set grid
set datafile separator ','

# ---------------- Measurement (instrument) uncertainties ----------------
X_ERR = 2 
Y_ERR  = 0.1  

# Linear Regression Fit
f(x) = a*x+b

set fit quiet
fit f(x) 'data.csv' using 1:2:(X_ERR):(Y_ERR) xyerrors via a,b 
# only 2 Error when linear fit

# Error Bandbound
up(x)   = (a+a_err)*x + (b+b_err)
down(x) = (a-a_err)*x + (b-b_err)

# Compute R^2 and correlation r (unweighted)
stats 'data.csv' using 2 name 'Y' nooutput
SST = (Y_records > 1) ? (Y_records - 1) * Y_stddev**2 : 0
stats 'data.csv' using (f($1)-$2) name 'E' nooutput
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
	'data.csv' using 1:2:(X_ERR):(Y_ERR) with xyerrorbars ls 2 title 'Data', \
	f(x) with lines ls 1 title 'Fit',\
	up(x) with lines ls 3 notitle, \
	down(x) with lines ls 4 notitle

###### Test value x ######
x_test = 5
dx_test = 0.1
y_esti = f(x_test)
dy_esti = a_err * x_test + b_err + a*dx_test

# Print Fit results
print sprintf('============================ OUTPUT y = a*x + b =============================')
print sprintf('Datafile:      %s', 'data.csv')
print sprintf('Uncertainties: dx = %.3f, dy = %.3f', X_ERR, Y_ERR)
print sprintf('Fit results:   a = %.6f +- %.6f (%.2f%%)', a,a_err, (a!=0)? 100.0*a_err/abs(a) : 0/0 )
print sprintf('               b = %.6f +- %.6f (%.2f%%)', b,b_err, (b!=0)? 100.0*b_err/abs(b) : 0/0 )
print sprintf('Goodness:      R^2 = %.6f, r = %.6f,  N=%d', R2, r, Y_records)
print sprintf('================================ Test value =================================')
print sprintf('Test value:    x_test = %.6f +- %.6f', x_test, dx_test)
print sprintf('Estimated:     y(%.6f) = %.6f +- %.6f (%.2f%%)', x_test, y_esti, dy_esti, (y_esti!=0)?100.0*dy_esti/abs(y_esti):0/0)
print sprintf('==================================== END ====================================')