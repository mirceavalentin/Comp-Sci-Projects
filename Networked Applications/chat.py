# Necessary libraries
import threading
import socket

def receive_from_server(sock):
    while True:
        message = sock.recv(4096).decode("utf-8")
        try:
            print(message)
        except OSError as msg:
            print(msg)

def send_message_to_server(sock):
    while True:
        command = input()
        try:
            sock.sendall(f"{command}\n".encode("utf-8"))
            print("Enter your command: ")
        except OSError as msg:
            print(msg)

def communicate_to_server(sock):
    user_name = input("Please enter your name: ")
    if user_name != '':
        sock.sendall(f"HELLO-FROM {user_name}\n".encode("utf-8"))
    else:
        print("Username cannot be empty!")
        exit(0)
    
    threading.Thread(target=receive_from_server, args=(sock, )).start()
    send_message_to_server(sock)

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