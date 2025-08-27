reset

# ============================ Plot Settings ============================
set terminal epslatex color
set out 'tv2-1.tex'

set title 'RC-Tiefpass: Betrag der Übertragungsfunktion'
set xlabel 'Frequenz $f$ (Hz)'
set ylabel '$|G| = U_{out}/U_{in}$'
# set grid
set datafile separator ','

# ---------------- Measurement (instrument) uncertainties ----------------
X_ERR = 5.0 
Y_ERR  = 0.01    # absolute voltage uncertainty (V) before normalization
U_IN   = 4.5     # Input voltage for normalization (V)
Y_ERR_N = Y_ERR / U_IN

# Linear Regression Fit
f(x) = a/sqrt(1+(x/b)**2)   # fit on normalized data

set fit quiet
fit f(x) 'data2-1.csv' using 1:($2/U_IN):(Y_ERR_N) yerrors via a,b 
# only 2 Error when linear fit

x0 = 1600
# Theoretical Model
f_theory(x) = 1/sqrt(1+(x/x0)**2)   # example theoretical model

# # Compute R^2 and correlation r (unweighted)
# stats 'data2-1.csv' using ($2/U_IN) name 'Y' nooutput
# SST = (Y_records > 1) ? (Y_records - 1) * Y_stddev**2 : 0
# stats 'data2-1.csv' using (f($1)-($2/U_IN)) name 'E' nooutput
# SSE = E_sumsq
# R2 = (SST > 0) ? (1.0 - SSE / SST) : 0/0
# R2 = (R2 > 1) ? 1 : ((R2 < 0) ? 0 : R2)
# r  = (R2 >= 0) ? sqrt(R2) : 0/0

# Styling
set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 pt 7 ps 1 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'green'


# Plot
plot \
	'data2-1.csv' using 1:($2/U_IN):(X_ERR):(Y_ERR_N) with xyerrorbars ls 2 title 'Messdaten (norm.)', \
	f(x) with lines ls 1 title 'Fitkurve', \
	f_theory(x) with lines ls 3 title 'Theoretisches Modell'



# Print Fit results
print sprintf('============================ OUTPUT f(x) = a/sqrt(1+(x/b)**2) =============================')
print sprintf('Datafile:           %s', 'data2-1.csv')
print sprintf('Uncertainties:      df = %.3f, dU = %.3f V  (normalized d(U/U_in)=%.4f)', X_ERR, Y_ERR, Y_ERR_N)
print sprintf('Fit results:        a = %.6f +- %.6f (%.2f%%)', a,a_err, (a!=0)? 100.0*a_err/abs(a) : 0/0 )
print sprintf('                    b = %.6f +- %.6f (%.2f%%)', b,b_err, (b!=0)? 100.0*b_err/abs(b) : 0/0 )
print sprintf('Theoretical Model:  x0 = 1.59 +- 0.16 (kHz)', x0)
# print sprintf('Goodness:      R^2 = %.6f, r = %.6f,  N=%d', R2, r, Y_records)
print sprintf('============================================END ===========================================')

set out