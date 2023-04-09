import threading
import socket

def receive_from_server(sock):
    while True:
        message = sock.recv(4096).decode("utf-8")
        if len(message) == 0:
            print("Connection closed by server.")
            exit(0)
        print(message)

def send_message_to_server(sock):
    while True:
        command = input("Avalabile commands:\nLIST\nSEND <user> <message>\nPlease input your command: ")
        sock.sendall(f"{command}\n".encode("utf-8"))

def communicate_to_server(sock):
    while True:
        user_name = input("Please enter your name: ")
        if user_name != '':
            sock.sendall(f"HELLO-FROM {user_name}\n".encode("utf-8"))
            break
        else:
            print("Username cannot be empty!")
    receive_from_server_thread = threading.Thread(target=receive_from_server, args=(sock,))
    receive_from_server_thread.start()
    send_message_to_server_thread = threading.Thread(target=send_message_to_server, args=(sock,))
    send_message_to_server_thread.start()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_port = ("143.47.184.219", 5378)
        sock.connect(host_port)
        print(f"Succesfully connected to server.")
    except:
        print(f"Unable to connect to server.")

    communicate_to_server(sock)

if __name__ == '__main__':
    main()
