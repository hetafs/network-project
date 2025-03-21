# Network Project

## Overview

This project is a **client-server network application** that allows users to upload, download, remove, and rename files. It also includes **user authentication** and **password reset functionality**.

## Features

- **User authentication** (login and new user registration)
- **File upload, download, removal, and renaming**
- **Password reset** for existing users
- **Multi-client support** using threading
- Uses **TCP connection** for reliable data transmission

## 📂 Folder Structure
Network-Project
   client/
     client.py
     Top.txt # Example file 
     study.txt # Example file 
     net.txt # Example file 
  server/ 
     server.py 
     client_data.json # Stores user data
  README.md # This file
  readme_ResultOfRun.pdf


## Installation & Usage

### Server Setup

1. Navigate to the server folder:
   cd server
2. Run the server:
   python server.py

### Client Setup
1. Navigate to the client folder:
   cd client
2. Run the client:
   python client.py
3. Follow the prompts to authenticate and manage files.

### Technologies Used
1. TCP Connection (using socket.SOCK_STREAM) for reliable communication
2. Python
3. Sockets
4. JSON for data storage
5. Multi-threading for handling multiple clients

### How It Works (TCP Connection Details)
	1. The server listens for incoming client connections on 127.0.0.1:11502 using TCP.
	2. The client establishes a connection to the server using TCP.
	3. Reliable communication is ensured by:
		Handshaking between the client and server
		Sending and receiving data streams without packet loss
		Ensuring order of data packets
	4. Each client communicates with the server in a dedicated thread, allowing multiple clients to connect simultaneously.

### Notes
	1. The server runs on 127.0.0.1 at port 11502 by default.
	2. Ensure that the client and server are running on the same network.
	3. The client_data.json file stores registered user credentials and file lists.
	4. You can replace the files (e.g., Top.txt, example.txt, net.txt) in the client folder to upload, download, etc.
 
### Future Improvements
	1. Implement encryption for secure authentication.
	2. Improve error handling and logging.
	3. Enhance file transfer efficiency for large files.
	4. Add user interface.


Author: Hetaf Alsuwailem
