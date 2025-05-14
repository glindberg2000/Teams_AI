#!/usr/bin/env python3
"""
MCP Matrix Client - Integrates Matrix Relay with MCP for LedgerFlow AI Team
"""
import os
import sys
import json
import time
import requests
import threading
from datetime import datetime


class MCPMatrixClient:
    """Matrix client that can be used with MCP"""

    def __init__(self, username="mcp_test", password="test123"):
        self.homeserver_url = "http://localhost:8980"
        self.username = username
        self.password = password
        self.access_token = None
        self.user_id = None
        self.device_id = None
        self.sync_token = None
        self.rooms = {}
        self.running = False
        self.sync_thread = None
        self.callbacks = []

    def register(self):
        """Register a new user"""
        try:
            url = f"{self.homeserver_url}/_matrix/client/r0/register"
            data = {
                "username": self.username,
                "password": self.password,
                "auth": {"type": "m.login.dummy"},
            }
            response = requests.post(url, json=data)

            if response.status_code == 200:
                result = response.json()
                self.access_token = result["access_token"]
                self.user_id = result["user_id"]
                self.device_id = result["device_id"]
                print(f"Successfully registered as {self.user_id}")
                return True
            else:
                print(f"Registration failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Error during registration: {e}")
            return False

    def login(self):
        """Log in to the homeserver"""
        try:
            url = f"{self.homeserver_url}/_matrix/client/r0/login"
            data = {
                "type": "m.login.password",
                "user": self.username,
                "password": self.password,
            }
            response = requests.post(url, json=data)

            if response.status_code == 200:
                result = response.json()
                self.access_token = result["access_token"]
                self.user_id = result["user_id"]
                self.device_id = result["device_id"]
                print(f"Successfully logged in as {self.user_id}")
                return True
            else:
                print(f"Login failed: {response.status_code} - {response.text}")
                # Try registration if login fails
                return self.register()
        except Exception as e:
            print(f"Error during login: {e}")
            return False

    def create_room(self, room_name):
        """Create a new room"""
        if not self.access_token:
            print("Not logged in")
            return None

        try:
            url = f"{self.homeserver_url}/_matrix/client/r0/createRoom"
            data = {
                "name": room_name,
                "preset": "public_chat",
            }
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                result = response.json()
                room_id = result["room_id"]
                self.rooms[room_name] = room_id
                print(f"Created room {room_name} with ID {room_id}")
                return room_id
            else:
                print(f"Room creation failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error creating room: {e}")
            return None

    def join_room(self, room_id_or_alias):
        """Join a room by ID or alias"""
        if not self.access_token:
            print("Not logged in")
            return False

        try:
            url = f"{self.homeserver_url}/_matrix/client/r0/join/{room_id_or_alias}"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.post(url, json={}, headers=headers)

            if response.status_code == 200:
                result = response.json()
                room_id = result["room_id"]
                print(f"Joined room {room_id}")
                return room_id
            else:
                print(f"Room join failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error joining room: {e}")
            return None

    def send_message(self, room_id, message):
        """Send a message to a room"""
        if not self.access_token:
            print("Not logged in")
            return False

        try:
            url = f"{self.homeserver_url}/_matrix/client/r0/rooms/{room_id}/send/m.room.message"
            data = {"msgtype": "m.text", "body": message}
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                print(f"Message sent to room {room_id}")
                return True
            else:
                print(f"Message send failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Error sending message: {e}")
            return False

    def start_sync(self, callback=None):
        """Start syncing with the server in a background thread"""
        if callback:
            self.callbacks.append(callback)

        if self.sync_thread and self.sync_thread.is_alive():
            return True

        self.running = True
        self.sync_thread = threading.Thread(target=self._sync_loop)
        self.sync_thread.daemon = True
        self.sync_thread.start()
        return True

    def _sync_loop(self):
        """Main sync loop that runs in the background"""
        while self.running:
            try:
                self._sync_once()
                time.sleep(1)  # Wait a bit before next sync
            except Exception as e:
                print(f"Sync error: {e}")
                time.sleep(5)  # Wait longer after an error

    def _sync_once(self):
        """Perform one sync with the server"""
        if not self.access_token:
            print("Not logged in")
            return

        try:
            url = f"{self.homeserver_url}/_matrix/client/r0/sync"
            params = {"timeout": 30000}

            if self.sync_token:
                params["since"] = self.sync_token

            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                self.sync_token = data["next_batch"]

                # Process rooms and events
                if "rooms" in data and "join" in data["rooms"]:
                    for room_id, room_data in data["rooms"]["join"].items():
                        if (
                            "timeline" in room_data
                            and "events" in room_data["timeline"]
                        ):
                            events = room_data["timeline"]["events"]
                            for event in events:
                                if (
                                    event["type"] == "m.room.message"
                                    and event.get("sender") != self.user_id
                                ):
                                    # Process incoming message
                                    sender = event.get("sender", "unknown")
                                    content = event.get("content", {})
                                    body = content.get("body", "")
                                    timestamp = datetime.now().strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    )

                                    # Call any registered callbacks
                                    for callback in self.callbacks:
                                        callback(
                                            {
                                                "room_id": room_id,
                                                "sender": sender,
                                                "body": body,
                                                "timestamp": timestamp,
                                                "event": event,
                                            }
                                        )
            else:
                print(f"Sync failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error during sync: {e}")

    def stop_sync(self):
        """Stop the sync thread"""
        self.running = False
        if self.sync_thread:
            self.sync_thread.join(timeout=1)

    def logout(self):
        """Log out from the homeserver"""
        if not self.access_token:
            return True

        try:
            self.stop_sync()

            url = f"{self.homeserver_url}/_matrix/client/r0/logout"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.post(url, json={}, headers=headers)

            if response.status_code == 200:
                self.access_token = None
                self.user_id = None
                self.device_id = None
                self.sync_token = None
                print("Successfully logged out")
                return True
            else:
                print(f"Logout failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Error during logout: {e}")
            return False


def message_callback(event):
    """Example callback function for processing messages"""
    print(f"[{event['timestamp']}] {event['sender']}: {event['body']}")


# Simple test function
def test_client():
    client = MCPMatrixClient("test_user", "test_password")
    if client.login():
        room_id = client.create_room("Test Room")
        if room_id:
            client.send_message(room_id, "Hello from MCPMatrixClient!")
            client.start_sync(message_callback)
            print("Listening for messages. Press Ctrl+C to stop.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Stopping client...")
            finally:
                client.stop_sync()
                client.logout()


if __name__ == "__main__":
    test_client()
