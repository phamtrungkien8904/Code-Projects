R=51
Rs=50
L=10e-6
C=1e-6

set xrange [0:1e5]
set yrange [0:1]

f(x) = sqrt((R**2 + (1/(2*pi*x*L) - (2*pi*x*C))**(-2))/((R+Rs)**2 + (1/(2*pi*x*L) - (2*pi*x*C))**(-2)))

plot f(x) with lines rgb 'red' lw 2 notitle