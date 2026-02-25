reset
set encoding utf8 


# set terminal epslatex color
# set out 'aufgabe.tex' #################

# ============================ Plot Settings ============================


set title 'Plot'
set ylabel 'y'
set xlabel 'x'
# set grid
set xrange [0:10]
set yrange [0:1.5]
set datafile separator ','
set samples 10000

f(x) = (sin(x-5)/(x-5))**2



# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' 
set style line 2 lw 1.5 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 1.5 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 1.5 pt 4 lc rgb 'red' 
set style line 5 lw 1.5 pt 4 lc rgb 'orange'




# Plot
plot f(x) with lines ls 4 title 'f(x) = (sin(x-5)/(x-5))^2' 



# set out