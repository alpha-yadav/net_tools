import socket,sys

def listen_for_broadcast(port):
      # Port for receiving broadcast messages

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to listen for messages
    client_socket.bind(("", port))
    print(f"Listening for broadcasts on port {port}...")

    while True:
        # Receive broadcast messages
        data, address = client_socket.recvfrom(1024)  # Set a timeout for receiving messages
        print(f"{address} -> {data.decode()}")

if __name__ == "__main__":
    port = 22340  # Default port
    if len(sys.argv) > 1:
        port= int(sys.argv[1])
    listen_for_broadcast(port=port)
