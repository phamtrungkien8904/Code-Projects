
reset
set encoding utf8 

# ============================ Plot Settings ============================
set terminal epslatex color
set out 'tv6.tex'

set title 'Lineare Regression $1/b^2$ gegen $t$'
set xlabel '$t$ (s)'
set ylabel '$1/b^2$ ($\mathrm{mm}^2$)'
set datafile separator ','
set samples 10000



f(x) = A*x + B

# Fit with provided uncertainties: x errors approx from dt (assume 0.5 s), y errors from column 5
dt = 0.5
set fit quiet
fit f(x) 'data.csv' using 1:4:(dt):5 xyerrors via A,B

# 1σ parameter band (linear propagation, ignoring covariance):
up(x)   = (A + A_err)*x + (B + B_err)
down(x) = (A - A_err)*x + (B - B_err)


# Styling
set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 pt 7 ps 1 lc rgb 'blue'
set style line 3 lt 1 lw 1.5 lc rgb '#1f77b4' dashtype 2
set style line 4 lt 1 lw 1.5 lc rgb '#1f77b4' dashtype 2


# Plot
plot \
	'data.csv' using 1:4:(dt):5 with xyerrorbars ls 2 title 'Messdaten', \
	f(x) with lines ls 1 title 'Fitgerade', \
	up(x) with lines ls 3 title 'Oberes Band', \
	down(x) with lines ls 4 title 'Unteres Band'


# Print Fit results
print sprintf('============================ OUTPUT 1/b^2 = A*t + B =============================')
print sprintf('Datafile:           %s', 'data.csv')
print sprintf('Fit results:        A = %.6g +- %.3g (%.2f%%)  [mm^2/s]', A,A_err, (A!=0)? 100.0*A_err/abs(A) : 0/0 )
print sprintf('                    B = %.6g +- %.3g (%.2f%%)  [mm^2]',   B,B_err, (B!=0)? 100.0*B_err/abs(B) : 0/0 )

# Derived parameter a = A/4 (same units as A: mm^2/s); σ_a = σ_A / 4
a = A/4.0
a_err = A_err/4.0
print sprintf('Derived:            a = A/4 = %.6g +- %.3g (%.2f%%)  [mm^2/s]', a, a_err, (a!=0)? 100.0*a_err/abs(a) : 0/0 )

stats 'data.csv' using 4 name 'Y' nooutput
stats 'data.csv' using (f($1) - $4) name 'RES' nooutput
SST = (Y_records>1)? (Y_records-1)*Y_stddev**2 : 0
SSE = RES_sumsq
R2 = (SST>0)? 1 - SSE/SST : 0/0
R2 = (R2>1)?1:((R2<0)?0:R2)
print sprintf('Goodness:           R^2 = %.5f (N=%d)', R2, Y_records)
print sprintf('========================================= END ==========================================')

set out