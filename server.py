import asyncio
import requests
import websockets
import json

# Store connected peers
peers = {}

async def handle_signaling(websocket):
    """Handles WebRTC signaling messages between peers."""
    try:
        # Register peer
        peer_id = str(websocket.remote_address)
        print(f"Peer connected: {peer_id}")
        
        peers[peer_id] = websocket

        # Send a welcome message
        await websocket.send(json.dumps({"message": "Connected to signaling server"}))

        while True:
            # Wait for the signaling message from the client
            message = await websocket.recv()
            print(f"Received message from {peer_id}: {message}")

            # Broadcast the message to the other peer
            data = json.loads(message)

            # Send the message to the corresponding peer
            for peer, peer_ws in peers.items():
                if peer != peer_id:
                    try:
                        await peer_ws.send(json.dumps(data))
                    except websockets.exceptions.ConnectionClosed:
                        pass  # Ignore closed connections

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup: remove disconnected peer from the list
        if peer_id in peers:
            del peers[peer_id]
        print(f"Peer disconnected: {peer_id}")


async def start_signaling_server():
    print("==========================================")
    """Start the WebRTC signaling server."""
    server = await websockets.serve(handle_signaling, "127.0.0.1", 8765)
    print("Signaling server started on ws://192.168.2.144:8765")
    await server.wait_closed()

# Start the signaling server
# if __name__ == "__main__":
asyncio.run(start_signaling_server())
