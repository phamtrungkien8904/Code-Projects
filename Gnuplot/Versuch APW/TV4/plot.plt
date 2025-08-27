#### Clayperon-Clausius ###
reset

# ============================ Plot Settings ============================
# set terminal epslatex color
# set out 'tv3.tex'

set title 'Dampfdruckkurve'
set xlabel 'T (Grad)'
set ylabel 'p (bar)'
set datafile separator ','

# ---------------- Measurement (instrument) uncertainties ----------------
X_ERR = 0.1          # °C uncertainty in temperature
Y_ERR = 1          # bar uncertainty in pressure

T0 = 273.2

# Linear Regression Fit
f(x) = a*exp(-b*(1/x))
# Initial parameter guesses (adjust if fit still poor)
a = 30
b = 0.4



set fit quiet
fit f(x) 'data.csv' using ($1+T0):2:(X_ERR):(Y_ERR) xyerrors via a,b
# only 2 Error when linear fit



# Styling
set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 pt 7 ps 1 lc rgb 'blue'


# Plot
plot \
	'data.csv' using ($1+T0):2:(X_ERR):(Y_ERR) with xyerrorbars ls 2 title 'Messdaten', \
	f(x) with lines ls 1 title 'Fitkurve'


# Print Fit results
print sprintf('============================ OUTPUT f(x) = a*exp(b*x) =============================')
print sprintf('Datafile:           %s', 'data.csv')
print sprintf('Uncertainties:      dT = %.1f Grad, dp = %.0f bar', X_ERR, Y_ERR)
print sprintf('Fit results:        a = %.6g +- %.3g (%.2f%%)', a,a_err, (a!=0)? 100.0*a_err/abs(a) : 0/0 )
print sprintf('                    b = %.6g +- %.3g (%.2f%%)', b,b_err, (b!=0)? 100.0*b_err/abs(b) : 0/0 )

# Goodness of fit (R^2)
stats 'data.csv' using 2 name 'P' nooutput
SST = (P_records>1)? (P_records-1)*P_stddev**2 : 0
stats 'data.csv' using ((f($1+T0))-$2) name 'RES' nooutput
SSE = RES_sumsq
R2 = (SST>0)? 1 - SSE/SST : 0/0
R2 = (R2>1)?1:((R2<0)?0:R2)
print sprintf('Goodness:           R^2 = %.5f  (N=%d)', R2, P_records)
# print sprintf('Goodness:      R^2 = %.6f, r = %.6f,  N=%d', R2, r, Y_records)
print sprintf('======================================= END ========================================')

# set out