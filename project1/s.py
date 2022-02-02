import select, socket, sys, Queue    
user_name = [] # keep track of all the registered user_name
user_collection = {} # dictionary to keep track of username and password

## load all users to user_name and user_collection
def loadAllUsers(user_name):
  file = open("user.txt","r")
  for line in file:
    oneUser = line.split(" ")
    username = oneUser[0]
    ## update user_collection with username and password and user_name
    if username not in user_name:
      user_name.append(username)
      user_collection[username] = oneUser[1].strip()
loadAllUsers(user_name)

online = {} # dictionary that keeps track of logined sockets as key and username as value
online_list = [] # list to trace all online usename

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('localhost', 5113))
server.listen(5)
inputs = [server, sys.stdin]
newData = 0
print("Server is up......")
while inputs:
    readable, writable, exceptional = select.select(
        inputs, inputs, inputs)
    for s in readable:
        # this stanza handles connection requests. 
        if s is server:
            print ("received a connect requst from a client ")
            print
            connection, client_address = s.accept()
            connection.send("Connected successfully with the server")
            print "connection is {}".format (connection)
            connection.setblocking(0)
            inputs.append(connection)
        
	# handles input from keyboard in server terminal    
        elif s is sys.stdin:
            newData = 1;
            command_string = raw_input()
            print "received:::: " + command_string
        else:
            # this stanza handles already connected sockets (data from clients)
            data = s.recv(1024)
	    # process the data if it is not empty
            if data:
	      # handles message like 'Register<A><123>'
	      if "Register" in data[0:10]:
		username = data[data.find('<')+1:data.find('>')]
		password = data[data.find('>')+2:len(data)-1]
		file = open("user.txt","a")
		# append username to user_name and write username and password to the file
		# if the username has not been registered yet
		if username not in user_name:
		  user_name.append(username)
		  user_collection[username] = password.strip()
		  file.write(username + " "+ password+"\n")
		else:
		  s.send(username + " has already exist!!")
		# for debugging purpose, list all the registered users
		print(user_name)
	      # handles command like 'Login<A><123>'
	      elif "Login" in data[0:7]:
		username = data[data.find('<')+1:data.find('>')]
		# prevent one socket from log in multiple account
		if s not in online.keys() and username not in online_list:
		  
		  password = data[data.find('>')+2:len(data)-1]
		  # check whether username is registered or not
		  if username in user_name:
		    # check the correctness of password
		    if user_collection[username] == password:
		      online_list.append(username)
		      online[s] = username
		      # for debugging purpose
		      print(len(online_list))
		      print(len(user_collection))
		      print(online.keys())
		      print(online_list)
		    else:
		      s.send("password is not correct!")
		  else:
		    s.send(username + "has already been registered.")
		else:
		  s.send(online[s] + " has already online. Please log out first!")
	      
	      # handles commend like 'List'  
	      elif "List" in data[0:6]:
		# prevent you from checking online users without logging in
		if s in online.keys():
		  allusers = "Online users: "
		  for i in online_list:
		    allusers = allusers + i + " "
		  s.send(allusers)
		else:
		  s.send("Please login first")
	      # handles command like 'Message<B><hello>'  
	      elif "Message" in data[0:9]:
		# make sure user has already logged in to send message
		if s in online.keys():
		  target = data[data.find('<')+1:data.find('>')]
		  msg = data[data.find('>')+2:len(data)-1]
		  # check whether target is online or not
		  if target in online_list:
		    for socket in online.keys():
		      if online[socket] == target:
			socket.send(online[s] + ": " + msg)
		  else:
		    s.send(target + " is not online")
		else:
		  s.send("Please login first to send message")

	      # handles command like 'Logout<A>'
	      # Notice: this implementation only allows you to log yourself out!
	      elif "Logout" in data[0:7]:
		username = data[data.find('<')+1:len(data)-1]
		if username in online_list:
		  for socket in online.keys():
		    if online[socket] == username:
		      if socket == s:
			del online[socket]
			online_list.remove(username)
			s.send(username + " logout successfully")
		      else:
			s.send("You cannot logout other client!")
		else:
		  s.send("Please login first!")
	      else:
		s.send("Please follow the specified input format to test the program")
		
    # handles exceptions in sockets
    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()


    

