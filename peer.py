from kademlia.network import Server
import asyncio

class KademliaServer:
    def __init__(self, node_id):
        self.server = Server()
        self.node_id = node_id

    async def start(self):
        await self.server.listen(8468)  # Kademlia listening port
        await self.server.bootstrap([('localhost', 8468)])  # Bootstrap with other nodes

    async def store_metadata(self, file_name, metadata):
        await self.server.set(file_name, metadata)

    async def get_metadata(self, file_name):
        return await self.server.get(file_name)
    
kademlia_server = KademliaServer(node_id="unique_node_id")
asyncio.run(kademlia_server.start())
