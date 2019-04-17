#RSA CLIENT

#The client recieves n and e
#These are used to encrypt plaintext
#Cipher = (Plaintext^e)modn
#Send to Server

import socket

cli = socket.socket()
cli.connect(("127.0.0.1",7003))
print "Connected to server."

msg = cli.recv(1024).split("&")
n = int(msg[0])
e = int(msg[1])
print "Public key recieved: ",n,e

Plaintext = 23
print "Sending Plaintext: ",Plaintext

Cipher = pow(Plaintext,e,n)

cli.send(str(Cipher).encode())

cli.close()
print "Connection closed."
