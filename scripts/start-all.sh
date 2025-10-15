#!/bin/bash
# Start both backend and frontend in separate terminals

echo "🚀 Starting PDF Extractor (Full Stack)..."

# Check if running on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - use Terminal
    osascript -e 'tell app "Terminal" to do script "cd \"'$(pwd)'\" && ./scripts/start-backend.sh"'
    osascript -e 'tell app "Terminal" to do script "cd \"'$(pwd)'\" && ./scripts/start-frontend.sh"'
    echo "✅ Started backend and frontend in separate Terminal windows"
else
    # Linux - try gnome-terminal or xterm
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd $(pwd) && ./scripts/start-backend.sh; exec bash"
        gnome-terminal -- bash -c "cd $(pwd) && ./scripts/start-frontend.sh; exec bash"
        echo "✅ Started backend and frontend in separate gnome-terminal windows"
    elif command -v xterm &> /dev/null; then
        xterm -e "cd $(pwd) && ./scripts/start-backend.sh" &
        xterm -e "cd $(pwd) && ./scripts/start==-frontend.sh" &
        echo "✅ Started backend and frontend in separate xterm windows"
    else
        echo "⚠️  Could not find a suitable terminal emulator"
        echo "Please run the following commands in separate terminals:"
        echo "  Terminal 1: ./scripts/start-backend.sh"
        echo "  Terminal 2: ./scripts/start-frontend.sh"
    fi
fi

