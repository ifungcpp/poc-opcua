import asyncio
from asyncua import Client
from asyncua.common.node import Node

async def browse_nodes(node: Node, indent=0):
    try:
        children = await node.get_children()
    except Exception as e:
        print(f"Error browsing {node}: {e}")
        return

    for child in children:
        try:
            name = await child.read_browse_name()
            node_class = await child.read_node_class()
            node_id = child.nodeid
            
            # Only process and print nodes with namespace index > 1
            if node_id.NamespaceIndex >= 1:
                print(f"{'  ' * indent}{name.Name} ({node_class.name}) - NodeId: {node_id}")
                
                # Recursively browse child nodes
                await browse_nodes(child, indent + 1)
            else:
                # Still browse children of nodes with namespace <= 1, but don't print them
                await browse_nodes(child, indent)
            
        except Exception as e:
            print(f"Error processing {child}: {e}")

async def main():
    # Replace with your OPC UA server URL
    url = "opc.tcp://localhost:4840"
    
    async with Client(url=url) as client:
        # Connect to the server
        await client.connect()
        print(f"Connected to OPC UA server at {url}")

        # Get the root node
        root = client.get_root_node()
        print("Browsing nodes:")
        
        # Start browsing from the root node
        await browse_nodes(root)

if __name__ == "__main__":
    asyncio.run(main())
