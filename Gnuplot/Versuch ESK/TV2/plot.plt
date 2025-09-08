reset
set encoding utf8 

# ============================ Plot Settings ============================

set terminal epslatex color
set out 'tv2.tex'

set title '$I/U$-Diagramm eines Wiederstandes'
set ylabel 'Spannung $U$/V'
set xlabel 'Strom $I$/mA'
# set grid
set datafile separator ','
set samples 10000

# ---------------- Measurement (instrument) uncertainties ----------------
X_ERR = 0.1 
Y_ERR  = 0.1  

# Linear Regression Fit
f(x) = a*x+b

set fit quiet
fit f(x) 'data.csv' using 2:1:4:3 xyerrors via a,b 
# only 2 Error when linear fit



# Compute R^2 on dependent variable (col 1 = U) and adjusted R^2; unweighted residuals
stats 'data.csv' using 1 name 'DEP' nooutput
SST = (DEP_records > 1) ? (DEP_records - 1) * DEP_stddev**2 : 0
stats 'data.csv' using (f($2) - $1) name 'E' nooutput
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


# Plot
plot \
	'data.csv' using 2:1:4:3 with xyerrorbars ls 2 title 'Messdaten', \
	f(x) with lines ls 1 title 'Fitgerade'


# Print Fit results
print sprintf('============================ OUTPUT y = a*x + b =============================')
print sprintf('Datafile:      %s', 'data.csv')
print sprintf('Fit results:   a = %.6f +- %.6f (%.2f%%)', a,a_err, (a!=0)? 100.0*a_err/abs(a) : 0/0 )
print sprintf('               b = %.6f +- %.6f (%.2f%%)', b,b_err, (b!=0)? 100.0*b_err/abs(b) : 0/0 )
print sprintf('Goodness:      R^2 = %.6f, r = %.6f,  N=%d', R2, r, DEP_records)
print sprintf('==================================== END ====================================')


set out