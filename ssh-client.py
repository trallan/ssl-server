import paramiko
import sys
import time

HOST = 'localhost'
PORT = 9050
USERNAME = 'user'
PASSWORD = 'password'


def main():
    # Establish SSH connection
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)
        print(f'Connected to {HOST}:{PORT}')

        # Start interactive session
        channel = client.invoke_shell()
        print("Welcome to the SSH client! Type 'exit' to quit.")

        # Command loop
        while True:
            # Wait for user input
            command = input('$ ').strip()

            # Check for exit command
            if command.lower() == 'exit':
                break

            # Send the command to the server
            channel.send(command + '\n')

            # Wait a short delay to allow server to process command
            time.sleep(0.1)
            # Receive and print server response
            while channel.recv_ready():
                output = channel.recv(1024).decode('utf-8')
                sys.stdout.write(output)

    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as ssh_err:
        print(f"SSH error: {ssh_err}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close SSH connection
        client.close()
        print("SSH connection closed.")


if __name__ == "__main__":
    main()
