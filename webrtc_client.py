import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
import socketio

# Set up WebRTC connection
class WebRTCClient:
    def __init__(self, signaling_server_url):
        self.sio = socketio.Client()
        self.sio.connect(signaling_server_url)

    def create_peer_connection(self):
        self.pc = RTCPeerConnection()

        # Set up WebRTC data channel
        self.data_channel = self.pc.createDataChannel('file_transfer')

        # Define event when data is received
        self.data_channel.on('message', self.on_data_received)

    def on_data_received(self, message):
        print(f"Received data: {message}")

    async def send_offer(self):
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        # Send offer to signaling server
        self.sio.emit('offer', {'offer': offer.sdp})

    async def send_answer(self, offer_sdp):
        offer = RTCSessionDescription(sdp=offer_sdp, type='offer')
        await self.pc.setRemoteDescription(offer)
        answer = await self.pc.createAnswer()
        await self.pc.setLocalDescription(answer)
        # Send answer back to signaling server
        self.sio.emit('answer', {'answer': answer.sdp})

if __name__ == '__main__':
    signaling_server_url = "http://127.0.0.1:5000"
    client = WebRTCClient(signaling_server_url)
    client.create_peer_connection()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.send_offer())