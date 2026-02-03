#!/bin/bash

# Start Backend Script
# This script installs dependencies and starts the Flask backend server

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"

echo "=========================================="
echo "🚀 Starting My Daily Log Backend"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3 and try again"
    exit 1
fi

echo "📦 Python version:"
python3 --version
echo ""

# Navigate to backend directory
cd "$BACKEND_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📦 Installing dependencies from requirements.txt..."
venv/bin/pip3 install --upgrade pip > /dev/null 2>&1
venv/bin/pip3 install -r requirements.txt

echo ""
echo "=========================================="
echo "✅ Backend server starting..."
echo "=========================================="
echo "📍 Backend URL: http://localhost:5000"
echo "📍 API Docs: http://localhost:5000/docs"
echo "📍 ReDoc: http://localhost:5000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Start FastAPI with uvicorn using venv python
venv/bin/python3 -m uvicorn app:app --host 0.0.0.0 --port 5000 --reload
