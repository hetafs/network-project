import socket
import json

def Authentication(client_socket):
    while True: #Prompt user for username and password
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        # Send username and password to server
        client_socket.send(username.encode())
        client_socket.send(password.encode())

        auth_response = client_socket.recv(1024).decode()  # recieve entry case
        if auth_response == 'LOG_IN':
            print(f"Welcome back, {username}!")
            return True
        elif auth_response == 'NEW_USER':
            print(f"You are a new user {username}. Welcome!")
            return True
        elif auth_response == 'INVALID_PASSWORD':
            reset_choice = input("Wrong password. Do you want to reset your password? (yes/no): ").lower()
            if reset_choice == 'yes':
                if reset_password(client_socket):
                    continue
            else:
                return False
        else:
            print("Error: Authentication failed. Please check your username and password.")
            return False


def main():  #Connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = "127.0.0.1"
    PORT = 11502
    client_socket.connect((IP, PORT))
    print("Connected Successfully")


    while True:
        if not Authentication(client_socket):
            return

        print("Display a list of your files") # after sign up list of their uploaded files
        files_list = json.loads(client_socket.recv(1024).decode())
        if files_list:
            print("Your files in the server are:")
            for file in files_list:
                print(file)
        else:
            print("You have not uploaded any file to the server")

        print("Select an option:")
        print("a. Upload a file")
        print("b. Remove a file")
        print("c. Download a file")
        print("d. Rename a file")
        option = input("Enter your option: ")

        if option == 'a':
            upload_file(client_socket)
            break
        elif option == 'b':
            remove_file(client_socket)
            break
        elif option == 'c':
            download_file(client_socket)
            break
        elif option == 'd':
            rename_file(client_socket)
            break
        else:
            break
    # Disconnect from the server
    client_socket.send('DISCONNECT'.encode())
    print("Ending connection with server")
    client_socket.close()

def upload_file(client_socket):
    filename = input("Enter the filename to send: ")

    #Send upload command and filename to server
    client_socket.send('UPLOAD'.encode())
    client_socket.send(filename.encode())

    #Read file contents and send to server
    with open(filename, 'rb') as file:
        file_contents = file.read()
        client_socket.send(file_contents)

    #Receive upload response from server
    print(client_socket.recv(1024).decode())
    print(f"File '{filename}' has been sent to the server.")
def remove_file(client_socket):
    filename = input("Enter the filename to remove: ")
    #Send remove command and filename to server
    client_socket.send('REMOVE'.encode())
    client_socket.send(filename.encode())

    #Receive remove response from server
    print(client_socket.recv(1024).decode())
    print(f"File '{filename}' has been removed from the server.")


def download_file(client_socket):
    filename = input("Enter the filename to download: ")
    #Send download command and filename to server
    client_socket.send('DOWNLOAD'.encode())
    client_socket.send(filename.encode())

    #Receive file contents from server
    file_contents = client_socket.recv(1024)

    #Write file contents to disk
    with open(filename, 'wb') as file:
        file.write(file_contents)
    print(f"File '{filename}' has been downloaded.")

def rename_file(client_socket):
    old_filename = input("Enter the old filename: ")
    new_filename = input("Enter the new filename: ")
    # Send to server
    client_socket.send('RENAME'.encode())
    client_socket.send(f"{old_filename},{new_filename}".encode())
    #Receive rename response from server
    print(client_socket.recv(1024).decode())
    print(f"File '{old_filename}' has renamed to '{new_filename}'.")

def reset_password(client_socket):
    client_socket.send('yes'.encode())   #Send the choice to reset password
    new_password = input("Enter your new password: ")
    client_socket.send(new_password.encode())
    reset_response = client_socket.recv(1024).decode()
    if reset_response == 'PASSWORD_RESET':
        print("Password reset successful.")
        return True
    else:
        print("Error: Password reset failed.")
        return False

if __name__ == "__main__":
    main()
