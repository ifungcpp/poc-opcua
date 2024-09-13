import asyncio
from asyncua import Client, Node, ua
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

            print(f"nsidx: {nsidx}")
            print(f"client: {client}")
            print(f"client.nodes.root: {client.nodes.root}")  # root as i=84
            print(f"client.nodes.root: {client.nodes.root!r}")
            print("Children of root are: ", await client.nodes.root.get_children())  # return list of nodes like [Node(i=85), Node(i=86), Node(i=87)]

            # Get a variable node using its browse path
            myvar = await client.nodes.root.get_child(
                ["0:Objects", f"{nsidx}:MyObject", f"{nsidx}:MyVariable"]
            )

            # Read and print the value of MyVariable
            value = client.get_node(ua.NodeId("MyVariable", nsidx))
            value = client.get_node(f"ns={nsidx};s=MyVariable")
            value = await myvar.read_value()
            datavalue = await myvar.read_data_value()
            print(f"Initial MyVariable value: {value}, {datavalue}")

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
        print("Client starting...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Client stopped...")
