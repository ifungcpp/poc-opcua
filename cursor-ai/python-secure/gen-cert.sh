openssl req -x509 -newkey rsa:2048 -keyout example_private_key.pem -out example_cert.pem -days 365 -nodes
openssl x509 -outform der -in example_cert.pem -out example_cert.der