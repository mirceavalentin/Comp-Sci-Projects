# Necessary libraries
import threading
import socket

def receive_from_server(sock):
    while 1:
        message = sock.recv(4096).decode("utf-8")
        if not message:
            print("Socket is closed.")
        else:
            print("Socket has data.")

def send_message_to_server(sock):
    while 1:
        message = input("Your message is: ")
        if message != '':
            sock.sendall(message.encode("utf-8"))
        else:
            print("Empty message")
            exit(0)

def communicate_to_server(sock):
    user_name = input("Please enter your name: ")
    if user_name != '':
        sock.sendall("HELLO-FROM {user_name}\n".encode("utf-8"))
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




























# string_bytes = "Sockets are great!".encode("utf-8")
# bytes_len = len(string_bytes)
# num_bytes_to_send = bytes_len
# while num_bytes_to_send > 0:
# # Sometimes, the operating system cannot send everything immediately.
# # For example, the sending buffer may be full.
# # send returns the number of bytes that were sent.
# num_bytes_to_send -= sock.send(string_bytes[bytes_len-num_bytes_to_send:])

# sock.sendall(string_bytes)      # Sendall calls send repeatedly until all bytes are sent.

# # Waiting until data comes in
# # Receive at most 4096 bytes.
# data = sock.recv(4096)
# if not data:
# print("Socket is closed.")
# else:
# print("Socket has data.")

# try:
# sock.send("how to handle errors?".encode("utf-8"))
# answer = sock.recv(4096)
# except OSError as msg:
# print(msg)




# print ("Hello world!")      # Test

