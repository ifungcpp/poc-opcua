import asyncio
import logging
from asyncua import Server, ua
from asyncua.crypto.permission_rules import SimpleRoleRuleset
from asyncua.server.user_managers import CertificateUserManager
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

async def main():
    # Setup server
    server = Server()
    await server.init()

    server.set_endpoint('opc.tcp://0.0.0.0:4840/freeopcua/server/')
    server.set_server_name("Secure OPC UA Server")

    # Setup security
    await server.load_certificate("example_cert.der")
    await server.load_private_key("example_private_key.pem")

    # Set security policy
    server.set_security_policy([SecurityPolicyBasic256Sha256],
                               permission_ruleset=SimpleRoleRuleset())

    # Setup user manager
    server.user_manager = CertificateUserManager()

    # Setup namespace
    uri = 'http://examples.freeopcua.github.io'
    idx = await server.register_namespace(uri)

    # Create a new node
    objects = server.nodes.objects
    myobj = await objects.add_object(idx, 'MyObject')
    myvar = await myobj.add_variable(idx, 'MyVariable', 6.7)
    await myvar.set_writable()

    _logger.info('Starting server!')
    async with server:
        while True:
            await asyncio.sleep(1)
            new_val = await myvar.get_value() + 0.1
            _logger.info('Set value of %s to %.1f', myvar, new_val)
            await myvar.write_value(new_val)

if __name__ == '__main__':
    asyncio.run(main())
