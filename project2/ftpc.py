import select, socket, sys,time

HOST = 'localhost'
PORT = 5015
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
inputs = [s,sys.stdin]
name = ""
while inputs:
    readable, writable, exceptional = select.select(inputs, inputs, inputs)
    for socket in readable:
        if socket is s:
            data = socket.recv(10240000) # assume big enough for the size of png
            msg = data # convert to string
            if msg[len(msg)-2:] == ")]": # task to send file to another client
	      l = eval(msg) # convert msg to list
	      # eg: l = ['1.txt', ('localhost', 1234)]
	      fileName = l[0]
	      receiver = l[1]
	      s.sendto("File Name: "+l[0],receiver)
	      # open the file,read it, and send to it another client
	      with open(fileName,'rb') as f:
		content = f.read(10240000)
		s.sendto(content,receiver)
		while content !="":
		  content = f.read(10240000)
		  s.sendto(content,receiver)      
	    elif msg == "Receive your shared files" or msg == "File Exists" or msg == "No Such File" or "Files are" in msg:
	      # situations where received data are not download related
	      print(msg)
	    elif msg[0:11] == "File Name: ":
	      name = msg[11:]
	      print("received file name")
	    else: # received data is file content
	      print("downloading...")
	      f = open("new_"+ name,"wb") #open the file
	      f.write(msg)
        elif socket is sys.stdin:
            msgToSend = raw_input()
            s.sendto(msgToSend,(HOST,PORT))
s.close()