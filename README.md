##Network Project##
###Overview###
This project is a client-server network application that allows users to upload, download, remove, and rename files. It also includes user authentication and password reset functionality.

Features
User authentication (login and new user registration)
File upload, download, removal, and renaming
Password reset for existing users
Multi-client support using threading
Uses TCP connection for reliable data transmission
Folder Structure
graphql
نسخ
تحرير
Network-Project
├── 📂 client
│   ├── client.py
│   ├── Top.txt  # Example
│   ├── study.txt  # Example
│   ├── net.txt  # Example
├── 📂 server
│   ├── server.py
│   ├── client_data.json  # Stores user data
└── README.md  # This file
└── readme_ResultOfRun.pdf  # PDF with results of the program run
Installation & Usage
Server Setup
Navigate to the server folder:

bash
نسخ
تحرير
cd server
Run the server:

bash
نسخ
تحرير
python server.py
Client Setup
Navigate to the client folder:

bash
نسخ
تحرير
cd client
Run the client:

bash
نسخ
تحرير
python client.py
Follow the prompts to authenticate and manage files.

Technologies Used
TCP Connection (using socket.SOCK_STREAM) for reliable communication
Python
Sockets
JSON for data storage
Multi-threading for handling multiple clients
How It Works (TCP Connection Details)
The server listens for incoming client connections on 127.0.0.1:11502 using TCP.
The client establishes a connection to the server using TCP.
Reliable communication is ensured by:
Handshaking between the client and server
Sending and receiving data streams without packet loss
Ensuring order of data packets
Each client communicates with the server in a dedicated thread, allowing multiple clients to connect simultaneously.
Notes
The server runs on 127.0.0.1 at port 11502 by default.
Ensure that the client and server are running on the same network.
The client_data.json file stores registered user credentials and file lists.
You can replace the files (e.g., Top.txt, example.txt, net.txt) in the client folder to upload, download, etc.
Future Improvements
Implement encryption for secure authentication.
Improve error handling and logging.
Enhance file transfer efficiency for large files.
Add user interface.
Author: Hetaf Alsuwailem
