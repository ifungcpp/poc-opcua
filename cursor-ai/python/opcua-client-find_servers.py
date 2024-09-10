import asyncio
from asyncua import Client
from asyncua.common.xmlimporter import XmlImporter
from asyncua.common.structures import load_type_definitions

async def find_servers(discovery_url):
    async with Client(url=discovery_url) as client:
        # Connect to the discovery server
        await client.connect()
        print(f"Connected to discovery server at {discovery_url}")

        # Use the FindServers service
        servers = await client.find_servers()
        
        if not servers:
            print("No servers found.")
        else:
            print(f"Found {len(servers)} server(s):")
            for server in servers:
                print(f"\nServer:")
                print(f"  Application URI: {server.ApplicationUri}")
                print(f"  Product URI: {server.ProductUri}")
                print(f"  Application Name: {server.ApplicationName.Text}")
                print(f"  Application Type: {server.ApplicationType}")
                print(f"  Gateway Server URI: {server.GatewayServerUri}")
                print(f"  Discovery Profile URI: {server.DiscoveryProfileUri}")
                print("  Discovery URLs:")
                for url in server.DiscoveryUrls:
                    print(f"    - {url}")

async def main():
    # Replace with your discovery server URL
    # If you don't have a specific discovery server, you can use the URL of any OPC UA server
    discovery_url = "opc.tcp://localhost:4840"

    await find_servers(discovery_url)

if __name__ == "__main__":
    asyncio.run(main())
