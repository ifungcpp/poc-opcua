#include <open62541/client_config_default.h>
#include <open62541/client_highlevel.h>
#include <open62541/plugin/log_stdout.h>
#include <iostream>
#include <thread>
#include <chrono>

// Subscription callback function
static void dataChangeHandler(UA_Client *client, UA_UInt32 subId, void *subContext,
                              UA_UInt32 monId, void *monContext, UA_DataValue *value) {
    UA_NodeId *nodeId = (UA_NodeId*)monContext;
    std::cout << "New data change event: Node " << nodeId->identifier.numeric << " = ";
    UA_Variant_print(&value->value, stdout);
    std::cout << std::endl;
}

int main() {
    UA_Client *client = UA_Client_new();
    UA_ClientConfig_setDefault(UA_Client_getConfig(client));

    // Connect to the server
    UA_StatusCode retval = UA_Client_connect(client, "opc.tcp://localhost:4840");
    if (retval != UA_STATUSCODE_GOOD) {
        std::cerr << "Failed to connect to the server" << std::endl;
        UA_Client_delete(client);
        return (int)retval;
    }

    // Get namespace index
    UA_UInt16 nsIndex;
    UA_String nsUri = UA_STRING("http://example.com/MyOPCUAServer/");
    retval = UA_Client_getNamespaceIndex(client, &nsUri, &nsIndex);
    if (retval != UA_STATUSCODE_GOOD) {
        std::cerr << "Failed to get namespace index" << std::endl;
        UA_Client_delete(client);
        return (int)retval;
    }

    std::cout << "Namespace index: " << nsIndex << std::endl;

    // Define node IDs
    UA_NodeId myVarId = UA_NODEID_STRING(nsIndex, (char*)"MyVariable");
    UA_NodeId myStrId = UA_NODEID_STRING(nsIndex, (char*)"MyString");
    UA_NodeId myIntId = UA_NODEID_STRING(nsIndex, (char*)"MyInt");

    // Read initial values
    UA_Variant value;
    UA_Variant_init(&value);

    retval = UA_Client_readValueAttribute(client, myVarId, &value);
    if (retval == UA_STATUSCODE_GOOD) {
        std::cout << "Initial MyVariable value: ";
        UA_Variant_print(&value, stdout);
        std::cout << std::endl;
    }
    UA_Variant_clear(&value);

    retval = UA_Client_readValueAttribute(client, myStrId, &value);
    if (retval == UA_STATUSCODE_GOOD) {
        std::cout << "Initial MyString value: ";
        UA_Variant_print(&value, stdout);
        std::cout << std::endl;
    }
    UA_Variant_clear(&value);

    retval = UA_Client_readValueAttribute(client, myIntId, &value);
    if (retval == UA_STATUSCODE_GOOD) {
        std::cout << "Initial MyInt value: ";
        UA_Variant_print(&value, stdout);
        std::cout << std::endl;
    }
    UA_Variant_clear(&value);

    // Create subscription
    UA_CreateSubscriptionRequest request = UA_CreateSubscriptionRequest_default();
    UA_CreateSubscriptionResponse response = UA_Client_Subscriptions_create(client, request,
                                                                            nullptr, nullptr, nullptr);

    // Add monitored items
    UA_MonitoredItemCreateRequest monRequest = UA_MonitoredItemCreateRequest_default(myVarId);
    UA_MonitoredItemCreateResult monResponse = 
        UA_Client_MonitoredItems_createDataChange(client, response.subscriptionId,
                                                  UA_TIMESTAMPSTORETURN_BOTH, monRequest,
                                                  &myVarId, dataChangeHandler, nullptr);

    monRequest = UA_MonitoredItemCreateRequest_default(myStrId);
    monResponse = 
        UA_Client_MonitoredItems_createDataChange(client, response.subscriptionId,
                                                  UA_TIMESTAMPSTORETURN_BOTH, monRequest,
                                                  &myStrId, dataChangeHandler, nullptr);

    monRequest = UA_MonitoredItemCreateRequest_default(myIntId);
    monResponse = 
        UA_Client_MonitoredItems_createDataChange(client, response.subscriptionId,
                                                  UA_TIMESTAMPSTORETURN_BOTH, monRequest,
                                                  &myIntId, dataChangeHandler, nullptr);

    std::cout << "Subscribed to data changes. Waiting for 30 seconds..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(30));

    // Clean up
    UA_Client_disconnect(client);
    UA_Client_delete(client);
    return 0;
}
