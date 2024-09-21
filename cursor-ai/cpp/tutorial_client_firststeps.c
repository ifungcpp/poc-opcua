#include <open62541/client_config_default.h>
#include <open62541/client_highlevel.h>
#include <open62541/plugin/log_stdout.h>

int main(void) {
    UA_Client *client = UA_Client_new();
    UA_ClientConfig_setDefault(UA_Client_getConfig(client));
    UA_StatusCode retval = UA_Client_connect(client, "opc.tcp://172.22.0.1:4840");
    if(retval != UA_STATUSCODE_GOOD) {
        UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND,
                    "The connection failed with status code %s",
                    UA_StatusCode_name(retval));
        UA_Client_delete(client);
        return 0;
    }

    UA_Variant value; 
    UA_Variant_init(&value);

    const UA_NodeId nodeId = UA_NS0ID(SERVER_SERVERSTATUS_CURRENTTIME);
    retval = UA_Client_readValueAttribute(client, nodeId, &value);

    if(retval == UA_STATUSCODE_GOOD &&
       UA_Variant_hasScalarType(&value, &UA_TYPES[UA_TYPES_DATETIME])) {
        UA_DateTime raw_date = *(UA_DateTime *) value.data;
        UA_DateTimeStruct dts = UA_DateTime_toStruct(raw_date);
        UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND,
                    "date is: %u-%u-%u %u:%u:%u.%03u",
                    dts.day, dts.month, dts.year, dts.hour,
                    dts.min, dts.sec, dts.milliSec);
    } else {
        UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND,
                    "Reading the value failed with status code %s",
                    UA_StatusCode_name(retval));
    }

    UA_Variant_clear(&value);
    UA_Client_delete(client);
    return 0;
}
