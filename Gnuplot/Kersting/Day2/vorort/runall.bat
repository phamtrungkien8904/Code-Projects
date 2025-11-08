@echo off
REM === Run the Python scripts ===
echo Running FFT Python scripts...
python fft.py
python theory.py

REM === Run Gnuplot scripts ===
echo Running Gnuplot scripts...
gnuplot runall.plt 


echo All tasks completed.


