import asyncio
from asyncua import Client, Node
from asyncua.ua.uaerrors import UaStatusCodeError

class SubscriptionHandler:
    async def datachange_notification(self, node: Node, val, data):
        print(f"New data change event: {node} = {val}")

async def main():
    url = "opc.tcp://localhost:4840/myopcua/server/"
    
    async with Client(url=url) as client:
        try:
            # Use the correct namespace URI
            custom_namespace_uri = "http://example.com/MyOPCUAServer/"
            nsidx = await client.get_namespace_index(custom_namespace_uri)

            # Get a variable node using its browse path
            myvar = await client.nodes.root.get_child(
                ["0:Objects", f"{nsidx}:MyObject", f"{nsidx}:MyVariable"]
            )

            # Read and print the value of MyVariable
            value = await myvar.read_value()
            print(f"Initial MyVariable value: {value}")

            # Create a subscription
            handler = SubscriptionHandler()
            subscription = await client.create_subscription(100, handler)
            await subscription.subscribe_data_change(myvar)

            # Keep the client running to receive updates
            print("Subscribed to data changes. Waiting for 30 seconds...")
            await asyncio.sleep(30)

        except UaStatusCodeError as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped...")
