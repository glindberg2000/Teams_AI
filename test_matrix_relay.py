#!/usr/bin/env python3
"""
Test script for Matrix relay system that demonstrates long-running connections
"""
import os
import sys
import time
import json
import argparse
import subprocess
import threading
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from mcp_matrix_client import MCPMatrixClient


def start_docker_server():
    """Start the Matrix server using docker-compose"""
    print("Starting Matrix server...")
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

        # Ensure data directory exists with proper permissions
        os.makedirs("data", exist_ok=True)
        subprocess.run(["chmod", "777", "data"], check=True)

        # First stop any existing containers
        subprocess.run(["docker-compose", "down", "--remove-orphans"], check=True)

        # Start the server
        result = subprocess.run(
            ["docker-compose", "up", "-d"], check=True, capture_output=True, text=True
        )
        print(result.stdout)
        print("Matrix server started. Waiting for it to initialize...")
        time.sleep(15)  # Give it more time to start
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def stop_docker_server():
    """Stop the Matrix server"""
    print("Stopping Matrix server...")
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        subprocess.run(
            ["docker-compose", "down", "--remove-orphans"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Matrix server stopped")
        return True
    except Exception as e:
        print(f"Error stopping server: {e}")
        return False


def test_long_running_connection():
    """Test a long-running connection to Matrix server"""
    print("\n=== Testing long-running Matrix connection ===\n")

    # Create the first client (AI Agent 1)
    agent1 = MCPMatrixClient("agent1", "password123")
    if not agent1.login():
        print("Failed to login as agent1")
        return False

    # Create a room for the agents to communicate
    room_id = agent1.create_room("AI Agents Communication Room")
    if not room_id:
        print("Failed to create room")
        return False

    print(f"Created room with ID: {room_id}")

    # Create the second client (AI Agent 2)
    agent2 = MCPMatrixClient("agent2", "password123")
    if not agent2.login():
        print("Failed to login as agent2")
        return False

    # Have the second agent join the room
    if not agent2.join_room(room_id):
        print("Failed to join room")
        return False

    # Define message handlers for both agents
    def agent1_message_handler(event):
        if event["sender"].endswith("agent2"):
            print(f"[Agent1 received] {event['sender']}: {event['body']}")
            # Respond to messages from agent2
            if "hello" in event["body"].lower():
                time.sleep(1)  # Simulate thinking
                agent1.send_message(room_id, "Hello Agent2, I received your message!")
            elif "task" in event["body"].lower():
                time.sleep(1)  # Simulate thinking
                agent1.send_message(
                    room_id, "I'll start working on the task right away."
                )

    def agent2_message_handler(event):
        if event["sender"].endswith("agent1"):
            print(f"[Agent2 received] {event['sender']}: {event['body']}")
            # Respond to messages from agent1
            if "received" in event["body"].lower():
                time.sleep(1)  # Simulate thinking
                agent2.send_message(room_id, "Great! Let me assign you a task.")
            elif "working" in event["body"].lower():
                time.sleep(1)  # Simulate thinking
                agent2.send_message(room_id, "Wonderful. Let me know when you're done.")

    # Set up message listening for both agents
    agent1.start_sync(agent1_message_handler)
    agent2.start_sync(agent2_message_handler)

    print("Both agents connected and listening. Starting conversation...")

    # Start the conversation
    time.sleep(2)  # Give time for sync to establish
    agent2.send_message(room_id, "Hello Agent1, can you hear me?")

    # Let the conversation run for a while
    try:
        total_duration = 60  # Run for 60 seconds
        progress_interval = 5  # Show progress every 5 seconds

        print(f"\nRunning long-polling test for {total_duration} seconds...")
        print("Press Ctrl+C to stop early")

        for i in range(0, total_duration, progress_interval):
            time.sleep(progress_interval)
            seconds_left = total_duration - i - progress_interval
            if seconds_left >= 0:
                print(f"Test running... {seconds_left} seconds left")

        print("\nTest completed successfully!")
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    finally:
        # Clean up
        print("\nShutting down agents...")
        agent1.stop_sync()
        agent2.stop_sync()
        agent1.logout()
        agent2.logout()

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Matrix Relay System")
    parser.add_argument(
        "--no-server", action="store_true", help="Don't start/stop Docker server"
    )
    args = parser.parse_args()

    try:
        if not args.no_server:
            if not start_docker_server():
                print("Failed to start Matrix server. Exiting.")
                sys.exit(1)

        # Run the test
        test_long_running_connection()
    finally:
        if not args.no_server:
            stop_docker_server()
