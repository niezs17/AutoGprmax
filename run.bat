@echo off

cls
setlocal

set CONDA_PATH=C:\Users\NIEZS\miniconda3
set CONDA_ENV=gprMax
set script_path=E:\PAPPER\PROCESS\GprMax\gpr_in\generate.py
set /a count=0
set /a air_num = %1
set /a water_num = %2
set /a times=%3

CALL %CONDA_PATH%\Scripts\activate.bat %CONDA_PATH%
CALL conda activate %CONDA_ENV%

echo **************************************************************
echo conda path: %CONDA_PATH%
echo conda env : %CONDA_ENV%
echo script path: %script_path%
echo Bscan figure: air num = %air_num% water num = %water_num% times = %times%
echo **************************************************************

set /p user_input="start to generate? (y/n): "
if /I "%user_input%"=="y" (
goto loop
)
(
goto end
)	

:loop
if %count% == %times% goto :end
python "%script_path%" %air_num% %water_num%
set /a count+=1
cls
goto :loop

:end
echo task end...have generated %count% figures...
endlocal

