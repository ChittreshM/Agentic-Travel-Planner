#!/usr/bin/env python3
"""
Start all agents and Streamlit app for the Travel Planner
"""
import os
import subprocess
import time
import sys

# Set API key
os.environ['OPENAI_API_KEY'] = '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'

def start_agent(name, port):
    """Start an agent on a specific port"""
    cmd = [
        sys.executable, '-m', 'uvicorn',
        f'agents.{name}.__main__:app',
        '--port', str(port),
        '--host', '0.0.0.0'
    ]
    print(f"Starting {name} on port {port}...")
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    return process

def main():
    print("Setting OPENAI_API_KEY=sk-proj-...")
    print("=" * 50)
    
    # Start all agents
    agents = [
        ('host_agent', 8000),
        ('flight_agent', 8001),
        ('stay_agent', 8002),
        ('activities_agent', 8003),
        ('places_agent', 8004),
        ('photos_agent', 8005)
    ]
    
    processes = []
    for name, port in agents:
        proc = start_agent(name, port)
        processes.append((name, port, proc))
        time.sleep(1)  # Small delay between starts
    
    print("\nWaiting for agents to start...")
    time.sleep(5)
    
    # Check if agents are running
    import requests
    print("\nChecking agent status:")
    for name, port, proc in processes:
        try:
            response = requests.get(f'http://localhost:{port}/health', timeout=2)
            if response.status_code == 200:
                print(f"✓ {name} is running on port {port}")
            else:
                print(f"✗ {name} returned status {response.status_code}")
        except Exception as e:
            print(f"✗ {name} not responding: {e}")
    
    print("\n" + "=" * 50)
    print("Starting Streamlit app...")
    print("The app will be available at http://localhost:8501")
    print("=" * 50)
    
    # Start Streamlit
    streamlit_cmd = [sys.executable, '-m', 'streamlit', 'run', 'travel_ui.py']
    subprocess.run(streamlit_cmd, cwd=os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    main()

