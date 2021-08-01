Run: 
Python streamer.py (port: I used 12000)
Python trial.py host (connection port) (client server port) message

Example:

Streamer: python streamer.py 12000
Viewer 1: python trial.py 10.0.0.10 12000 12001 message
Viewer 2: python trial.py localhost 12001 12002 message

Streamer will await a connection and begin transmitting data every second. Once a connection request
is accepted the address of the client will be appended to a connections list and a tracker list 
containing the address and the number of viewers connected to that viewer.

Viewer 1 will create a Client thread and connect to the Streamer, recieve and display transmittion, 
and add it to a buffer of size 15. Viewer 1 will also create a Server thread which awaits a connection
request. Upon accepting the request a thread is created for the new Viewer 2. The thread sleeps for 
ten seconds in case Viewer 1's buffer does not contain enough data.

Viewer 2 will connect to the Streamer 

Things left to do:
Remove from tracker upon disconnect.
Handle when Viewer X is transmitting data to Viewer Y and X disconnects.
Each viewer can only have one other viewer connected for propper transmition- skips bits. (Feature or bug?)
Add status messages.