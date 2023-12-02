# 🕌 Dubai Athan Time Notification System 🕒

## Description
This system comprises two main components: a server and a client. The server scrapes Athan (Islamic prayer call) times for Dubai and sends email notifications at each Athan time. The client can connect to the server to request specific Athan times.

## Features
- 🌐 **Server**:
  - Scrapes Athan times for Dubai from the Khaleej Times website.
  - Sends email notifications at each Athan time.
  - Allows clients to connect and request Athan times.

- 💻 **Client**:
  - Connects to the server to request Athan times.
  - Provides an interactive menu for users to choose specific Athan times.

## Prerequisites
- Python 3
- Libraries: `requests`, `bs4` (BeautifulSoup), `smtplib`, `datetime`, `socket`, `threading`
- Internet connection
- SMTP email server access (Gmail used in the example)

## Setup

### Server
1. **Install Required Libraries:**
   ```
   pip install requests beautifulsoup4
   ```
2. **Email Configuration:**
   - Replace `your_email@gmail.com`, `your_password`, and `recipient_email@gmail.com` in the server script with actual email details.

### Client
1. **No additional setup is required for the client script.**

## Usage

### Server
1. **Start the Server Script:**
   ```
   python athan_server.py
   ```
   - The server will scrape the Athan times and listen for client connections.

### Client
1. **Run the Client Script:**
   ```
   python athan_client.py
   ```
   - Enter the username and password when prompted.
   - Interact with the server using the provided menu options.

## Important Notes
- 🛠️ **Web Scraping Dependency:** The server's functionality depends on the Khaleej Times website's layout. Changes to the site may require updates to the scraping logic.
- 🔐 **Email Security:** Ensure your email provider settings allow SMTP access.
- 🔄 **Continuous Operation:** The server script needs to run continuously for uninterrupted service.

## Disclaimer
- 🚫 This system is for educational purposes. Be aware of the legal and ethical implications of web scraping and automated email systems.
