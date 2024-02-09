@echo off
setlocal
set script_path=E:\PAPPER\PROCESS\GprMax\gpr_in\generate.py
set /a count=0
:loop
if %count% == 60 goto :end
echo generate B-scan figure for %count% times...
python "%script_path%" 1 2
set /a count+=1
cls
goto :loop
:end
echo finish the task, have generated %count% figures...
endlocal