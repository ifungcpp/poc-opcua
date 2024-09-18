from asyncua import ua
from asyncua.sync import Client

def show_endpoint(endpoints):
    print(f"Found {len(endpoints)} endpoint(s):")
    for i, endpoint in enumerate(endpoints, 1):
        print(f"\nEndpoint {i}:")
        print(f"  Endpoint URL: {endpoint.EndpointUrl}")
        print(f"  Security Mode: {endpoint.SecurityMode.name}")
        print(f"  Security Policy: {endpoint.SecurityPolicyUri}")
        print(f"  Transport Profile URI: {endpoint.TransportProfileUri}")
        print(f"  Security Level: {endpoint.SecurityLevel}")
        
        if endpoint.ServerCertificate:
            print(f"  Server Certificate: {len(endpoint.ServerCertificate)} bytes")
        else:
            print("  Server Certificate: None")
        
        print("  User Identity Tokens:")
        for token in endpoint.UserIdentityTokens:
            print(f"    - Policy ID: {token.PolicyId}")
            print(f"      Token Type: {token.TokenType}")  # Anonymous = 0 UserName = 1 Certificate = 2 IssuedToken = 3
            print(f"      Issued Token Type: {token.IssuedTokenType}")
            print(f"      Issuer Endpoint URL: {token.IssuerEndpointUrl}")
            print(f"      Security Policy URI: {token.SecurityPolicyUri}")
        
        print(f"  Server URI: {endpoint.Server.ApplicationUri}")
        print(f"  Product URI: {endpoint.Server.ProductUri}")
        print(f"  Application Name: {endpoint.Server.ApplicationName.Text}")
        print(f"  Application Type: {endpoint.Server.ApplicationType.name}")
        print(f"  Gateway Server URI: {endpoint.Server.GatewayServerUri}")
        print(f"  Discovery Profile URI: {endpoint.Server.DiscoveryProfileUri}")
        print(f"  Discovery URLs: {', '.join(endpoint.Server.DiscoveryUrls)}")

def find_endpoints(server_url):
    try:
        # We don't need to connect for this operation
        print(f"Discovering endpoints for server at {server_url}")

        # Use the GetEndpoints service
        client = Client(url=server_url)
        endpoints = client.connect_and_get_server_endpoints()
        client.disconnect()
        
        if not endpoints:
            print("No endpoints found.")
        else:
            show_endpoint(endpoints)

    except ua.UaError as e:
        print(f"An error occurred: {e}")

def main():
    # Replace with your OPC UA server URL
    server_url = "opc.tcp://localhost:4840"
    find_endpoints(server_url)

if __name__ == "__main__":
    main()