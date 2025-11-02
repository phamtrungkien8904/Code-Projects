@echo off
REM === Change to your project directory ===
cd /d "C:\Users\lugwi\Desktop\Github\Code-Projects\Gnuplot\Kersting\Day1"

REM === Run the Python script ===
echo Running FFT Python script...
python fft.py

REM === Run Gnuplot scripts ===
echo Running Gnuplot scripts...
gnuplot runall.plt

echo All tasks completed.

