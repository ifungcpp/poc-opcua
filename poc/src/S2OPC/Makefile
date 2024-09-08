# Compiler and flags
INC_DIR :=
INC_DIR += -I /usr/local/include/s2opc/common
INC_DIR += -I /usr/local/include/s2opc/clientserver
INC_DIR += -I /usr/local/include/s2opc/pubsub

LIB_DIR :=
LIBS :=
LIBS += -Wl,--start-group
LIBS += -lpthread
LIBS += -lexpat
LIBS += -lmbedtls
LIBS += -lmbedx509
LIBS += -lmbedcrypto
LIBS += -ls2opc_common
LIBS += -ls2opc_clientserver
LIBS += -Wl,--end-group

CC := gcc
#CFLAGS := -g -O3 -m64 -Werror -Wall -Wextra -pedantic -fPIC -rdynamic -static # <= okay
CFLAGS := -g -O3 -m64 -Werror -Wall -Wextra -pedantic -fPIC -rdynamic

subscribe.x: subscribe.o
	$(CC) $(CFLAGS) $(LIB_DIR) -o subscribe.x subscribe.o $(LIBS)

subscribe.o: subscribe.c
	$(CC) $(CFLAGS) $(INC_DIR) -c subscribe.c

clean:
	rm -rf subscribe.o subscribe.x s2opc*logs
