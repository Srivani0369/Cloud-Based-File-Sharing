import socket
import os

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 5002       # Any free port

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"[SERVER] Listening on {HOST}:{PORT}...")

# Ensure directory for uploaded files
if not os.path.exists("uploads"):
    os.makedirs("uploads")

while True:
    conn, addr = server_socket.accept()
    print(f"[+] Connection from {addr}")

    option = conn.recv(1024).decode()
    
    # Upload file from client
    if option == '1':
        filename = conn.recv(1024).decode()
        filepath = os.path.join("uploads", filename)
        with open(filepath, 'wb') as f:
            data = conn.recv(1024)
            while data:
                f.write(data)
                data = conn.recv(1024)
        print(f"[SERVER] File '{filename}' received successfully.")
    
    # Send file to client (download)
    elif option == '2':
        filename = conn.recv(1024).decode()
        filepath = os.path.join("uploads", filename)
        if os.path.exists(filepath):
            conn.send(b"FOUND")
            with open(filepath, 'rb') as f:
                data = f.read(1024)
                while data:
                    conn.send(data)
                    data = f.read(1024)
            print(f"[SERVER] File '{filename}' sent successfully.")
        else:
            conn.send(b"NOTFOUND")
            print(f"[SERVER] File '{filename}' not found.")
    
    conn.close()
