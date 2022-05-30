@echo off
for /f "delims=[] tokens=2" %%a in ('ping -4 -n 1 %ComputerName% ^| findstr [') do set NetworkIP=%%a
cmd /k "cd /d KmuttSearchEngine\env\Scripts & activate & cd /d .. & cd /d .. & python manage.py runserver %NetworkIP%:80"