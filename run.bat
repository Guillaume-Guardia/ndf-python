@echo off

:: Find python path
FOR /f %%p in ('where python') do (
    SET PYTHONPATH=%%p
    goto :start
)
:start

%PYTHONPATH% "src\pyndf\main.py"
