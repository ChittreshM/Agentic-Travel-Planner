#!/bin/bash

echo "=== Stopping All Services ==="
echo ""

# Kill uvicorn agents
echo "Stopping agents..."
pkill -f "uvicorn.*800[0-3]" 2>/dev/null
pkill -f "python.*uvicorn.*800[0-3]" 2>/dev/null

# Kill Streamlit
echo "Stopping Streamlit..."
pkill -f "streamlit.*travel_ui" 2>/dev/null
pkill -f "python.*streamlit.*travel_ui" 2>/dev/null

# Kill any processes on the ports directly
echo "Releasing ports..."
for port in 8000 8001 8002 8003 8501; do
    lsof -ti:$port 2>/dev/null | xargs kill -9 2>/dev/null
done

# Wait a moment
sleep 2

# Verify everything is stopped
echo ""
echo "=== Verification ==="
echo ""

echo "Port Status:"
for port in 8000 8001 8002 8003 8501; do
    if lsof -ti:$port > /dev/null 2>&1; then
        echo "✗ Port $port: Still in use"
    else
        echo "✓ Port $port: Free"
    fi
done

echo ""
echo "Process Check:"
REMAINING=$(ps aux | grep -E "uvicorn|streamlit" | grep -v grep | wc -l | tr -d ' ')
if [ "$REMAINING" -eq 0 ]; then
    echo "✓ All processes stopped - Resources released"
else
    echo "✗ $REMAINING process(es) still running:"
    ps aux | grep -E "uvicorn|streamlit" | grep -v grep
fi

echo ""
echo "=== Cleanup Complete ==="


