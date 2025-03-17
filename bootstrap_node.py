import asyncio
from kademlia.network import Server

class KademliaNode:
    def __init__(self, node_id, port=8468, bootstrap_node=None):
        self.node_id = node_id
        self.server = Server()
        self.port = port
        self.bootstrap_node = bootstrap_node

    async def start(self):
        """ Start the Kademlia node and bootstrap if needed """
        await self.server.listen(self.port)
        print(f"✅ Kademlia Node {self.node_id} started on port {self.port}")

        if self.bootstrap_node:
            await asyncio.sleep(2)  # Ensure readiness before bootstrapping
            try:
                print(f"🔗 Bootstrapping to {self.bootstrap_node}")
                await self.server.bootstrap([self.bootstrap_node])
                print(f"✅ Node {self.node_id} bootstrapped successfully!")
            except Exception as e:
                print(f"❌ Bootstrap error: {e}")
        else:
            print(f"✅ Node {self.node_id} is the bootstrap node")

        # Allow time for neighbors to be discovered
        print("Waiting for neighbors to be discovered...")
        await asyncio.sleep(10)  # Give it more time to discover neighbors

        # Print routing table buckets (neighbors)
        buckets = self.server.protocol.router.buckets
        print(f"Routing table buckets: {buckets}")

        # Collect all neighbors from the buckets
        all_neighbors = []
        for bucket in buckets:
            all_neighbors.extend(bucket)  # Add all nodes in the bucket to the neighbors list

        print(f"Known neighbors: {all_neighbors}")


    async def set_metadata(self, key, value):
        """ Store metadata in the DHT """
        if not self.server.protocol:
            print("❌ Error: Kademlia server not initialized")
            return False

        await asyncio.sleep(5)  # Allow time for the bootstrap to complete

        try:
            await self.server.set(key, value)
            print(f"✅ Stored: {key} -> {value}")
            return True
        except Exception as e:
            print(f"❌ Error storing: {e}")
            return False

# Example usage to create the bootstrap node
async def main():
    node_id = 1  # Bootstrap node (Node 1)
    node = KademliaNode(node_id, port=8470, bootstrap_node=("127.0.0.1", 8468))  # No bootstrap node for the first node
    await node.start()

if __name__ == "__main__":
    asyncio.run(main())
