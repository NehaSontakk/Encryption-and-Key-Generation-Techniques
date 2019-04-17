#RSA SERVER

import math
import socket

#Choose two numbers a,b
#a,b prime and not equal

a = int(input("Enter a prime number: "))
b = int(input("Enter another prime number: "))

def checkprime(num):
	numroo = int(math.sqrt(num))
	for i in range(2,numroo):
		if num%i == 0:
			return False
	return True

if a!=b:
	print "Are the numbers selected correct: ",checkprime(a),checkprime(b)

#Modulus number for rsa
n = a*b
#Phi function is a multiplication of coprimes to a,b 
#since a,b are prime their coprimes are a-1,b-1
phi = (a-1)*(b-1)

#We need to select an e now
#e is a number coprime to phi and less than phi
e_list = []
for i in range(2,phi):
	if phi%i != 0:
		e_list.append(i)
print e_list

e = int(input("Choose an e: "))

#Send n and e to client
#Get ciphertext from client
#decrypt ciphertext
#To decrypt we need 'd'

#d = phi*i+1 / e, keep going till d is not float

for i in range(1,phi):
	num = phi*i+1
	if num%e == 0:
		d = num/e

print "decryption key: ",d

#now that we have everything let's send it to client

serv = socket.socket()
serv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
serv.bind(("127.0.0.1",7003))
print "Connected to localhost."
serv.listen(10)
print "Listening.."

try:
	while True:
		con,addr = serv.accept()
		print "Connected at ",addr
		msg = str(n)+"&"+str(e)
		con.send(msg.encode())
		cipher = int(con.recv(1024))
		plaintext = pow(cipher,d,n)
		print "Recieved Plaintext is: ",plaintext
		con.close()

except KeyboardInterrupt:
	serv.close()
