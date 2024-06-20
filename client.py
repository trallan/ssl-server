import socket
import ssl

HOST = 'localhost'
PORT = 9050

# Create an SSL context
context = ssl.create_default_context()

# The client doesn't need to load a certificate; it only verifies the server's certificate
context.load_verify_locations(
    'certfile.pem')  # Server's certificate for verification


def main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap the socket with SSL
    ssl_sock = context.wrap_socket(sock, server_hostname=HOST)

    try:
        # Connect to the server
        ssl_sock.connect((HOST, PORT))
        print(f'Connected to {HOST}:{PORT}')
        while True:
            # Get input from the user
            message = input("Enter command (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break

            # Send the message to the server
            ssl_sock.sendall(message.encode('utf-8'))
            print(f'Sent: {message}')

            # Receive a response from the server
            response = ssl_sock.recv(1024).decode('utf-8')
            print(f'{response}')
    except KeyboardInterrupt:
        print('Client shutting down...')
    except Exception as e:
        print(f'Exception occurred: {e}')
    finally:
        ssl_sock.close()
        print('Connection closed')


if __name__ == "__main__":
    main()
