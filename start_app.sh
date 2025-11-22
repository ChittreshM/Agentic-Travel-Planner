#!/bin/bash

# Set API key
export OPENAI_API_KEY="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"

# Navigate to the project directory
cd /Users/mmitra/python-ds-algo-env/algorithms/Problems/Google-Agent-Development-Kit-Demo

# Activate virtual environment
source /Users/mmitra/python-ds-algo-env/venv/bin/activate

# Install dependencies if needed
echo "Checking dependencies..."
pip install -q -r requirements.txt 2>/dev/null || echo "Dependencies check complete"

# Start agents in background using python -m uvicorn
echo "Starting agents..."
python3 -m uvicorn agents.host_agent.__main__:app --port 8000 > /tmp/host_agent.log 2>&1 &
HOST_PID=$!

python3 -m uvicorn agents.flight_agent.__main__:app --port 8001 > /tmp/flight_agent.log 2>&1 &
FLIGHT_PID=$!

python3 -m uvicorn agents.stay_agent.__main__:app --port 8002 > /tmp/stay_agent.log 2>&1 &
STAY_PID=$!

python3 -m uvicorn agents.activities_agent.__main__:app --port 8003 > /tmp/activities_agent.log 2>&1 &
ACTIVITIES_PID=$!

python3 -m uvicorn agents.places_agent.__main__:app --port 8004 > /tmp/places_agent.log 2>&1 &
PLACES_PID=$!

python3 -m uvicorn agents.photos_agent.__main__:app --port 8005 > /tmp/photos_agent.log 2>&1 &
PHOTOS_PID=$!

echo "Agents started. PIDs: Host=$HOST_PID, Flight=$FLIGHT_PID, Stay=$STAY_PID, Activities=$ACTIVITIES_PID, Places=$PLACES_PID, Photos=$PHOTOS_PID"

# Wait for agents to start
echo "Waiting for agents to initialize..."
sleep 5

# Check if agents are running
echo "Checking agent status..."
curl -s http://localhost:8000/health > /dev/null && echo "✓ Host agent is running" || echo "✗ Host agent failed to start"
curl -s http://localhost:8001/health > /dev/null && echo "✓ Flight agent is running" || echo "✗ Flight agent failed to start"
curl -s http://localhost:8002/health > /dev/null && echo "✓ Stay agent is running" || echo "✗ Stay agent failed to start"
curl -s http://localhost:8003/health > /dev/null && echo "✓ Activities agent is running" || echo "✗ Activities agent failed to start"
curl -s http://localhost:8004/health > /dev/null && echo "✓ Places agent is running" || echo "✗ Places agent failed to start"
curl -s http://localhost:8005/health > /dev/null && echo "✓ Photos agent is running" || echo "✗ Photos agent failed to start"

# Start Streamlit
echo ""
echo "Starting Streamlit app..."
echo "The app will open at http://localhost:8501"
echo ""
python3 -m streamlit run travel_ui.py

# Cleanup function (if script is interrupted)
trap "kill $HOST_PID $FLIGHT_PID $STAY_PID $ACTIVITIES_PID $PLACES_PID $PHOTOS_PID 2>/dev/null; exit" INT TERM

