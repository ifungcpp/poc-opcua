#include <cstdio>

/* sleep_ms */
#ifdef _WIN32
# include <synchapi.h>
# define sleep_ms(ms) Sleep(ms)
#else
# include <unistd.h>
# define sleep_ms(ms) usleep(ms * 1000)
#endif

#include <open62541/client_config_default.h>
#include <open62541/client_highlevel.h>
#include <open62541/client_subscriptions.h>
#include <open62541/plugin/log_stdout.h>

static void
handler_currentTimeChanged(UA_Client *client, UA_UInt32 subId, void *subContext,
                           UA_UInt32 monId, void *monContext, UA_DataValue *value) {
    UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND, "currentTime has changed!");
    if(UA_Variant_hasScalarType(&value->value, &UA_TYPES[UA_TYPES_DATETIME])) {
        UA_DateTime raw_date = *(UA_DateTime *) value->value.data;
        UA_DateTimeStruct dts = UA_DateTime_toStruct(raw_date);
        UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND,
                    "date is: %02u-%02u-%04u %02u:%02u:%02u.%03u",
                    dts.day, dts.month, dts.year, dts.hour, dts.min, dts.sec, dts.milliSec);
    }
}

static void
deleteSubscriptionCallback(UA_Client *client, UA_UInt32 subscriptionId, void *subscriptionContext) {
    UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND,
                "Subscription Id %u was deleted", subscriptionId);
}

class OPCUA_Client {
public:
    OPCUA_Client() : m_client(UA_Client_new()) {
        UA_ClientConfig_setDefault(UA_Client_getConfig(m_client));
    }

    ~OPCUA_Client() {
        UA_Client_delete(m_client);
    }

    UA_StatusCode connect(const char* endpoint) {
        return UA_Client_connect(m_client, endpoint);
    }

    UA_StatusCode disconnect() {
        return UA_Client_disconnect(m_client);
    }

    UA_SessionState getState() {
        UA_SessionState ss;
        UA_Client_getState(m_client, NULL, &ss, NULL);
        UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND, "Session state: %s", UA_SessionState_name(ss));
        return ss;
    }

    void runIterate(int msec) {
        UA_Client_run_iterate(m_client, msec);
    }

    bool readServerTime() {
        UA_Variant value;
        UA_Variant_init(&value);

        const UA_NodeId nodeId = UA_NODEID_NUMERIC(0, UA_NS0ID_SERVER_SERVERSTATUS_CURRENTTIME);
        UA_StatusCode retval = UA_Client_readValueAttribute(m_client, nodeId, &value);

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
        return retval == UA_STATUSCODE_GOOD;
    }

    UA_StatusCode subscribeServerTime() {
        UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND, "A session with the server is activated");
        /* A new session was created. We need to create the subscription. */
        /* Create a subscription */
        UA_CreateSubscriptionRequest request = UA_CreateSubscriptionRequest_default();
        UA_CreateSubscriptionResponse response =
            UA_Client_Subscriptions_create(m_client, request, NULL, NULL, deleteSubscriptionCallback);
        if(response.responseHeader.serviceResult == UA_STATUSCODE_GOOD)
            UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND,
                        "Create subscription succeeded, id %u",
                        response.subscriptionId);
        else
            return response.responseHeader.serviceResult;

        /* Add a MonitoredItem */
        UA_NodeId currentTimeNode =
            UA_NODEID_NUMERIC(0, UA_NS0ID_SERVER_SERVERSTATUS_CURRENTTIME);
        UA_MonitoredItemCreateRequest monRequest =
            UA_MonitoredItemCreateRequest_default(currentTimeNode);

        UA_MonitoredItemCreateResult monResponse =
            UA_Client_MonitoredItems_createDataChange(m_client, response.subscriptionId,
                                                        UA_TIMESTAMPSTORETURN_BOTH, monRequest,
                                                        NULL, handler_currentTimeChanged, NULL);
        if(monResponse.statusCode == UA_STATUSCODE_GOOD)
            UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND,
                        "Monitoring UA_NS0ID_SERVER_SERVERSTATUS_CURRENTTIME', id %u",
                        monResponse.monitoredItemId);
        return monResponse.statusCode;
    }

    static const char * UA_SessionState_name(UA_SessionState ss) {
        switch (ss) {
        case UA_SESSIONSTATE_CLOSED: return "UA_SESSIONSTATE_CLOSED";
        case UA_SESSIONSTATE_CREATE_REQUESTED: return "UA_SESSIONSTATE_CREATE_REQUESTED";
        case UA_SESSIONSTATE_CREATED: return "UA_SESSIONSTATE_CREATED";
        case UA_SESSIONSTATE_ACTIVATE_REQUESTED: return "UA_SESSIONSTATE_ACTIVATE_REQUESTED";
        case UA_SESSIONSTATE_ACTIVATED: return "UA_SESSIONSTATE_ACTIVATED";
        case UA_SESSIONSTATE_CLOSING: return "UA_SESSIONSTATE_CLOSING";
        default: return "UA_SESSIONSTATE_Unknown";
        }
    }

private:
    UA_Client *m_client;
};

int main() 
{
    OPCUA_Client client;
    bool subOkay = false;

    while (true)
    {
        UA_StatusCode retval = UA_STATUSCODE_GOOD;

        if (client.getState() != UA_SESSIONSTATE_ACTIVATED)
        {
            retval = client.connect("opc.tcp://172.22.0.1:48400");
            if (retval == UA_STATUSCODE_GOOD) 
            {
                client.subscribeServerTime();
                subOkay = true;
            }
        }
        if (retval != UA_STATUSCODE_GOOD) 
        {
            UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND,
                        "The connection failed with status code %s",
                        UA_StatusCode_name(retval));
            sleep_ms(1000);
        }
        else
        {
            if (subOkay || client.readServerTime())
            {
                client.runIterate(1000);
            }
            else
            {
                // sudo iptables -A INPUT -p tcp --dport 48400 -j DROP
                // sudo iptables -A OUTPUT -p tcp --dport 48400 -j DROP
                // sudo iptables -D OUTPUT -p tcp --dport 48400 -j DROP
                client.disconnect();
            }
            sleep_ms(1000);
        }
    }
    return 0;
}
