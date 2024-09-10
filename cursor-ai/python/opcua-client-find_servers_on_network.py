import asyncio
from asyncua import Client, ua

async def find_servers_on_network(discovery_url):
    async with Client(url=discovery_url) as client:
        try:
            # Connect to the discovery server
            await client.connect()
            print(f"Connected to discovery endpoint at {discovery_url}")

            # Use the FindServersOnNetwork service
            servers = await client.find_servers_on_network()
            
            if not servers:
                print("No servers found on the network.")
            else:
                print(f"Found {len(servers)} server(s) on the network:")
                for server in servers:
                    print(f"\nServer:")
                    print(f"  Server Name: {server.ServerName}")
                    print(f"  Discovery URL: {server.DiscoveryUrl}")
                    print(f"  Server Capabilities:")
                    for capability in server.ServerCapabilities:
                        print(f"    - {capability}")
                    print(f"  Application URI: {server.ApplicationUri}")
                    print(f"  Product URI: {server.ProductUri}")
                    print(f"  Application Type: {server.ApplicationType}")
                    print(f"  Gateway Server URI: {server.GatewayServerUri}")
                    print(f"  Discovery Profile URI: {server.DiscoveryProfileUri}")
                    print(f"  Application Name: {server.ApplicationName.Text}")

        except ua.UaError as e:
            print(f"An error occurred: {e}")

async def main():
    # Replace with your discovery server URL
    # This should typically be a Local Discovery Server (LDS) URL
    discovery_url = "opc.tcp://localhost:4840"

    await find_servers_on_network(discovery_url)

if __name__ == "__main__":
    asyncio.run(main())