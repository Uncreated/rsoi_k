@echo off
cd commands
SET TIMEOUT=500
START "FRONTEND" /MAX start_module.bat frontend.py
ping 1.1.1.1 -n 1 -w %TIMEOUT% > nul
START "SESSION" /MAX start_module.bat session.py
ping 1.1.1.1 -n 1 -w %TIMEOUT% > nul
START "PURCHASE" /MAX start_module.bat purchase.py
ping 1.1.1.1 -n 1 -w %TIMEOUT% > nul
START "ITEMS" /MAX start_module.bat items.py
ping 1.1.1.1 -n 1 -w %TIMEOUT% > nul
START "PAYMENT" /MAX start_module.bat payment.py
ping 1.1.1.1 -n 1 -w %TIMEOUT% > nul
START "DELIVERY"  /MAX start_module.bat delivery.py