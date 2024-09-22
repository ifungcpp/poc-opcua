import asyncio
from asyncua import Client, ua

async def main():
    async with Client("opc.tcp://172.22.0.1:4840") as client:
        try:
            await client.connect()
            print("Connected to OPC UA server")

            node_id = ua.NodeId(ua.ObjectIds.Server_ServerStatus_CurrentTime)
            value = await client.get_node(node_id).read_value()
            print("Date is:", value)  # Date is: 2024-09-22 15:53:26.810859+00:00

        except Exception as e:
            print("The connection failed:", e)

if __name__ == "__main__":
    asyncio.run(main())
