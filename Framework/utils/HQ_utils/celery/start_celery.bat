echo off

tasklist |findstr celery>nul && (
 echo celery is running
) || (
 echo celery is not running
echo starting celery
celery worker -A celeryTasks -n celeryTasks -Q celeryTasks -l info

)