@echo off

cls
setlocal

REM  Here is the part you need to modify !!!

REM Set the path to your CUDA installation
set CONDA_PATH=[YOUR_CUDA_PATH]
REM Set the name of your GprMax conda environment
set CONDA_ENV=[YOUR_GPRMAX_ENVIRONMENT_NAME]
REM Set the path to the dataset generation script
set script_path=[./generate.py]
REM Set the number of air-filled cavities
set /a air_num=[NUMBER_OF_AIR_FILLED_CAVITIES]
REM Set the number of water-filled cavities
set /a water_num=[NUMBER_OF_WATER_FILLED_CAVITIES]
REM Set the number of scans
set /a times=[NUMBER_OF_SCANS]

REM  Here is the part you usually no need to modify !!!
set /a count=0
CALL %CONDA_PATH%\Scripts\activate.bat %CONDA_PATH%
CALL conda activate %CONDA_ENV%

echo **************************************************************
echo conda path: %CONDA_PATH%
echo conda env : %CONDA_ENV%
echo script path: %script_path%
echo Bscan figure: air num = %air_num% water num = %water_num% times = %times%
echo **************************************************************

:loop
if %count% == %times% goto :end
python "%script_path%" %air_num% %water_num%
set /a count+=1
cls
goto :loop