# Diffie Hellman Key Exchange
# Server = Alice
# Agree on P,G
# choose a
# Calculate A = (G^a)modP
# Send A to Bob
# Get B from Bob
# The secret key will be = (B^a)modP
import math
import socket
from random import getrandbits
from public_space import P,G

def primecheck(num):
	num_root = int(math.sqrt(num))
	for i in range(2,num_root):
		if num%i == 0:
			return False
	return True

print "Are P,G prime: ",primecheck(P),primecheck(G)

serv = socket.socket()
serv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
serv.bind(('127.0.0.1',8112))
print "Connected to localhost"
serv.listen(10)
print "listening..."

try:
	while True:
		con,addr = serv.accept()
		print "Connection established: ",con
		#Select a
		a = getrandbits(32)
		#Make key A
		A = pow(G,a,P)
		#Send A to Bob
		con.send(str(A).encode())
		#Get B from Bob
		B = int(con.recv(32))
		#Make secret key
		A_secret = pow(B,a,P)
		print A_secret
		con.close()

except KeyboardInterrupt:
	serv.close()
