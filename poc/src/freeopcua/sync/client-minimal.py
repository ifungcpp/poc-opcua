import time
from asyncua.sync import Client

if __name__ == "__main__":
    #with Client("opc.tcp://172.22.15.122:4840/freeopcua/server/") as client:
    # with Client("opc.tcp://127.0.0.1:4840/freeopcua/server/") as client:
    # with Client("opc.tcp://172.22.0.1:4840") as client:
    # with Client("opc.tcp://localhost:4840") as client:
    with Client("opc.tcp://172.22.15.122:4840") as client:
        while True:
            now = client.get_node("i=2258").read_data_value()
            if now is not None:
                print("now:", now.Value.Value)
            else:
                uri = "http://examples.freeopcua.github.io" # getting our namespace idx
                idx = client.get_namespace_index(uri)            
                var = client.nodes.root.get_child(["0:Objects", f"{idx}:MyObject", f"{idx}:MyVariable"]) # Now getting a variable node using its browse path
                val = var.read_data_value()
                print("now:", now.Value.Value, "var is:", var, "with value:", val.Value.Value) # now: 2024-06-23 03:26:22.175491 var is: ns=2;i=2 with value: 244.2999999999904
            time.sleep(1)