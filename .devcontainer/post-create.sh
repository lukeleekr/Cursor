#!/bin/bash

# This script runs after the devcontainer is created
# It installs dependencies for all Node.js projects in the repository

set -e

echo "🚀 Setting up Vibe Book development environment..."

# Install dependencies for instagram-app (Vite + React)
if [ -d "Chapter-4/instagram-app" ]; then
    echo "📦 Installing dependencies for instagram-app..."
    cd "Chapter-4/instagram-app"
    if [ -f "package.json" ]; then
        npm install
        echo "✅ instagram-app dependencies installed"
    fi
    cd ../..
fi

# Install dependencies for memo-app (Create React App)
if [ -d "Chapter-4/memo-app" ]; then
    echo "📦 Installing dependencies for memo-app..."
    cd "Chapter-4/memo-app"
    if [ -f "package.json" ]; then
        npm install
        echo "✅ memo-app dependencies installed"
    fi
    cd ../..
fi

echo "✨ Development environment setup complete!"
echo ""
echo "To start a project:"
echo "  - Vite app: cd 'Chapter-4/instagram-app' && npm run dev"
echo "  - CRA app:  cd 'Chapter-4/memo-app' && npm start"


