@echo off
title YouTube Video Downloader
python gui.py
if errorlevel 1 (
    echo.
    echo ERROR: Failed to start downloader!
    echo Please run install.bat first.
    pause
)