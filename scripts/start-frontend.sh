#!/bin/bash
# Start the frontend development server

echo "🎨 Starting PDF Extractor Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    pnpm install
fi

# Start the development server
echo "✅ Starting Next.js development server on http://localhost:3000"
pnpm dev

