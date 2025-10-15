#!/bin/bash
# Build script for Code Snippet Manager

set -e  # Exit on error

echo "============================================"
echo "Code Snippet Manager - Build Script"
echo "============================================"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated!"
    echo "Please activate it first:"
    echo "  source venv/bin/activate"
    exit 1
fi

echo "✓ Virtual environment: $VIRTUAL_ENV"
echo ""

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller not found!"
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

echo "✓ PyInstaller installed"
echo ""

# Clean previous builds
echo "[1/4] Cleaning previous builds..."
rm -rf build dist
echo "✓ Cleaned"
echo ""

# Run tests
echo "[2/4] Running integration tests..."
python test_integration.py
if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Aborting build."
    exit 1
fi
echo "✓ Tests passed"
echo ""

# Build executable
echo "[3/4] Building executable..."
pyinstaller build.spec --clean

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi
echo "✓ Build successful"
echo ""

# Check output
echo "[4/4] Checking output..."
if [ -d "dist/CodeSnippetManager" ]; then
    echo "✓ Build directory: dist/CodeSnippetManager"

    if [ "$(uname)" == "Darwin" ]; then
        if [ -d "dist/CodeSnippetManager.app" ]; then
            echo "✓ macOS App Bundle: dist/CodeSnippetManager.app"
        fi
    fi

    # Show directory contents
    echo ""
    echo "Contents:"
    ls -lh dist/CodeSnippetManager/

    # Show size
    SIZE=$(du -sh dist/CodeSnippetManager | cut -f1)
    echo ""
    echo "Total size: $SIZE"
else
    echo "❌ Build directory not found!"
    exit 1
fi

echo ""
echo "============================================"
echo "✅ Build Complete!"
echo "============================================"
echo ""
echo "Executable location:"
echo "  dist/CodeSnippetManager/CodeSnippetManager"
echo ""

if [ "$(uname)" == "Darwin" ]; then
    echo "macOS App Bundle:"
    echo "  dist/CodeSnippetManager.app"
    echo ""
    echo "To run:"
    echo "  open dist/CodeSnippetManager.app"
else
    echo "To run:"
    echo "  ./dist/CodeSnippetManager/CodeSnippetManager"
fi

echo ""
