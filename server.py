import socket
import threading
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Authentication credentials
USER = "admin"
PASSWD = "password"
URL = "https://www.khaleejtimes.com/prayer-time-uae/dubai"


# Scrape Athan times
def scrape_athan_times():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    prayer_times = {}
    headers = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    # The CSS selector needs to be updated according to the website's structure
    time_elements = soup.select('.prayer-timing-wrap tbody tr:first-child td:not(:first-child)')
    for header, time_element in zip(headers, time_elements):
        prayer_times[header] = time_element.text.strip()
    return prayer_times


# This will hold the scraped Athan times
athan_times = {}


# Update Athan times once a day
def update_athan_times():
    global athan_times
    athan_times = scrape_athan_times()
    # Schedule the next update for the next day
    threading.Timer(86400, update_athan_times).start()


# Start the update immediately when the server starts
update_athan_times()


def client_handler(client_socket):
    try:
        # Receive the username and password from the client
        username = client_socket.recv(1024).decode('utf-8')
        password = client_socket.recv(1024).decode('utf-8')

        # Check the credentials
        if username == USER and password == PASSWD:
            client_socket.send("Login successful".encode('utf-8'))
            # Logged-in user interaction loop
            while True:
                # Send choices to the client
                client_socket.send(
                    "\n[1] Send Fajr Time\n[2] Send Dhuhr Time\n[3] Send Asr Time\n[4] Send Maghrib Time\n[5] Send Isha Time\nType 'done' to exit\nChoice: ".encode(
                        'utf-8'))
                choice = client_socket.recv(1024).decode('utf-8').strip()

                # Process the client's choice
                if choice == "done":
                    client_socket.send("Exiting".encode('utf-8'))
                    break
                elif choice in ["1", "2", "3", "4", "5"]:
                    # Send the corresponding Athan time
                    times = list(athan_times.values())
                    client_socket.send(
                        f"{list(athan_times.keys())[int(choice) - 1]} time is at: {times[int(choice) - 1]}".encode(
                            'utf-8'))
                else:
                    client_socket.send("Invalid choice. Please try again.".encode('utf-8'))
        else:
            client_socket.send("Login failed: invalid username or password".encode('utf-8'))
    except Exception as e:
        print(f"An exception occurred: {e}")
    finally:
        client_socket.close()


def start_server(host='localhost', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}. Waiting for connections...")

    try:
        while True:
            client_sock, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_thread = threading.Thread(target=client_handler, args=(client_sock,))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer is shutting down.")
    finally:
        server_socket.close()
        print("Server closed.")


if __name__ == "__main__":
    start_server()
