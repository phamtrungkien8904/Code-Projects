reset
set encoding utf8 

# ============================ Plot Settings ============================

set terminal epslatex color
set out 'tv1-zelle.tex'

set title 'Belastungskurve der Galvanischen Zelle'
set ylabel 'Klemmenspannung $U$/V'
set xlabel 'Belastungsstrom $I$/mA'
# set grid
set datafile separator ','
set samples 10000

# ---------------- Measurement (instrument) uncertainties ----------------
X_ERR = 0.1 
Y_ERR  = 0.1  

# Linear Regression Fit
f(x) = a*x+b

set fit quiet
fit f(x) 'data-zelle.csv' using 2:1:4:3 xyerrors via a,b 
# only 2 Error when linear fit

# Error Bandbound
up(x)   = (a+a_err)*x + (b+b_err)
down(x) = (a-a_err)*x + (b-b_err)

# Compute R^2 on dependent variable (col 1 = U) and adjusted R^2; unweighted residuals
stats 'data-zelle.csv' using 1 name 'DEP' nooutput
SST = (DEP_records > 1) ? (DEP_records - 1) * DEP_stddev**2 : 0
stats 'data-zelle.csv' using (f($2) - $1) name 'E' nooutput
SSE = E_sumsq
R2 = (SST > 0) ? (1.0 - SSE / SST) : 0/0
R2 = (R2 > 1) ? 1 : ((R2 < 0) ? 0 : R2)
# adjusted R^2 for linear model with intercept (p = 1 predictor)
p = 1
R2_adj = (DEP_records > p + 1) ? 1 - (1 - R2) * (DEP_records - 1) / (DEP_records - p - 1) : 0/0
# signed correlation coefficient using slope sign
sgn = (a >= 0) ? 1 : -1
r  = (R2 >= 0) ? sgn * sqrt(R2) : 0/0

# Styling
set style line 1 lt 1 lw 2 lc rgb '#d62728'
set style line 2 pt 7 ps 1 lc rgb '#111111'
set style line 3 lt 1 lw 2 lc rgb '#1f77b4' dashtype 2  # upper dashed
set style line 4 lt 1 lw 2 lc rgb '#1f77b4' dashtype 2  # lower dashed

# Plot
plot \
	'data-zelle.csv' using 2:1:4:3 with xyerrorbars ls 2 title 'Messdaten', \
	f(x) with lines ls 1 title 'Fitgerade',\
	up(x) with lines ls 3 title 'Oberes Band', \
	down(x) with lines ls 4 title 'Unteres Band'

###### Test value x ######
x_test = 5
dx_test = 0.1
y_esti = f(x_test)
dy_esti = a_err * x_test + b_err + a*dx_test

# Print Fit results
print sprintf('============================ OUTPUT y = a*x + b =============================')
print sprintf('Datafile:      %s', 'data-zelle.csv')
print sprintf('Fit results:   a = %.6f +- %.6f (%.2f%%)', a,a_err, (a!=0)? 100.0*a_err/abs(a) : 0/0 )
print sprintf('               b = %.6f +- %.6f (%.2f%%)', b,b_err, (b!=0)? 100.0*b_err/abs(b) : 0/0 )
print sprintf('Goodness:      R^2 = %.6f, r = %.6f,  N=%d', R2, r, DEP_records)
print sprintf('==================================== END ====================================')


set out