#!/bin/bash

echo "=========================================="
echo "Ingredient Intelligence Analyzer Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Create .env file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your OpenAI API key!"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p output
mkdir -p examples
echo "✓ Directories created"
echo ""

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OPENAI_API_KEY"
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo "3. Run example:"
echo "   python example.py"
echo ""
echo "For more information, see README.md"
echo ""
