@echo on
c:
cd Program Files\Redis
:start
redis-server.exe
pause
goto start