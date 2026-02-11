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
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  Mac: brew install python3"
    exit 1
fi

echo "[1/4] Checking Python... OK"
echo ""

# Check if we're in a virtual environment and ensure pip is available
echo "[2/4] Ensuring pip is available..."

if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "Virtual environment detected: $VIRTUAL_ENV"
    # Ensure pip is installed in the virtual environment
    python3 -m ensurepip --upgrade 2>/dev/null || {
        echo "Installing pip in virtual environment..."
        curl -sS https://bootstrap.pypa.io/get-pip.py | python3
    }
else
    # Check if pip exists globally
    if ! python3 -m pip --version &> /dev/null; then
        echo "Installing pip..."
        sudo apt install -y python3-pip 2>/dev/null || {
            curl -sS https://bootstrap.pypa.io/get-pip.py | python3
        }
    fi
fi

# Upgrade pip
python3 -m pip install --upgrade pip 2>/dev/null || true

echo ""

# Install Python dependencies
echo "[3/4] Installing Python dependencies..."
python3 -m pip install yt-dlp

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to install yt-dlp!"
    echo "Try running: pip install yt-dlp"
    exit 1
fi

echo ""
echo "[4/4] Installing FFmpeg..."

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