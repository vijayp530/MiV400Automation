#1 Copy \\10.163.33.106\Public\ROBOT\celery to c:\celery
#2 Make sure python 2.7 is installed
#3 Modify ENV PATH to include python exe location
#4 Install pip 
#5 run python -m pip install celery==3.1.23
#6 run python -m pip install redis
#7 Modify celeryTasks.py redis IP to point to ATF host
#8 Run schtasks /Create /SC minute /MO 15 /TN celeryWorker /TR c:\celery\start_celery.bat

schtasks /Delete /TN celeryWorker