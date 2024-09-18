import asyncio
import logging
from asyncua import Client, ua
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

async def main():
    url = "opc.tcp://localhost:4840/freeopcua/server/"
    
    # Create client and set security
    _logger.info("Creating client")
    client = Client(url=url)

    _logger.info("Setting security")
    await client.set_security_string("Basic256Sha256,SignAndEncrypt,example_cert.der,example_private_key.pem")

    try:
        async with client:
            # Find the namespace index
            uri = 'http://examples.freeopcua.github.io'
            idx = await client.get_namespace_index(uri)

            # Get a specific node knowing its node id
            var = await client.nodes.root.get_child(["0:Objects", f"{idx}:MyObject", f"{idx}:MyVariable"])
            
            # Read and print the value of MyVariable
            value = await var.read_value()
            _logger.info(f"MyVariable value: {value}")

            # Write a new value to MyVariable
            new_value = 42.0
            await var.write_value(new_value)
            _logger.info(f"Wrote new value to MyVariable: {new_value}")

            # Read the value again to confirm the change
            value = await var.read_value()
            _logger.info(f"MyVariable new value: {value}")

            # Subscribe to changes
            handler = SubscriptionHandler()
            subscription = await client.create_subscription(1000, handler)
            await subscription.subscribe_data_change(var)

            # Run for 10 seconds
            _logger.info("Waiting for 10 seconds")
            await asyncio.sleep(10)
            _logger.info("Done waiting")

    except Exception as e:
        _logger.error(f"An error occurred: {e}")

class SubscriptionHandler:
    async def datachange_notification(self, node, val, data):
        _logger.info(f"New data change event: {node} {val}")

if __name__ == "__main__":
    asyncio.run(main())
