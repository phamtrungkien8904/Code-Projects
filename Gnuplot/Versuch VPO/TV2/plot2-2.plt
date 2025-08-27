reset

# ============================ Plot & Fit: Phase from Time Shift ============================
# Data file: data2-2.csv with columns: f_Hz  t_us
# We fit y = 2*pi*f*t  (phase in radians) to model: y = a - atan(f/b)
# => a (rad) approximates asymptotic phase at low f + offset; b (Hz) is characteristic frequency.

set terminal epslatex color
set out 'tv2-2.tex'

set title 'RC-Hochpass: Phase aus Zeitverschiebung'
set xlabel 'Frequenz $f$ (Hz)'
set ylabel 'Phase $\varphi = 2\pi f t$ (rad)'
set datafile separator whitespace

# Optional: show also phase in degrees on second axis
deg(x) = x*180.0/pi
set y2tics
set format y2 '%.0f°'
set link y2 via deg(y) inverse y*pi/180.0
set y2label 'Phase $\varphi (^\circ)$'
set yrange [0:1.7]

# Parameters initial guesses
a = 1.5   # ~ low-frequency limit guess (rad)
b = 1000  # characteristic frequency (Hz)

# Model
phase_model(x) = a - atan(x/b)

# Data transformation: phase from time delay t (microseconds)
phase_from_time(f_hz, t_us) = 2*pi*f_hz*(t_us*1e-6)

set fit quiet
fit phase_model(x) 'data2-2.csv' using 1:(phase_from_time($1,$2)) via a,b

# Theoretical phase response
x0 = 1600
phase_theo(x) = pi/2 - atan(x/x0)

# Styling
set style line 1 lt 1 lw 2 lc rgb '#d62728'
set style line 2 pt 7 ps 1.1 lc rgb '#1f77b4'
set style line 3 lt 1 lw 2 lc rgb '#2ca02c'
# Plot
plot \
	'data2-2.csv' using 1:(phase_from_time($1,$2)) with points ls 2 title 'Messdaten', \
	phase_model(x) with lines ls 1 title 'Fit: $a - \arctan(f/b)$', \
	phase_theo(x) with lines ls 3 title 'Theorie: $\pi/2 - \arctan(f/f_g)$'

# Output fit results
print sprintf('================ Fit: y = a - atan(f/b), y = 2*pi*f*t (rad) ===============')
print sprintf('Data file: data2-2.csv')
print sprintf('Results: a = %.6f +/- %.6f rad (%.2f deg)', a, a_err, deg(a))
print sprintf('         b = %.6f +/- %.6f Hz', b, b_err)
print sprintf('Theoretical characteristic frequency f_g = %.2f Hz', x0)
print sprintf('==========================================================================')

set out