import asyncio
from asyncua import Server, ua, Node


async def main():
    # Create a new server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/myopcua/server/")

    # Set the endpoint URL
    await server.init()

    # Set up our own namespace
    uri = "http://example.com/MyOPCUAServer/";
    idx = await server.register_namespace(uri)

    # Create a new object
    myobj: Node = await server.nodes.objects.add_object(f"ns={idx};s=MyObject", f"{idx}:MyObject")

    # Create a variable
    myvar: Node = await myobj.add_variable(f"ns={idx};s=MyVariable", f"{idx}:MyVariable", 6.7, ua.VariantType.Float)
    myint: Node = await myobj.add_variable(f"ns={idx};s=MyInt16", f"{idx}:MyInt16", 0, ua.VariantType.Int16)
    await myobj.add_variable(f"ns={idx};s=MyInt32", f"{idx}:MyInt32", 0, ua.VariantType.Int32)
    await myobj.add_variable(f"ns={idx};s=MyInt64", f"{idx}:MyInt64", 0, ua.VariantType.Int64)
    await myobj.add_variable(f"ns={idx};s=MyString", f"{idx}:MyString", '', ua.VariantType.String)

    # Set MyVariable to be writable by clients
    await myvar.set_writable()

    # Infinite loop to continuously update the variable
    async with server:
        while True:
            await asyncio.sleep(1)
            new_val = await myvar.get_value() + 0.1
            await myint.write_value(int(new_val), ua.VariantType.Int16)
            await myvar.write_value(new_val, ua.VariantType.Float)
            print(f"{myvar}, MyVariable = {new_val:.3f}")


if __name__ == "__main__":
    try:
        print("Server starting...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped...")
