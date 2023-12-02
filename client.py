import socket

def main():
    try:
        # Create a socket object for TCP connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()  # Get the hostname of the client
        port = 9999  # Communication port between client and server
        s.connect((host, port))  # Connect to the server
    except socket.error as e:
        print(f"Connection Error: {e}")
        exit()

    # Authentication
    username = input("Enter username: ")
    s.send(username.encode())
    password = input("Enter password: ")
    s.send(password.encode())

    # Interaction with the server
    while True:
        data = s.recv(1024).decode()  # Receive data from server
        print(data)  # Print the received data

        if "Choice:" in data:
            choice = input()  # User input for the choice
            s.send(choice.encode())

        elif "Exiting" in data or "invalid Username or Password" in data:
            break  # Exit the loop if 'Exiting' or 'invalid Username or Password' is received

    s.close()  # Close the socket

if __name__ == "__main__":
    main()
