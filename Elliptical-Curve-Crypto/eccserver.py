#Elliptical Curve Cryptography
#User 1 = A
#User 2 = B
#Server


#Find points on the ellipse that satisfy condition = G
#Select two private keys A=a,B=b
#Private key A -> Pa = a*G and B->Pb = b*G
#Share this with each other
#Encrypt Pm -> Cipher = [xG,Pm+xPb]
#Send to B
#B decrypts it with Pm = Pm+xPb-xbG

import math

a = int(input("Enter a:"))
b = int(input("Enter b:"))

def points(a,b):
	if 4*(a**3)+27*(b**2) != 0:
		x=1
		while True:
			lhs = x**3+a*x**2+b
			y = math.sqrt(lhs)
			if lhs == y**2:
				return x,y
			else:
				x=x+1
	else:
		print 'Select other nos'

#G
x,y = points(a,b)
print x,y

#Select a secret key
a = int(input("Enter A's secret key: "))

#A's public key = aG
Pa =  [a*x,a*y]

print "A's public key:",Pa

#Plaintext message
Pm = int(input("Enter plaintext: "))
#Choose random number k
k = int(input("Enter a random number x: "))

#Get B's public key
import socket 
serv = socket.socket()
serv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
serv.bind(('127.0.0.1',8021))
serv.listen(10)
try:
	while True:
		con,addr = serv.accept()
		print "Connected at ",con
		#send G
		msgG = str(x)+"&"+str(y)
		print "Sending",msgG
		con.send(str(msgG).encode())
		#get Pb
		Pb1,Pb2 = con.recv(100).split('&')
		print "B's public key: ",Pb1,Pb2
		#encrypt message
		cipher1 = k*x+k*y
		cipher2 = Pm+k*float(Pb1)+k*float(Pb2)
		cipher = str(cipher1)+"&"+str(cipher2)
		con.send(cipher.encode())
		print "Sending cipher ",cipher
		con.close()


except KeyboardInterrupt:
	serv.close()
