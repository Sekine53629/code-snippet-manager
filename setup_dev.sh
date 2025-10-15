#!/bin/bash
# Development environment setup script

echo "================================"
echo "Code Snippet Manager - Dev Setup"
echo "================================"

# Create virtual environment
echo -e "\n[1] Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "[2] Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "[3] Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "[4] Installing dependencies..."
pip install -r requirements.txt

echo -e "\n================================"
echo "✓ Setup completed successfully!"
echo "================================"
echo -e "\nTo activate the virtual environment:"
echo "  source venv/bin/activate"
echo -e "\nTo run the application:"
echo "  python main.py"
