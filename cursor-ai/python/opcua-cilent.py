import asyncio
import traceback
from asyncua import Client, Node, ua
from asyncua.ua.uaerrors import UaStatusCodeError
from asyncua.common.subscription import DataChangeNotificationHandler, DataChangeNotif

class SubscriptionHandler(DataChangeNotificationHandler):
    async def datachange_notification(self, node: Node, val, data: DataChangeNotif):
        print("New data change event:")
        print(f"  Node: {node}")
        print(f"  Value: {val}")
        print(f"  Data Type: {type(val).__name__}")
        print(f"  Status: {data.monitored_item.Value.StatusCode.name}")
        print(f"  Source Timestamp: {data.monitored_item.Value.SourceTimestamp}")
        print(f"  Server Timestamp: {data.monitored_item.Value.ServerTimestamp}")

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
            myint: Node = client.get_node(f"ns={nsidx};s=MyInt")
            myint16: Node = client.get_node(f"ns={nsidx};s=MyInt16")
            myint32: Node = client.get_node(f"ns={nsidx};s=MyInt32")
            myint64: Node = client.get_node(f"ns={nsidx};s=MyInt64")
            myfloat: Node = client.get_node(f"ns={nsidx};s=MyFloat")
            mydouble: Node = client.get_node(f"ns={nsidx};s=MyDouble")

            # Read and print the value of MyVariable
            value_var: ua.DataValue = await myvar.read_data_value()
            value_str: ua.DataValue = await mystr.read_data_value()
            value_int: ua.DataValue = await myint.read_data_value()
            print(f"\n Initial MyVariable value: {value_var}")
            print(f"\n Initial MyString value: '{value_str}'")
            print(f"\n Initial MyInt value: {value_int}")
            print(f"\n ... MyInt node: {myint}")
            print(f"\n ... MyInt value: {value_int.Value.Value}")
            print(f"\n ... MyInt type: {value_int.Value.VariantType.name}")
            print(f"\n ... MyInt status: {value_int.StatusCode.name}")
            print(f"\n ... MyInt source timestamp: {value_int.SourceTimestamp}")
            print(f"\n ... MyInt server timestamp: {value_int.ServerTimestamp}")
            print("\n")

            # Create a subscription
            handler = SubscriptionHandler()
            subscription = await client.create_subscription(100, handler)
            await subscription.subscribe_data_change(myvar)
            await subscription.subscribe_data_change(mystr)
            await subscription.subscribe_data_change(myint)
            await subscription.subscribe_data_change(myint16)
            await subscription.subscribe_data_change(myint32)
            await subscription.subscribe_data_change(myint64)
            await subscription.subscribe_data_change(myfloat)
            await subscription.subscribe_data_change(mydouble)

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
