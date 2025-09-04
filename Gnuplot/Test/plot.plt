################ Fourier-Series of a Square Wave ################
set samples 10000
f(x,N) = (4/pi) * sum [n=1:N] (sin((2*n-1)*x)/(2*n-1))

plot f(x, 2) title 'Fourier Series (N=2)',\
     f(x, 5) title 'Fourier Series (N=5)',\
     f(x, 10) title 'Fourier Series (N=10)',\
     f(x, 50) title 'Fourier Series (N=50)'

################ End of Fourier-Series of a Square Wave ################
