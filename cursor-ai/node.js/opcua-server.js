const opcua = require("node-opcua");

const server = new opcua.OPCUAServer({
    port: 4840,
    resourcePath: "/myopcua/server/",
    buildInfo: {
        productName: "Node.js OPC UA Server",
        buildNumber: "1",
        buildDate: new Date()
    }
});

function post_initialize() {
    console.log("Server initialized");
    
    const addressSpace = server.engine.addressSpace;
    
    // Register the custom namespace
    const customNamespaceUri = "http://example.com/MyOPCUAServer/";
    const namespace = addressSpace.registerNamespace(customNamespaceUri);

    // Create a new object
    const myObject = namespace.addObject({
        organizedBy: addressSpace.rootFolder.objects,
        browseName: "MyObject",
        nodeId: `ns=${namespace.index};s=MyObject`
    });

    // Add a variable to the object
    let myVariable = namespace.addVariable({
        componentOf: myObject,
        browseName: "MyVariable",
        dataType: "Double",
        nodeId: `ns=${namespace.index};s=MyVariable`,
        minimumSamplingInterval: 1000,
        value: {
            get: function () {
                return new opcua.Variant({
                    dataType: opcua.DataType.Double,
                    value: Math.random() * 100
                });
            }
        }
    });

    // Change the variable value every second
    setInterval(() => {
        myVariable.setValueFromSource(new opcua.Variant({
            dataType: opcua.DataType.Double,
            value: Math.random() * 100
        }));
    }, 1000);

    console.log(`Server namespace index: ${namespace.index}`);
    console.log(`Custom namespace URI: ${customNamespaceUri}`);
}

server.initialize(post_initialize);

server.start(() => {
    console.log("Server is now listening ... (press CTRL+C to stop)");
    console.log("Port:", server.endpoints[0].port);
    const endpointUrl = server.endpoints[0].endpointDescriptions()[0].endpointUrl;
    console.log("Endpoint URL:", endpointUrl);
});
