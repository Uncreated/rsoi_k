@echo off
cd ..
:start
@echo on
flask\Scripts\python %1
pause
@echo off
goto start