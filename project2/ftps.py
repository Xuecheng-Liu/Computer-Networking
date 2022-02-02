import select, socket, sys

fileToHost = {}
files = []
HOST = 'localhost'
PORT = 5015
clientsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
clientsock.bind((HOST,PORT))
print ("waiting for packets...")

inputs = [clientsock, sys.stdin]

while inputs:
    readable, writable, exceptional = select.select(inputs, inputs, inputs)
    for s in readable:
        if s is not sys.stdin: # only handles socket
            data,addr = clientsock.recvfrom(1024)
            print("get connection from "+ str(addr)) # for debugging purpose
	    msg =  data #decode byte to string
	    print(msg) # for debugging purpose
	    if msg[0:5] == "Share":
	      sharedFiles = msg[6:].split(" ") #get file names
	      print(sharedFiles) #for debugging
	      files.extend(sharedFiles) #keep track of all files
	      for f in sharedFiles:
		fileToHost[f] = addr
	      print(fileToHost) # for debugging
	      clientsock.sendto("Receive your shared files",addr)
	    elif msg[0:4] == "List":
	      clientsock.sendto("Files are "+ str(files),addr)
	    elif msg[0:6] == "Search":
	      name = msg[7:]
	      print(name)
	      if name in files:
		clientsock.sendto("File Exists",addr)
	      else:
		clientsock.sendto("No Such File",addr)
	    elif msg[0:8] == "download":
	      name = msg[9:] #extract the file name
	      owner = fileToHost[name] #file owner address
	      msgToOwner = [name,addr] # a list for file name and receiver
	      clientsock.sendto(str(msgToOwner),owner)
	      
	      
clientsock.close()