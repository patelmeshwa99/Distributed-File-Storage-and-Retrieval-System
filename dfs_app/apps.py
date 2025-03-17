import os
import subprocess
import threading
from django.apps import AppConfig
import psutil

class DfsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dfs_app'

    def ready(self):
        # Start Kademlia DHT server
        # kademlia_service.start_server()

        def start_webrtc_server():
            try:
                print("Starting WebRTC Server...")
                subprocess.Popen(["python3", "dfs_app/utils/client.py"])  # Path to your client script
            except Exception as e:
                print(f"Error starting WebRTC client: {e}")

        # # Start WebRTC Client (optional, if you want to trigger signaling)
        def start_webrtc_client():
            try:
                print("Starting WebRTC Client...")
                subprocess.Popen(["python3", "dfs_app/utils/client.py"])  # Path to your client script
            except Exception as e:
                print(f"Error starting WebRTC client: {e}")



        # Start both in separate threads
        # start_webrtc_server()
        # start_webrtc_client()
        # threading.Thread(target=start_webrtc_server, daemon=True).start()
        # threading.Thread(target=start_webrtc_client, daemon=True).start()
