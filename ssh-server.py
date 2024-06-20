import paramiko
import threading
import socket
import logging

# Create logging file
logging.basicConfig(filename='ssh-server.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')

HOST = 'localhost'
PORT = 9050

# Load the private key with a passphrase
HOST_KEY = paramiko.RSAKey(filename='server_key', password='test')


class SSHServer(paramiko.ServerInterface):

    def __init__(self):
        self.event = threading.Event()
        self.shell_requested = False

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == 'user' and password == 'password':
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password'

    def check_channel_shell_request(self, channel):
        self.shell_requested = True
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height,
                                  pixelwidth, pixelheight, modes):
        return True


def handle_client(client, addr):
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)
    server = SSHServer()

    try:
        transport.start_server(server=server)

        chan = transport.accept(20)
        if chan is None:
            print('No channel.')
            return

        server.event.wait(10)
        if not server.shell_requested:
            print('Shell not requested.')
            return

        # Now loop to handle commands
        while chan.active:
            try:
                # Receive data from the client
                data = chan.recv(1024)
                if not data:
                    break

                # Decode the received data
                command = data.decode('utf-8').strip()
                if command == 'exit':
                    chan.send('Bye!\n')
                    break
                elif command == 'server-info':
                    response = "Server information: Example server v1.0\n"
                    logging.info(f'Client request server-info')
                else:
                    response = "Wrong command\n"

                # Send response to the client
                chan.send(response.encode('utf-8'))

            except Exception as e:
                print(f'Error receiving/sending command: {e}')
                break

    except Exception as e:
        print(f'Exception: {e}')
    finally:
        transport.close()
        logging.info(f'Connection closed {addr}')
        print(f'Connection closed from {addr}')


def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f'Server listening on {HOST}:{PORT}...')

    while True:
        client, addr = sock.accept()
        print(f'Accepted connection from {addr}')
        logging.info(f'Accepted connection from {addr}')
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()


if __name__ == "__main__":
    start_server()
