# Necessary libraries
import threading
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_port = ("143.47.184.219", 5378)
sock.connect(host_port)
print("Connected to the server.")

# Take the username of the user and then form the first hello message
username = input("Enter your username: ")
first_hello = f"HELLO-FROM {username}\n"

# Send the first hello message
sock.send(first_hello.encode("utf-8"))

# Receive the first message and print it
message = sock.recv(4096).decode("utf-8")
print(message)            

def sending():
    while True:
         message = input("Type your command: ")
         string_bytes = "f{message}".encode("utf-8")
         bytes_len = len(string_bytes)
         while num_bytes_to_send > 0:
            num_bytes_to_send -= sock.send(string_bytes[bytes_len-num_bytes_to_send:])



# To do: Implement threading and sending. Maybe use a while loop in this function.


# # Receiving function
# def receive():
#     while True:
#         message = sock.recv(4096).decode("utf-8")
#         print(message)

# # Sending function
# def send():
#     while True:
#         message = input("Please send ur message: ")
#         sock.send(message.encode("utf-8"))

# # Threading for each of them
# receive_thread = threading.Thread(target=receive)
# receive_thread.start()

# # Threading for each of them
# send_thread = threading.Thread(target=send)
# receive_thread.start()