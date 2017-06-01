import os
import socket
import threading
import shutil


def newpiinit(piname):

	#piname=raw_input('Please enter the Pi Name (5 letters):')
	path="/Users/ChunjieXu/Desktop/Publickeys"
	files=os.listdir(path)

	if piname in files:
		print('Name exists, please enter a new name.')
	else:
		os.chdir('/Users/ChunjieXu/Desktop/Allkeys')
		os.makedirs(piname)
		os.chdir(piname)
		os.system('openssl req -new -x509 -keyout ./cakey.pem -out cacert.pem -days 365')
		os.system('cp cakey.pem cakey.pem.enc')
		os.system('openssl rsa -in ./cakey.pem.enc -out ./cakey.pem')
		os.system('openssl rsa -in ./cakey.pem.enc -passin pass:1234 -pubout -out ./capublickey.pem')
		for old_name in os.listdir('.'):
    		#curpath=os.getcwd()
    		#folder_name=os.path.basename(curpath)
			prefix=piname
			new_name=prefix+old_name
			os.rename(old_name,new_name)
		for keys in os.listdir('.'):
			result=piname+'capublickey.pem'
			shutil.copy(result,path)

socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address=('localhost', 9999)
socket.bind(server_address)
socket.listen(1)
print 'This server is ready for connection'
connectionSocket,addr=socket.accept()
print 'Got connection from ', addr

while 1:
	piname=raw_input('Please enter the Pi Name (5 letters):')
	newpiinit(piname)
	path="/Users/ChunjieXu/Desktop/Publickeys"
	os.chdir(path)
	connectionSocket.send(piname+'capublickey.pem\n')
	filename=piname+'capublickey.pem'
	with open(filename,'rb') as f:
		for data in f:
			connectionSocket.sendall(data)
			if not data:
				break
	f.close()			
	print 'Send key', filename
connectionSocket.close()
print 'Connection closed'

