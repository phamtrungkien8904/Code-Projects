#### Clayperon-Clausius ###
reset
set encoding utf8 

# ============================ Plot Settings ============================
set terminal epslatex color
set out 'tv4.tex'

set title 'Clapeyron-Clausius (Lineare Regression)'
set xlabel '$-1/T$ ($\mathrm{K}^{-1}$)'
set ylabel '$\ln(p/\mathrm{bar})$'
set datafile separator ','
set samples 10000

# ---------------- Measurement (instrument) uncertainties ----------------
X_ERR = 0.1          # °C uncertainty (original T input)
Y_ERR = 1            # bar uncertainty in pressure

# Column map after expansion:
# 1: Temperature_C, 2: Pressure_bar, 3: -1/T(K), 4: ln(p/bar)

# Linear model: ln(p) = A * (-1/T) + B  (Arrhenius type)
f(x) = A*x + B

set fit quiet
fit f(x) 'data.csv' using 3:4:(X_ERR/($1+273.15)**2):(1/$2) xyerrors via A,B

# Theorie

kB = 1.380649e-23   # J/K
e = 1.602176634e-19 # C

# Styling
set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 pt 7 ps 1 lc rgb 'blue'


# Plot
plot \
	'data.csv' using 3:4:(X_ERR/($1+273.15)**2):(1/$2) with xyerrorbars ls 2 title 'Messdaten', \
	f(x) with lines ls 1 title 'Fitgerade'


# Print Fit results
print sprintf('============================ OUTPUT ln(p) = A*(-1/T) + B =============================')
print sprintf('Datafile:           %s', 'data.csv')
print sprintf('Uncertainties:      dT = %.1f Grad, dp = %.0f bar', X_ERR, Y_ERR)
print sprintf('Fit results:        A = %.6g +- %.3g (%.2f%%)', A,A_err, (A!=0)? 100.0*A_err/abs(A) : 0/0 )
print sprintf('                    B = %.6g +- %.3g (%.2f%%)', B,B_err, (B!=0)? 100.0*B_err/abs(B) : 0/0 )
print sprintf('Analysis:           E_b = %.6g +- %.3g (%.2f%%) (eV)', A*kB/e, A_err*kB/e, (A!=0)? 100.0*-A_err*kB/abs(-A*kB) : 0/0)

# Goodness of fit (R^2)
stats 'data.csv' using 4 name 'LP' nooutput
SST = (LP_records>1)? (LP_records-1)*LP_stddev**2 : 0
stats 'data.csv' using (f($3)-$4) name 'RES' nooutput
SSE = RES_sumsq
R2 = (SST>0)? 1 - SSE/SST : 0/0
R2 = (R2>1)?1:((R2<0)?0:R2)
print sprintf('Goodness:           R^2 = %.5f  (N=%d)', R2, LP_records)
# print sprintf('Goodness:      R^2 = %.6f, r = %.6f,  N=%d', R2, r, Y_records)
print sprintf('======================================== END =========================================')

set out