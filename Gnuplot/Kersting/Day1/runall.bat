@echo off
REM === Change to your project directory ===
cd /d "C:\Users\lugwi\Desktop\Github\Code-Projects\Gnuplot\Kersting\Day1"

REM === Run the Python script ===
echo Running FFT Python script...
python fft.py

REM === Run Gnuplot scripts ===
echo Running Gnuplot scripts...
gnuplot -p plot-signal.plt
gnuplot -p plot-fft.plt
gnuplot -p plot-bode-gain.plt
gnuplot -p plot-bode-phase.plt

echo All tasks completed.
pause
