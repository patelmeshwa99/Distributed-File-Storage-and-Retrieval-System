import asyncio
from aiortc import RTCConfiguration, RTCPeerConnection, RTCSessionDescription
import websockets
import json

async def offer_peer_connection():
    print("///////////////////////////////")
    # Connect to the signaling server
    async with websockets.connect("ws://127.0.0.1:8765") as websocket:
        
        # Create a peer connection
        pc = RTCPeerConnection(RTCConfiguration())

        # Create a data channel for sending file data
        data_channel = pc.createDataChannel("fileTransfer")
        
        # Define what happens when the data channel opens
        data_channel.onopen = lambda: print("Data channel opened")
        
        # Create an offer
        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)

        # Send the offer to the signaling server
        await websocket.send(json.dumps({"type": "offer", "sdp": offer.sdp}))
        
        # Wait for the answer from the signaling server
        response = await websocket.recv()
        data = json.loads(response)
        
        if "type" in data and data["type"] == "answer":
            answer_sdp = data["sdp"]
            print("Received answer:", answer_sdp)
            
            # Set remote description (answer)
            await pc.setRemoteDescription(RTCSessionDescription(sdp=answer_sdp, type="answer"))
        
        # Handle ICE candidates
        while True:
            candidate_message = await websocket.recv()
            candidate_data = json.loads(candidate_message)
            if candidate_data["type"] == "candidate":
                print("Received ICE candidate:", candidate_data)
                candidate = candidate_data["candidate"]
                await pc.addIceCandidate(candidate)
        
        # Close the connection after use
        await pc.close()

# Run the peer connection process
# print("Hi")
asyncio.run(offer_peer_connection())
