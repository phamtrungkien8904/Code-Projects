reset
set encoding utf8 


# set terminal epslatex color
# set out 'TV11.tex' #################

# ============================ Plot Settings ============================


set title 'Grafische Bestätigung der Abbildungsgleichung'
set ylabel 'Bildweite (cm)'
set xlabel 'Gegenstandsweite (cm)'
# set grid
set xrange [0:40]
set yrange [0:120]
set datafile separator ','
set samples 10000

g1 = 29.0
b1 = 66.0
g2 = 27.3
b2 = 77.7
g3 = 26.0
b3 = 89.0
g4 = 25.3
b4 = 99.7
g5 = 25.0
b5 = 105.0
# g6 = 66.2
# b6 = 28.8
# g7 = 78.1
# b7 = 26.9
# g8 = 89.2
# b8 = 25.8
# g9 = 99.8
# b9 = 25.2
# g10 = 105.0
# b10 = 25.0


y1(x) = -b1/g1*x + b1
y2(x) = -b2/g2*x + b2
y3(x) = -b3/g3*x + b3
y4(x) = -b4/g4*x + b4
y5(x) = -b5/g5*x + b5
# y6(x) = -b6/g6*x + b6
# y7(x) = -b7/g7*x + b7
# y8(x) = -b8/g8*x + b8
# y9(x) = -b9/g9*x + b9
# y10(x) = -b10/g10*x + b10

# # Schnittpunktbereich (aus Paar-Schnittpunkten der Geraden y1..y5)
# f_x_min = 19.5867
# f_x_max = 20.6710
# f_y_min = 18.2417
# f_y_max = 21.9533
# f_x_mean = 20.2632
# f_y_mean = 19.8135

# set style rect back fc rgb 'gray70' fs transparent solid 0.12 border lc rgb 'black' dt 2 lw 1.5
# set object 1 rect from f_x_min,f_y_min to f_x_max,f_y_max
# print sprintf('f_x in [%.2f, %.2f] cm', f_x_min, f_x_max) 
# print sprintf('f_y in [%.2f, %.2f] cm', f_y_min, f_y_max) 


# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' 
set style line 2 lw 1.5 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 1.5 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 1.5 pt 4 lc rgb 'red' 
set style line 5 lw 1.5 pt 4 lc rgb 'orange'




# Plot
plot \
    y1(x) with lines ls 4 notitle, \
    y2(x) with lines ls 4 notitle, \
    y3(x) with lines ls 4 notitle, \
    y4(x) with lines ls 4 notitle, \
    y5(x) with lines ls 4 notitle
    # y6(x) with lines ls 5 notitle, \
    # y7(x) with lines ls 5 notitle, \
    # y8(x) with lines ls 5 notitle, \
    # y9(x) with lines ls 5 notitle, \
    # y10(x) with lines ls 5 notitle


# set out