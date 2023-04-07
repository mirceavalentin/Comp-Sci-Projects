import threading
import socket

def sending(sock):
    while True:
        command = ("Enter your command:")
        sock.sendall(command.encode("utf-8"))
        threading.Thread(target=sending, args=(sock, )).start()

def receiving(sock):
    while True:
        received_message = sock.recv(4096).decode("utf-8")
        print(received_message)
        threading.Thread(target=receiving, args=(sock, )).start()

def main():

    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_port = ("143.47.184.219", 5378)
        sock.connect(host_port)
        print("You've connected to the server.\n")

        print("Hello! This is a simple chatroom. The avalabile commands are:\nLIST = This is a list containing all currently logged-in users.\nSEND <user> <msg> = This sends a message to a specific user.\n")
        username = ("Please enter your username: ")
        sock.sendall(f"HELLO-FROM {username}\n".encode("utf-8"))
        message = sock.recv(4096).decode("utf-8")
        print(message)

        sending(sock)
        receiving(sock)

        if __name__ == '__main__':
            main()
