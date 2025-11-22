#!/bin/bash

# Set API key
export OPENAI_API_KEY="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"

# Navigate to project directory
cd /Users/mmitra/python-ds-algo-env/algorithms/Problems/Google-Agent-Development-Kit-Demo

# Activate virtual environment
source /Users/mmitra/python-ds-algo-env/venv/bin/activate

# Kill any existing processes
echo "Cleaning up existing processes..."
pkill -f "uvicorn.*800[0-5]" 2>/dev/null
pkill -f "streamlit.*travel_ui" 2>/dev/null
sleep 2

# Start all agents
echo "Starting agents..."
python3 -m uvicorn agents.host_agent.__main__:app --port 8000 > /tmp/host_agent.log 2>&1 &
HOST_PID=$!
echo "Host agent started (PID: $HOST_PID)"

python3 -m uvicorn agents.flight_agent.__main__:app --port 8001 > /tmp/flight_agent.log 2>&1 &
FLIGHT_PID=$!
echo "Flight agent started (PID: $FLIGHT_PID)"

python3 -m uvicorn agents.stay_agent.__main__:app --port 8002 > /tmp/stay_agent.log 2>&1 &
STAY_PID=$!
echo "Stay agent started (PID: $STAY_PID)"

python3 -m uvicorn agents.activities_agent.__main__:app --port 8003 > /tmp/activities_agent.log 2>&1 &
ACTIVITIES_PID=$!
echo "Activities agent started (PID: $ACTIVITIES_PID)"

python3 -m uvicorn agents.places_agent.__main__:app --port 8004 > /tmp/places_agent.log 2>&1 &
PLACES_PID=$!
echo "Places agent started (PID: $PLACES_PID)"

python3 -m uvicorn agents.photos_agent.__main__:app --port 8005 > /tmp/photos_agent.log 2>&1 &
PHOTOS_PID=$!
echo "Photos agent started (PID: $PHOTOS_PID)"

# Wait for agents to start
echo ""
echo "Waiting for agents to initialize..."
sleep 5

# Check agent status
echo ""
echo "Checking agent status..."
for port in 8000 8001 8002 8003 8004 8005; do
    if curl -s --connect-timeout 2 http://localhost:$port > /dev/null 2>&1; then
        echo "✓ Port $port: Agent is running"
    else
        echo "✗ Port $port: Agent failed to start (check /tmp/*_agent.log)"
    fi
done

# Start Streamlit
echo ""
echo "Starting Streamlit..."
python3 -m streamlit run travel_ui.py > /tmp/streamlit.log 2>&1 &
STREAMLIT_PID=$!
echo "Streamlit started (PID: $STREAMLIT_PID)"

# Wait for Streamlit
sleep 5

# Final status
echo ""
echo "=== Final Status ==="
if curl -s --connect-timeout 2 http://localhost:8501 > /dev/null 2>&1; then
    echo "✓ Streamlit is running on http://localhost:8501"
    echo ""
    echo "Open your browser and go to: http://localhost:8501"
else
    echo "✗ Streamlit failed to start (check /tmp/streamlit.log)"
fi

echo ""
echo "All services are running in the background."
echo "To stop all services, run: pkill -f 'uvicorn|streamlit'"
echo ""
echo "PIDs: Host=$HOST_PID, Flight=$FLIGHT_PID, Stay=$STAY_PID, Activities=$ACTIVITIES_PID, Places=$PLACES_PID, Photos=$PHOTOS_PID, Streamlit=$STREAMLIT_PID"

