import socketio
from aiohttp import web

# Initialize the Socket.IO server
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

# Handle incoming WebRTC messages
@sio.event
async def connect(sid, environ):
    print(f"Peer connected: {sid}")

@sio.event
async def offer(sid, data):
    print(f"Offer received from {sid}")
    # Send the offer to another peer
    await sio.emit('offer', data)

@sio.event
async def answer(sid, data):
    print(f"Answer received from {sid}")
    # Send the answer to the offerer
    await sio.emit('answer', data)

@sio.event
async def disconnect(sid):
    print(f"Peer disconnected: {sid}")

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=5000)