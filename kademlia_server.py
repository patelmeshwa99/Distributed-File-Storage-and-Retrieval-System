# kademlia_node.py

from kademlia.network import Server
import asyncio

class KademliaNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = Server()

    async def start(self):
        await self.server.listen(self.port)
        print(f"Kademlia node listening on {self.host}:{self.port}")

    async def bootstrap(self, bootstrap_node):
        await self.server.bootstrap([bootstrap_node])
        print(f"Connected to bootstrap node {bootstrap_node}")

    async def store_metadata(self, key, value):
        await self.server.set(key, value)

    async def get_metadata(self, key):
        value = await self.server.get(key)
        return value

# Initialize and start Kademlia node
node = KademliaNode("127.0.0.1", 5000)

async def run():
    await node.start()
    # Optionally bootstrap to another node (if already exists in the network)
    # await node.bootstrap(("127.0.0.1", 5001))

    # Example: Store metadata about a file chunk
    await node.store_metadata("file_chunk_1", "peer_1_location")
    metadata = await node.get_metadata("file_chunk_1")
    print(f"Metadata for file_chunk_1: {metadata}")

try:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # If the loop is already running (e.g., in an async context), create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run())
except RuntimeError:
    # If no loop is found, create one
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
loop = asyncio.get_event_loop()
