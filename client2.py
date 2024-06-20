import socket

HOST = 'localhost'
PORT = 9050


def main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        sock.connect((HOST, PORT))
        print(f'Connected to {HOST}:{PORT}')

        # Send a message to the server
        message = "Hello, Server! This is not a secure message."
        sock.sendall(message.encode('utf-8'))
        print(f'Sent: {message}')

        # Receive a response from the server
        response = sock.recv(1024).decode('utf-8')
        print(f'Received: {response}')

    except Exception as e:
        print(f'Exception occurred: {e}')
    finally:
        sock.close()
        print('Connection closed')


if __name__ == "__main__":
    main()
