import socket
import threading
import requests

# Constants for the server
HOST = 'localhost'
PORT = 9999
USER = "admin"
PASSWD = "password"

# Function to get Athan times using Aladhan API
def get_athan_times():
    params = {
        "city": "Dubai",
        "country": "United Arab Emirates",
        "method": "2"  # Fiqh Hanafi
    }
    response = requests.get("http://api.aladhan.com/v1/timingsByCity", params=params)
    if response.status_code == 200:
        timings = response.json()['data']['timings']
        return timings
    else:
        print("Error fetching prayer times:", response.status_code)
        return {}

# This dictionary will store the Athan times
athan_times = get_athan_times()

# Client handler function
def client_handler(client_socket):
    try:
        # Authentication
        username = client_socket.recv(1024).decode('utf-8').strip()
        password = client_socket.recv(1024).decode('utf-8').strip()

        if username == USER and password == PASSWD:
            client_socket.send("Login successful".encode('utf-8'))
            while True:
                # Send choices to the client
                client_socket.sendall("Choose Athan time to send [Fajr, Dhuhr, Asr, Maghrib, Isha] or 'done' to exit: ".encode('utf-8'))
                choice = client_socket.recv(1024).decode('utf-8').strip()

                if choice.lower() == 'done':
                    client_socket.sendall("Exiting".encode('utf-8'))
                    break
                elif choice.capitalize() in athan_times:
                    response = f"{choice.capitalize()} time is at: {athan_times[choice.capitalize()]}"
                    client_socket.sendall(response.encode('utf-8'))
                else:
                    client_socket.sendall("Invalid choice. Please try again.".encode('utf-8'))
        else:
            client_socket.sendall("Login failed: invalid username or password".encode('utf-8'))

    except Exception as e:
        print(f"An exception occurred with client {client_socket.getpeername()}: {e}")
    finally:
        client_socket.close()

# Function to start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server started on {HOST}:{PORT}. Waiting for connections...")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            threading.Thread(target=client_handler, args=(client_socket,), daemon=True).start()
        except Exception as e:
            print(f"An exception occurred: {e}")

    server_socket.close()

# Run the server
if __name__ == "__main__":
    start_server()
