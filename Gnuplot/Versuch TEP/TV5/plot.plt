reset
set datafile separator ','

# Physical constants / geometry (ensure units consistent: SI)
rho = 1000.0                 # kg/m^3 (water)
g   = 9.81                   # m/s^2
V0  = 1105.3                  # cm^3
dV0 = 0.13                    # cm^3
h   = 20.5                    # cm
dh  = 0.05                    # cm
d   = 1.7                     # cm
dd  = 0.05                    # cm
V   = (V0 + pi*h*d**2/4)*1e-6   # m^3
p   = 716*133.322            # Pa (716 Torr -> Pa)
dp  = 0.1*133.322            # Pa
A   = (pi*d**2/4)*1e-4   # m^2

# Data files
DATA_T0 = 'data1.csv'   # Ohne Kolben
DATA_Tk = 'data2.csv'   # Mit Kolben

# Extract periods (second column / first column)
stats DATA_T0 using ($2/$1) name 'T0s' nooutput
stats DATA_Tk using ($2/$1) name 'Tks' nooutput

T0      = T0s_mean
Tk      = Tks_mean
T0_sd   = T0s_stddev
Tk_sd   = Tks_stddev
T0_sem  = (T0s_records>0)? T0_sd/sqrt(T0s_records) : 0/0
Tk_sem  = (Tks_records>0)? Tk_sd/sqrt(Tks_records) : 0/0

# Damped (?) gamma formula (assumes small damping):
# gamma = K * (T0^2/Tk^2 - 1)
K = 2*rho*g*V/p/A
ratio = T0**2/Tk**2 - 1
gamma = K * ratio
gamma_theo = (5.0+2.0)/5.0

# Propagate uncertainty (neglect covariance):
dR_dT0 = 2*T0 / (Tk**2)
dR_dTk = -2*T0**2 / (Tk**3)
ratio_var = (dR_dT0*T0_sd)**2 + (dR_dTk*Tk_sd)**2
gamma_sd = K*sqrt(ratio_var)
gamma_rel_pct = (gamma!=0)? 100*gamma_sd/abs(gamma) : 0/0

print '================== Period Analysis =================='
print sprintf('File T0 (no piston): %s  N=%d', DATA_T0, T0s_records)
print sprintf('T0 = %.6f s  SD=%.6f  SEM=%.6f', T0, T0_sd, T0_sem)
print sprintf('File Tk (with piston): %s  N=%d', DATA_Tk, Tks_records)
print sprintf('Tk = %.6f s  SD=%.6f  SEM=%.6f', Tk, Tk_sd, Tk_sem)
print '----------------- Gamma Result ----------------------'
print sprintf('K constant = %.6f', K)
print sprintf('ratio = T0^2/Tk^2 - 1 = %.6f', ratio)
print sprintf('gamma = %.6f +- %.6f  (%.2f%%)', gamma, gamma_sd, gamma_rel_pct)
print sprintf('gamma_theo = %.6f  (difference = %.6f)', gamma_theo, gamma - gamma_theo)
print '====================================================='