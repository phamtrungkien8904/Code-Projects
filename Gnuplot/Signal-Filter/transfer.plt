reset
set encoding utf8 

# ============================ Plot Settings ============================

set title 'Betrag der Übertragungsfunktion'
set xlabel 'f/f0'
set ylabel '|H(f)|'
set xrange [0:2]
set yrange [0:1.5]
set sample 10000
# set grid


set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'

tau_C = 2.0  # Capacitor time constant
tau_L = 0.5  # Inductance time constant
f1 = 1/(2*pi*sqrt(tau_C))  # Grenzfrequenz der RC-Schaltung
f2 = 1/(2*pi*sqrt(tau_L * tau_C))  # Grenzfrequenz der RLC-Schaltung
# Betrag der Übertragungsfunktion
# RC-Tiefpass (1. Ordnung)
f1(x) = 1/sqrt(1 + (2*pi*x*f1*tau_C)**2)

# RLC-Tiefpass (2. Ordnung)
f2(x) = 1/sqrt((1-tau_C*tau_L*(2*pi*x*f2)**2)**2 + (2*pi*x*f2*tau_C)**2)

plot f1(x) with lines linestyle 1 notitle, \
     f2(x) with lines linestyle 2 notitle