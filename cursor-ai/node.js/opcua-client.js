const opcua = require("node-opcua");

async function main() {
    const client = opcua.OPCUAClient.create({
        endpoint_must_exist: false
    });

    const endpointUrl = "opc.tcp://localhost:4840/myopcua/server/";
    const customNamespaceUri = "http://example.com/MyOPCUAServer/";

    try {
        // Step 1: Connect to the server
        await client.connect(endpointUrl);
        console.log("Connected to server");

        // Step 2: Create session
        const session = await client.createSession();
        console.log("Session created");

        // Step 3: Read the namespace array and find the index of our custom namespace
        const namespaceArray = await session.readNamespaceArray();
        console.log("Available namespaces:");
        namespaceArray.forEach((ns, index) => console.log(`${index}: ${ns}`));

        const namespaceIndex = namespaceArray.indexOf(customNamespaceUri);
        if (namespaceIndex === -1) {
            throw new Error(`Custom namespace ${customNamespaceUri} not found`);
        }
        console.log(`Custom namespace index: ${namespaceIndex}`);

        // Step 4: Read a variable
        // Read using nodeId
        const nodeId = `ns=${namespaceIndex};s=MyVariable`;
        const dataValue1 = await session.read({ nodeId: nodeId, attributeId: opcua.AttributeIds.Value });
        console.log(`Initial value of MyVariable (using nodeId) = ${dataValue1.value.value}`);

        // Step 5: Create subscription
        const subscription = await session.createSubscription2({
            requestedPublishingInterval: 1000,
            requestedLifetimeCount: 100,
            requestedMaxKeepAliveCount: 10,
            maxNotificationsPerPublish: 100,
            publishingEnabled: true,
            priority: 10
        });

        subscription.on("started", () => console.log("Subscription started"));

        // Step 6: Install monitored item
        const itemToMonitor = {
            nodeId: nodeId,
            attributeId: opcua.AttributeIds.Value
        };
        const parameters = {
            samplingInterval: 100,
            discardOldest: true,
            queueSize: 10
        };

        const monitoredItem = await subscription.monitor(itemToMonitor, parameters, opcua.TimestampsToReturn.Both);

        monitoredItem.on("changed", (dataValue) => {
            console.log(`MyVariable changed: ${dataValue.value.value}`);
        });

        // Keep the client running for 30 seconds
        await new Promise(resolve => setTimeout(resolve, 30000));

        // Step 7: Close session and disconnect
        await session.close();
        await client.disconnect();
        console.log("Session closed and disconnected");

    } catch (err) {
        console.error("An error occurred:", err);
    }
}

main();
