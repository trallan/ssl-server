import socket
import ssl
import threading
import logging

# Create logging file
logging.basicConfig(filename='server.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')

# SSL context
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='certfile.pem', keyfile='keyfile.pem')

HOST = 'localhost'
PORT = 9050


def is_valid_message(message):
  return message.isalnum() or ' ' in message or message.startswith('server')


def handle_client(conn, addr):
  logging.info(f'Conntected by {addr}')
  ssl_conn = context.wrap_socket(conn, server_side=True)
  try:
    while True:
      data = ssl_conn.recv(1024).decode('utf-8')
      if not data:
        break
      if is_valid_message(data):
        logging.info(f'Received from {addr}: {repr(data)}')
        if data == 'server -info':
          response = "Server information: Example server v1.0"
        else:
          response = "Wrong command"
        ssl_conn.sendall(response.encode('utf-8'))
  except KeyboardInterrupt:
    print('Server shutting down...')
  except Exception as e:
    logging.error(f'Exception occurred while handling connection: {e}')
  finally:
    ssl_conn.close()
    logging.info(f'Connection closed {addr}')


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(5)
print('Server is listening...')

try:
  while True:
    conn, addr = s.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
except KeyboardInterrupt:
  print('Server shutting down...')
except Exception as e:
  print('Exception occurred:', e)
finally:
  s.close()
  print('Server closed')
