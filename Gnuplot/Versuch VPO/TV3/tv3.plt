reset

# ============================ Plot Settings ============================
# set terminal epslatex color
# set out 'tv3.tex'

set title 'RLC-Resonanzkurve'
set xlabel 'Frequenz f (Hz)'
set ylabel 'U_out/U_max'
set datafile separator ','

# ---------------- Measurement (instrument) uncertainties ----------------
X_ERR = 5.0              # Hz (adjust if known better)
Y_ERR  = 10.0            # mV absolute uncertainty of U_out

# Determine peak output automatically so model (whose max=1) can fit.
stats 'data3.csv' using 2 name 'D' nooutput
U_MAX = D_max            # mV peak measured output
Y_ERR_N = Y_ERR / U_MAX  # normalized y uncertainty


# Theoretical Model
R = 340
L = 0.12
dL = 0.0028
C = 10**(-8)
x0 = 1/(2*pi*sqrt(L*C))

# Linear Regression Fit
f(x) = 1/sqrt(1+(a/x*(x**2 - b**2))**2)

# Initial parameter guesses (adjust if fit still poor)
a = 0.0017    # width-related parameter (roughly ~1/(2*FWHM))
b = 4400      # peak frequency guess (Hz)

set fit quiet
fit f(x) 'data3.csv' using 1:($2/U_MAX) via a,b
# only 2 Error when linear fit



f_theory(x) = 1/sqrt(1+(2*pi*L/R/x*(x**2 - x0**2))**2)
# # Compute R^2 and correlation r (unweighted)
# stats 'data3.csv' using ($2/U_IN) name 'Y' nooutput
# SST = (Y_records > 1) ? (Y_records - 1) * Y_stddev**2 : 0
# stats 'data3.csv' using (f($1)-($2/U_IN)) name 'E' nooutput
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
	'data3.csv' using 1:($2/U_MAX):(X_ERR):(Y_ERR_N) with xyerrorbars ls 2 title 'Messdaten (norm.)', \
	f(x) with lines ls 1 title 'Fitkurve', \
	f_theory(x) with lines ls 3 title 'Theoriekurve'



# Print Fit results
print sprintf('============================ OUTPUT f(x) = 1/sqrt(1+(a/x*(x**2 - b**2))**2) =============================')
print sprintf('Datafile:           %s', 'data3.csv')
print sprintf('Normalization:      U_MAX = %.1f mV (peak output)', U_MAX)
print sprintf('Uncertainties:      dF = %.2f Hz, dU = %.1f mV  (normalized d(U/U_max)=%.4f)', X_ERR, Y_ERR, Y_ERR_N)
print sprintf('Fit results:        a = %.6f +- %.6f (%.2f%%)', a,a_err, (a!=0)? 100.0*a_err/abs(a) : 0/0 )
print sprintf('                    b = %.6f +- %.6f (%.2f%%)', b,b_err, (b!=0)? 100.0*b_err/abs(b) : 0/0 )
## Derived resonance metrics from model f(x)=1/sqrt(1+(a/x (x^2-b^2))^2)
# Half-power ( -3 dB ) points solve (a/x (x^2 - b^2))^2 = 1 -> a(x^2-b^2) = ± x
D  = 1 + 4*(a*b)**2
f1 = (-1 + sqrt(D)) / (2*a)
f2 = ( 1 + sqrt(D)) / (2*a)
BW = f2 - f1          # = 1/a
Qcalc = b / BW        # = a*b
# Series resistance estimate using both equivalent formulas for a series RLC (should match if model physically valid)
R_est = 2*pi*b*L / Qcalc
## Uncertainty propagation
Q_err = sqrt( (b*a_err)**2 + (a*b_err)**2 )
# R_est = 2*pi*L*(b/Q) = 2*pi*L*(1/a)  (since Q=a*b) -> dR from a & L only
R_est_err = 2*pi*sqrt( (L * (-1/a**2) * a_err)**2 + ((1/a) * dL)**2 )
print sprintf('Data Analysis:      f1 = %.2f Hz, f2 = %.2f Hz  (BW = %.2f Hz)', f1, f2, BW)
print sprintf('                    Q = b/BW = %.3f +- %.3f', Qcalc, Q_err)
print sprintf('                    R_est = (w0 L / Q) = %.2f +- %.2f Ohm', R_est, R_est_err)
print sprintf('Theoretical Model:  f_0 = 4.6 +- 0.5 (kHz)')
# print sprintf('Goodness:      R^2 = %.6f, r = %.6f,  N=%d', R2, r, Y_records)
print sprintf('=================================================== END ==================================================')

# set out