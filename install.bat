@echo off
echo ========================================
echo YouTube Video Downloader - Installer
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

echo [1/3] Checking Python... OK
echo.

:: Install Python dependencies
echo [2/3] Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo [3/3] Installing FFmpeg...

:: Check if ffmpeg exists
ffmpeg -version >nul 2>&1
if not errorlevel 1 (
    echo FFmpeg is already installed!
    goto :done
)

:: Download ffmpeg using yt-dlp's bundled version
echo Downloading FFmpeg (this may take a minute)...
python -m pip install --upgrade yt-dlp[default]

:done
echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now run the downloader using:
echo   - GUI: start_downloader.bat
echo   - CLI: python downloader.py --help
echo.
pause