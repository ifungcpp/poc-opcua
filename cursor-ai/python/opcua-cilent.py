import asyncio
import traceback
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
            nsidx: int = await client.get_namespace_index(custom_namespace_uri)

            print(f"nsidx: {nsidx}")
            print(f"client: {client}")
            print(f"client.nodes.root: {client.nodes.root}")  # root as i=84
            print(f"client.nodes.root: {client.nodes.root!r}")
            print("Children of root are: ", await client.nodes.root.get_children())  # return list of nodes like [Node(i=85), Node(i=86), Node(i=87)]

            # Get a variable node using its browse path
            myvar: Node = await client.nodes.root.get_child(
                ["0:Objects", f"{nsidx}:MyObject", f"{nsidx}:MyVariable"]
            )
            mystr: Node = client.get_node(ua.NodeId("MyString", nsidx))
            myint16: Node = client.get_node(f"ns={nsidx};s=MyInt16")
            myint32: Node = client.get_node(f"ns={nsidx};s=MyInt32")

            # Read and print the value of MyVariable
            value: ua.DataValue = await myvar.read_data_value()
            value_str = await mystr.read_value()
            value_int16 = await myint16.read_value()
            value_int32 = await myint32.read_value()
            print(f"Initial MyVariable value: {value}")
            print(f"Initial MyString value: '{value_str}'")
            print(f"Initial MyInt16 value: {value_int16}")
            print(f"Initial MyInt32 value: {value_int32}")

            # Create a subscription
            handler = SubscriptionHandler()
            subscription = await client.create_subscription(100, handler)
            await subscription.subscribe_data_change(myvar)
            await subscription.subscribe_data_change(mystr)
            await subscription.subscribe_data_change(myint16)
            await subscription.subscribe_data_change(myint32)

            # Keep the client running to receive updates
            print("Subscribed to data changes. Waiting for 30 seconds...")
            await asyncio.sleep(30)

        except UaStatusCodeError as e:
            print(f"An error occurred: {e}")
            print("\nCall stack:")
            traceback.print_exc()

        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    try:
        print("Client starting...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Client stopped...")
