openssl req -nodes -config openssl.cnf -x509 -newkey rsa:4096 -keyout testkey.pem -out testcert.pem -days 99999