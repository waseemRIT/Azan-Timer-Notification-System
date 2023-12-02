import socket

def main():
    host = 'localhost'  # Server hostname or IP address; change if different
    port = 9999         # The same port as used by the server

    client_socket = socket.socket()  # Instantiate socket
    client_socket.connect((host, port))  # Connect to the server

    # Authentication
    username = input("Enter username: ")
    password = input("Enter password: ")
    client_socket.send(username.encode('utf-8'))
    client_socket.send(password.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(response)

    if "successful" in response:
        while True:
            # Receive and print options from the server
            options = client_socket.recv(1024).decode('utf-8')
            print(options, end='')

            # User inputs their choice
            choice = input()
            client_socket.send(choice.encode('utf-8'))

            if choice.lower() == 'done':
                break

            # Receive and print the response from the server
            data = client_socket.recv(1024).decode('utf-8')
            print(data)

        print("Disconnected from the server.")
    else:
        print("Failed to log in. Exiting...")

    client_socket.close()

if __name__ == "__main__":
    main()
