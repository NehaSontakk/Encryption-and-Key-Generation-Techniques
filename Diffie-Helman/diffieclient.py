# Client
# Bob
# Bob gets P,G from public space
# Bob also selects a large integer b
# Bob calculates B = (G^b)modP
# Bob recieves A from alice
# Bobs secret key = (A^b)modP
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

cli = socket.socket()
#cli.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
cli.connect(('127.0.0.1',8112))

#choose b
b = getrandbits(32)
#Make B key
B = pow(G,b,P)
cli.send(str(B).encode())
#get A from Alice
A = int(cli.recv(32))
B_secret = pow(A,b,P)
print B_secret
cli.close()
