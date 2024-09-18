import logging
from asyncua import ua
from asyncua.sync import Client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def show_endpoint(endpoints):
    logging.info(f"Found {len(endpoints)} endpoint(s):")
    for i, endpoint in enumerate(endpoints, 1):
        logging.info(f"\nEndpoint {i}:")
        logging.info(f"  Endpoint URL: {endpoint.EndpointUrl}")
        logging.info(f"  Security Mode: {endpoint.SecurityMode.name}")
        logging.info(f"  Security Policy: {endpoint.SecurityPolicyUri}")
        logging.info(f"  Transport Profile URI: {endpoint.TransportProfileUri}")
        logging.info(f"  Security Level: {endpoint.SecurityLevel}")
        
        if endpoint.ServerCertificate:
            logging.info(f"  Server Certificate: {len(endpoint.ServerCertificate)} bytes")
        else:
            logging.info("  Server Certificate: None")
        
        logging.info("  User Identity Tokens:")
        for token in endpoint.UserIdentityTokens:
            logging.info(f"    - Policy ID: {token.PolicyId}")
            logging.info(f"      Token Type: {token.TokenType}")  # Anonymous = 0 UserName = 1 Certificate = 2 IssuedToken = 3
            logging.info(f"      Issued Token Type: {token.IssuedTokenType}")
            logging.info(f"      Issuer Endpoint URL: {token.IssuerEndpointUrl}")
            logging.info(f"      Security Policy URI: {token.SecurityPolicyUri}")
        
        logging.info(f"  Server URI: {endpoint.Server.ApplicationUri}")
        logging.info(f"  Product URI: {endpoint.Server.ProductUri}")
        logging.info(f"  Application Name: {endpoint.Server.ApplicationName.Text}")
        logging.info(f"  Application Type: {endpoint.Server.ApplicationType.name}")
        logging.info(f"  Gateway Server URI: {endpoint.Server.GatewayServerUri}")
        logging.info(f"  Discovery Profile URI: {endpoint.Server.DiscoveryProfileUri}")
        logging.info(f"  Discovery URLs: {', '.join(endpoint.Server.DiscoveryUrls)}")

def find_endpoints(server_url):
    try:
        # We don't need to connect for this operation
        logging.info(f"Discovering endpoints for server at {server_url}")

        # Use the GetEndpoints service
        client = Client(url=server_url)
        endpoints = client.connect_and_get_server_endpoints()
        client.disconnect()
        
        if not endpoints:
            logging.info("No endpoints found.")
        else:
            show_endpoint(endpoints)

    except ua.UaError as e:
        logging.error(f"An error occurred: {e}")

def main():
    # Replace with your OPC UA server URL
    server_url = "opc.tcp://localhost:4840"
    find_endpoints(server_url)

if __name__ == "__main__":
    main()