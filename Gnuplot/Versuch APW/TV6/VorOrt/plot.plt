set decimalsign locale
set datafile separator ';'

s=180/108;

f(x) = (t2-t1)/2*erf((x-x0)*b)+(t1+t2)/2;
fit f(x) '7.csv' using ($1*s):3 every ::2 via t1,t2,x0,b


plot '7.csv' using 1:3 every ::2 title 'Messwerte';
plot '7.csv' using ($1*s):3 every ::2 title 'Messwerte', f(x) title 'Fit'


set xlabel 'Länge [mm]'
set ylabel 'Temperatur [°C]'

