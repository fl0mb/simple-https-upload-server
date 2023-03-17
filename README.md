# Simple-Https-Upload-Server
Simple python server to upload files to over https.

Create certs first and reference them in L40 of server.py:
```
openssl req -x509 -days 365 -newkey rsa:4048 -keyout pkey.pem -out cert.crt -nodes
```
(keep in mind the private key will not be encrypted)

Upoad a file with:

```
curl -k https://<ip>:8080/<filename> --data-binary  @/path/to/file
```

**Use with caution, this is highly insecure!**
