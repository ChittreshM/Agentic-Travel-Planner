#!/bin/bash
echo "=== Service Status Check ==="
echo ""

echo "Checking agents..."
for port in 8000 8001 8002 8003; do
    if curl -s http://localhost:$port/health > /dev/null 2>&1; then
        echo "✓ Port $port: Agent is running"
    else
        echo "✗ Port $port: Not responding"
    fi
done

echo ""
echo "Checking Streamlit..."
if curl -s http://localhost:8501 > /dev/null 2>&1; then
    echo "✓ Streamlit is running on http://localhost:8501"
else
    echo "✗ Streamlit is not responding"
fi

echo ""
echo "Process list:"
ps aux | grep -E "uvicorn.*800[0-3]|streamlit.*8501" | grep -v grep

