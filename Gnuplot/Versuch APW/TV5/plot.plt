#### Stefan-Boltzmann ###
reset
set encoding utf8 

# ============================ Plot Settings ============================
set terminal epslatex color
set out 'tv5.tex'

set title 'Stefan-Boltzmann (Lineare Regression)'
set xlabel '$T^4 - T_0^4$ ($10^{11} \ \mathrm{K}^4$)'
set ylabel '$V$ (mV)'
set datafile separator ','
set samples 10000

# ---------------- Measurement (instrument) uncertainties ----------------
TK = 273.15        # Celsius to Kelvin shift
T0 = 26.0 + TK      # Ambient reference temperature (26°C example; adjust if needed)
DT0 = 1.9           # Uncertainty of T0 (K)

# Measurement uncertainties (adjust to your instrument specs)
dT = 0.5            # K (converted from °C sensor uncertainty)
dV_rel = 0.04/100.0 # 0.04% of reading
dV_abs = 0.002      # 2 digits -> 0.002 mV assuming 0.001 mV resolution

# Derived abscissa: x = (T^4 - T0^4)
# Propagate uncertainties from T (each point) and T0 (reference):
#   dx/dT  = 4 T^3
#   dx/dT0 = -4 T0^3
#   σ_x = sqrt( (4 T^3 σ_T)^2 + (4 T0^3 σ_T0)^2 )
# Voltage uncertainty: σ_V = sqrt( (dV_rel * V)^2 + dV_abs^2 )

# Helper functions (argument in °C for temperature column):
Xval(tc) = ((tc+TK)**4 - (T0)**4)
Dx(tc)  = sqrt( (4*(tc+TK)**3 * dT)**2 + (4*(T0)**3 * DT0)**2 )
Dy(v)   = sqrt( (dV_rel*v)**2 + (dV_abs)**2 )

f(x) = A*x + B

set fit quiet
fit f(x) 'data.csv' using (Xval($1)/1e11):( $2 ):( Dx($1) ):( Dy($2) ) xyerrors via A,B

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
	'data.csv' using (Xval($1)/1e11):( $2 ):( Dx($1) ):( Dy($2) ) with xyerrorbars ls 2 title 'Messdaten', \
	f(x) with lines ls 1 title 'Fitgerade', \
	up(x) with lines ls 3 title 'Fehlerstreifen (obere Grenze)', \
	down(x) with lines ls 4 title 'Fehlerstreifen (untere Grenze)'


# Print Fit results
print sprintf('============================ OUTPUT V = A*(T^4 - T0^4) + B =============================')
print sprintf('Datafile:           %s', 'data.csv')
print sprintf('Fit results:        A = %.6g +- %.3g (%.2f%%)', A,A_err, (A!=0)? 100.0*A_err/abs(A) : 0/0 )
print sprintf('                    B = %.6g +- %.3g (%.2f%%)', B,B_err, (B!=0)? 100.0*B_err/abs(B) : 0/0 )
print sprintf('Uncertainties:      dT=%.2f K, dT0=%.2f K, rel dV=%.4f, abs dV=%.4f mV', dT, DT0, dV_rel, dV_abs)

# Goodness-of-fit metrics
# Unweighted R^2 based on variance of V
stats 'data.csv' using 2 name 'Y' nooutput
stats 'data.csv' using (f(Xval($1)) - $2) name 'RES' nooutput
SST = (Y_records>1)? (Y_records-1)*Y_stddev**2 : 0
SSE = RES_sumsq
R2 = (SST>0)? 1 - SSE/SST : 0/0
R2 = (R2>1)?1:((R2<0)?0:R2)


print sprintf('Goodness:           R^2 = %.5f (N=%d)', R2, Y_records)
print sprintf('========================================= END ==========================================')

set out