reset
set encoding utf8 

# set terminal epslatex color
# set out 'wien.tex' 

# ============================ Plot Settings ============================

set title 'Wien Bridge'
set xlabel '$\log(f/f_0)$'
set ylabel '$H(f/f_0)$'
set logscale x 10
set xrange [10e-7:10e5]
set format x '{%L}'
set yrange [0:1]
set samples 100000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 1.5 lc rgb 'black' dt 2

# Use floating-point division (1/3 and 1/9 would be 0 with integer division)
H(x) = (1.0/3.0) / sqrt(1.0 + (1.0/9.0) * (x - 1.0/x)**2)

H13(x) = 1.0/3.0

# Label slightly above the H=1/3 reference line
set label 1 '$H=1/3$' at 1, H13(1) offset char 0,1 center


plot H(x) with lines linestyle 1 notitle, \
    H13(x) with lines linestyle 3 notitle

# set out