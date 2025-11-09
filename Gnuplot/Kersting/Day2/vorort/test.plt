set datafile separator ','
stats 'test.csv' using 1:(($4>=2)?$4:1/0) name 'bw' nooutput
bw_out = bw_max_x
print sprintf("Output = %.2f", bw_out)