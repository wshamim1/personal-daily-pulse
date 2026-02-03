#!/bin/bash

# Start Frontend Script
# This script installs dependencies and starts the React development server

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

echo "=========================================="
echo "🚀 Starting My Daily Log Frontend"
echo "=========================================="
echo ""

# Check if Node.js and npm are installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed"
    echo "Please install Node.js (which includes npm) and try again"
    echo "Download from: https://nodejs.org/"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed"
    echo "Please install Node.js which includes npm"
    exit 1
fi

echo "📦 Node.js version:"
node --version
echo "npm version:"
npm --version
echo ""

# Navigate to frontend directory
cd "$FRONTEND_DIR"

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies with npm..."
    npm install
else
    echo "📦 Dependencies already installed"
fi

echo ""
echo "=========================================="
echo "✅ Frontend server starting..."
echo "=========================================="
echo "📍 Frontend URL: http://localhost:3000"
echo "📍 Backend should be running at: http://localhost:5000"
echo ""
echo "Tips:"
echo "  - The app will open in your browser automatically"
echo "  - Press Ctrl+C to stop the server"
echo "  - Hot reload is enabled - changes will update automatically"
echo "=========================================="
echo ""

# Start React development server
npm start
