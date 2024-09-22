const opcua = require("node-opcua");

async function main() {
  const client = opcua.OPCUAClient.create({
    endpointMustExist: false,
  });

  try {
    // Step 1: Connect to the server
    await client.connect("opc.tcp://172.22.0.1:4840");
    console.log("Connected to OPC UA server");

    // Step 2: Create session
    const session = await client.createSession();

    // Step 3: Read the current time
    const nodeId = opcua.resolveNodeId("ns=0;i=2258"); // Server_ServerStatus_CurrentTime
    const dataValue = await session.read({ nodeId: nodeId, attributeId: opcua.AttributeIds.Value });

    // Step 4: Print the result
    if (dataValue.statusCode.isGood()) {
      console.log("Date is:", dataValue.value.value.toUTCString());
    } else {
      console.log("Error reading date:", dataValue.statusCode.toString());
    }

    // Step 5: Close session and disconnect
    await session.close();
    await client.disconnect();

  } catch (err) {
    console.error("An error occurred:", err.message);
  }
}

main();