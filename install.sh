#!/bin/bash

echo "========================================"
echo "YouTube Video Downloader - Installer"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.7 or higher:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Mac: brew install python3"
    exit 1
fi

echo "[1/3] Checking Python... OK"
echo ""

# Install Python dependencies
echo "[2/3] Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to install dependencies!"
    exit 1
fi

echo ""
echo "[3/3] Installing FFmpeg..."

# Check if ffmpeg exists
if command -v ffmpeg &> /dev/null; then
    echo "FFmpeg is already installed!"
else
    echo "Installing FFmpeg..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt update
        sudo apt install -y ffmpeg
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # Mac
        brew install ffmpeg
    fi
fi

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "You can now run the downloader using:"
echo "  - GUI: ./start_downloader.sh"
echo "  - CLI: python3 downloader.py --help"
echo ""