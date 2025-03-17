import asyncio
from kademlia.network import Server

class KademliaService:
    """ Singleton service to run Kademlia in Django """
    _instance = None  # Ensures only one instance runs

    def __new__(cls, port=8468, bootstrap_node=None):
        if cls._instance is None:
            cls._instance = super(KademliaService, cls).__new__(cls)
            cls._instance.server = Server()
            cls._instance.port = port
            cls._instance.bootstrap_node = bootstrap_node
            cls._instance.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(cls._instance.loop)
            cls._instance.loop.run_until_complete(cls._instance.start())
        return cls._instance

    async def start(self):
        """ Start the Kademlia node and bootstrap if needed """
        await self.server.listen(self.port)
        print(f"✅ Kademlia Node started on port {self.port}")

        if self.bootstrap_node:
            await asyncio.sleep(2)  # Ensure readiness before bootstrapping
            try:
                print(f"🔗 Bootstrapping to {self.bootstrap_node}")
                await self.server.bootstrap([self.bootstrap_node])
                print("✅ Bootstrap successful!")
            except Exception as e:
                print(f"❌ Bootstrap error: {e}")

    async def set_metadata(self, key, value):
        """ Store metadata in the DHT """
        if not self.server.protocol:
            print("❌ Error: Kademlia server not initialized")
            return False
        try:
            await self.server.set(key, value)
            print(f"✅ Stored: {key} -> {value}")
            return True
        except Exception as e:
            print(f"❌ Error storing: {e}")
            return False

    async def get_metadata(self, key):
        """ Retrieve metadata from the DHT """
        if not self.server.protocol:
            print("❌ Error: Kademlia server not initialized")
            return None
        try:
            value = await self.server.get(key)
            print(f"🔍 Retrieved: {key} -> {value}")
            return value
        except Exception as e:
            print(f"❌ Error retrieving: {e}")
            return None

# Create a single instance of KademliaService when Django starts
kademlia_instance = KademliaService(port=8470, bootstrap_node=("127.0.0.1", 8468))
