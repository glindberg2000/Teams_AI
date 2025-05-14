#!/usr/bin/env python3
"""
Simple test script for Matrix relay system
"""
import os
import sys
import time
import subprocess


def main():
    """Start the Matrix server, wait, then stop it"""
    try:
        # Ensure data directory exists with proper permissions
        print("Setting up data directory...")
        os.makedirs("data", exist_ok=True)
        subprocess.run(["chmod", "777", "data"], check=True)

        # Clean up any existing containers
        print("Cleaning up existing containers...")
        subprocess.run(["docker-compose", "down", "--remove-orphans", "-v"], check=True)

        # Start the server
        print("Starting Matrix server...")
        subprocess.run(["docker-compose", "up", "-d"], check=True)

        # Check if containers are running
        print("Checking container status...")
        subprocess.run(["docker-compose", "ps"], check=True)

        # Wait for user to press a key
        print("\nMatrix server is running. Press Enter to stop it...")
        input()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Stop the server
        print("Stopping Matrix server...")
        subprocess.run(["docker-compose", "down", "--remove-orphans", "-v"], check=True)


if __name__ == "__main__":
    main()
