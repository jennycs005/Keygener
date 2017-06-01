from socket import *
import os
serverName = 'localhost'
serverPort = 9999
clientSocket=socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
path = "/Users/ChunjieXu/Desktop/Publickeysnode0"
os.chdir(path)
while 1:
	data=clientSocket.recv(1024)
	filename=data[:data.find('\n')]
	with open(filename, 'wb') as f:
		f.write(data[data.find('\n'):])
		if not data:
			break
	with open(filename,'wb') as f:
		f.writelines(data[1:])
	f.close()
	print('Successfully get the file')

clientSocket.close()
print('connection closed')