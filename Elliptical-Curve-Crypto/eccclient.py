#User 2 : B
#Decide a private key b
#get x,y from A
#make a public key
#Pb = bG
#send Pb to A
#get ciphertext from A
#decrypt with private key
#Pm = Pm+Pbx - bxG

b = int(input("Enter B's private key: "))
import socket

cli = socket.socket()
cli.connect(('127.0.0.1',8021))

x,y = cli.recv(1024).split('&')
print "Recieved G: ",x,y

Pb1=float(x)*b
Pb2=float(y)*b
msgPb = str(Pb1)+"&"+str(Pb2)
cli.send(str(msgPb).encode())
cipher1,cipher2 = cli.recv(1024).split("&")
print "Recieved cipher: ",cipher1,cipher2

#decrypt recieved cipher
decrypt1 = float(cipher1)*b
plaintext = float(cipher2)-decrypt1
print "The plaintext is: ",plaintext
cli.close()
