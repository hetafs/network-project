import socket
import json
import os
import threading


def conn_client(client_socket, address, client_data): #connect with client
    print(f"Connection from {address} has been established.")

    while True:
        #Receive username and password from the client
        username = client_socket.recv(1024).decode()
        password = client_socket.recv(1024).decode()

        if client_data.get(username, {}).get('password') == password: # case 1: log in
            client_socket.send('LOG_IN'.encode())  # Send to client successful login
            client_files = client_data[username]['files']
            try:
                client_socket.send(json.dumps(client_files).encode())
            except ConnectionAbortedError:
                break

        elif username not in client_data:                            # case 2: New user registration
            client_data[username] = {'password': password, 'files': []}
            with open('client_data.json', 'w') as file:
                json.dump(client_data, file)

            # Create a folder for the new user
            user_folder = os.path.join(username)
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)

            client_socket.send('NEW_USER'.encode())  # Send to client new user
            client_files = client_data[username]['files']
            try:
                client_socket.send(json.dumps(client_files).encode())
            except ConnectionAbortedError:
                break
            print(f"New user '{username}' has been registered.")

        else:                                                   # case 3: Incorrect password
            client_socket.send('INVALID_PASSWORD'.encode())  # Send to client invalid password
            reset_choice = client_socket.recv(1024).decode()
            if reset_choice.lower() == 'yes':
                new_password = client_socket.recv(1024).decode()
                reset_password(client_data, username, new_password)
                client_socket.send('PASSWORD_RESET'.encode())
                print(f"Password for {username} reset successfully.")
                continue
            else:
                print(f"Login attempt failed for {username}.")

        #after user logged in, loop for file operations
        while True:
            command = client_socket.recv(1024).decode()

            if command == 'UPLOAD':
                upload(client_socket, username, client_data, address)
            elif command == 'DOWNLOAD':
                download(client_socket, username, address)
            elif command == 'LIST':
                client_socket.send(json.dumps(client_files).encode())
            elif command == 'REMOVE':
                remove(client_socket, username, client_data, address)
            elif command == 'RENAME':
                rename(client_socket, username, client_data, address)
            elif command == 'DISCONNECT':
                print(f"Client at {address} has disconnected.")
                break

def upload(client_socket, username, client_data, address):
    #Receive the filename and file contents from the client
    filename = client_socket.recv(1024).decode()
    file_contents = client_socket.recv(1024)

    with open(os.path.join(username, filename), 'wb') as file:
        file.write(file_contents)

    client_data[username]['files'].append(filename) #Update client's file list
    with open('client_data.json', 'w') as file:
        json.dump(client_data, file)
    client_socket.send("File uploaded successfully.".encode())
    print("here is send")
    print(f" file '{filename}' has been recieved from client {address}.")

def download(client_socket, username, address):
    filename = client_socket.recv(1024).decode()  #Receive the filename from the client
    file_path = os.path.join(username, filename)

    if os.path.exists(file_path):      #If the file exists, send its contents to the client
        with open(file_path, 'rb') as file:
            file_contents = file.read()
        client_socket.send(file_contents)
        print(f" file '{filename}' has been downloaded by client {address}.")

    else:
        client_socket.send("ERROR: File not found.".encode())

def remove(client_socket, username, client_data, address):
    filename = client_socket.recv(1024).decode() #Receive the filename from the client
    file_path = os.path.join(username, filename)

    if os.path.exists(file_path):  #If the file exists, remove it and update the client's file list
        os.remove(file_path)
        client_data[username]['files'].remove(filename)
        with open('client_data.json', 'w') as file:
            json.dump(client_data, file)
        client_socket.send("File removed successfully.".encode())
        print(f" file '{filename}' has been removed by client {address}.")
    else: #If the file doesn't exist
        client_socket.send("ERROR: File not found.".encode())
        print(f" file '{filename}' not fount")


def rename(client_socket, username, client_data, address):
    filenames = client_socket.recv(1024).decode().split(',')  # Split into old and new filenames
    old_filename = filenames[0].strip()
    new_filename = filenames[1].strip()

    old_file_path = os.path.join(username, old_filename)
    new_file_path = os.path.join(username, new_filename)

    if os.path.exists(old_file_path): #If the old file exists, rename it and update the client's file list
        os.rename(old_file_path, new_file_path)
        client_data[username]['files'].remove(old_filename)
        client_data[username]['files'].append(new_filename)
        with open('client_data.json', 'w') as file:
            json.dump(client_data, file)
        client_socket.send("File renamed successfully.".encode())
        print(f" file renamed by client {address}.")

    else:
        client_socket.send("ERROR: File not found.".encode())


def reset_password(client_data, username, new_password):
    if username in client_data:
        client_data[username]['password'] = new_password
        with open('client_data.json', 'w') as file:
            json.dump(client_data, file)
        return True
    return False


def server_main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = "127.0.0.1"
    PORT = 11502
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    print(f"Server is listening on {IP}:{PORT}")

    #get client data
    try:
        with open('client_data.json', 'r') as file:
            client_data = json.load(file)
    except FileNotFoundError:
        client_data = {}

    #listens for incoming connections
    connected_clients = 0 #client in conn counter
    while True:
        client_socket, address = server_socket.accept()
        connected_clients += 1
        print(f"Number of clients : {connected_clients}")
        print("Waiting for incoming connections ")
        client_thread = threading.Thread(target=conn_client, args=(client_socket, address, client_data))
        client_thread.start()

if __name__ == "__main__":
    server_main()
