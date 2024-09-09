import asyncio
from asyncua import Server, ua


async def main():
    # Create a new server
    server = Server()

    # Set the endpoint URL
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/myopcua/server/")

    # Set up our own namespace
    uri = "http://example.com/MyOPCUAServer/";
    idx = await server.register_namespace(uri)

    # Create a new object
    myobj = await server.nodes.objects.add_object(f"ns={idx};s=MyObject", "MyObject")

    # Create a variable
    myvar = await myobj.add_variable(f"ns={idx};s=MyVariable", "MyVariable", 6.7)

    # Set MyVariable to be writable by clients
    await myvar.set_writable()

    async with server:
        while True:
            await asyncio.sleep(1)
            new_val = await myvar.get_value() + 0.1
            await myvar.write_value(new_val)
            print(f"MyVariable = {new_val:.3f}, {myvar}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped...")
