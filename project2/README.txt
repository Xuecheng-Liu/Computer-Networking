There are two python files contained for this assignment: ftps.py and ftpc

To run the program, download the zip in stdliux and unzip it. Open one terminal and type "python ftps.py" to run the server
and "python ftpc.py" to run the client. Please make sure you run the program under the correct directory of the file.

There are several command you can type in the client terminal
  1. Share filenames (eg: Share 1.txt). You can also share multiple files(eg:Share 1.txt 2.png).
     I assume different client will share different files for each file name. After shareing, the server will
     tell you received your shared files. Also, I assume the file you shared is in the same folder as the ftpc.py, otherwise,
     the program will crash under the downloading process.
  2. List. This command will tell you all the available files
  3. Search filename (eg: Seach 1.txt). I only support you to search one file at a time and the server will tell you
     whether the file exists or not.
  4. download filename (eg:download 1.txt) This command will enable you to download the file that is shared by another
     client. Please make you download the shared files and the client who share the file should still running. You should
     check whether the file exists or not by using Search command. If you try to download a file that has not been shared
     or the file has already been shared but does not exist, the program will crash.
     The downloaded files will be in the same folder as the client who makes the request to download.
     The downloaded file will be called new_filename. For example, if you are downloading 1.txt, you will get new_1.txt
     
     
  Please make sure you follow the suggestions above to test the program since I make a lot of assumptions to simplify
  the project.
  
