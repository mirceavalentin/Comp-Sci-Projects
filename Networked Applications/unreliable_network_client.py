
import socket, threading, sys, time


BUFFER_SIZE = 512
CONN_ADDR = ("143.47.184.219", 5382)

msg_event = threading.Event()

def timeout(n):
    global msg_acknowledged
    print(f"Starting timeout of {n} seconds")
    start, elapsed_time = time.time(), 0
    time.sleep(1)
    while elapsed_time <= n:
        if not msg_acknowledged:
            elapsed_time = time.time() - start
        else: 
            return elapsed_time
            
    return -1


# snipped from the lab manual
def send_full_message(sock, msg):

    # check if msg is a string
    if isinstance(msg, str):
        msg = msg.encode('utf-8')

    bytes_len = len(msg)
    num_bytes_to_send = bytes_len
    while num_bytes_to_send > 0:
        # Sometimes, the operating system cannot send everything immediately.
        # For example, the sending buffer may be full.
        # send returns the number of bytes that were sent.
        # sendto also specifies the destination address.
        num_bytes_to_send -= sock.sendto(msg[bytes_len - num_bytes_to_send:], CONN_ADDR)
    return True
    


def receive_full_msg(sock: socket.socket):
    recv_msg = b"" 
    recv_error = False

    if (sock is None):
        raise ValueError(f"Socket cannot be None")

    while not recv_error:
        try:
            recv_data = sock.recvfrom(BUFFER_SIZE)[0]         
            recv_msg = recv_msg + recv_data

            if not recv_data or b"\n" in recv_data:
                recv_error = True
                break

        except Exception as e:
            if msg_acknowledged:
                print(f"A client side error occurred! No data received {e}")            
            break

    return recv_msg



def checksum_addition_overflow(binary_chars_sum):
    checksum = bin(binary_chars_sum)

    if len(checksum) > 9:
        i = len(checksum) - 7
        binary_chars_sum = int(checksum[2:i], 2) + int(checksum[i:], 2)
        checksum = bin(binary_chars_sum)

    return binary_chars_sum, checksum



def checksum_generator(msg):
    binary_chars_sum = 0b00000000  

    # a is the index of each character being processed
    for a in range(len(msg)):
        binary_chars_sum += ord(msg[a])
        binary_chars_sum, checksum = checksum_addition_overflow(binary_chars_sum)

    checksum = format(int(checksum, 2), "#09b")

    complement_sum = "0b"
    for i in range(2, len(checksum)):
        complement_sum += "1" if checksum[i] == "0" else "0"

    return complement_sum 



def validate_recv_checksum(msg):
    req_header_pos = 0 
    while True:
        if msg[req_header_pos] == " ":
            break
        req_header_pos += 1
        if req_header_pos == len(msg) - 2:
            return False
    
    checksum_digit_pos = 0 
    while True:
        if msg[checksum_digit_pos:checksum_digit_pos+2] == "0b":
            break

        checksum_digit_pos += 1
        if checksum_digit_pos == len(msg) - 2:
            return False

    checksum = msg[checksum_digit_pos:].strip() 
    for i in range(2, 8):
        if checksum[i] not in ["0", "1"]:
            return False

    msg_body = msg[req_header_pos+1:checksum_digit_pos]
    
    try:
        checksum, msg_body = checksum.encode('utf-8'), msg_body.encode('utf-8')

        binary_chars_sum = int(checksum, 2)
        for i in range(len(msg_body)):
            binary_chars_sum += msg_body[i]
            binary_chars_sum, checksum = checksum_addition_overflow(binary_chars_sum)

    except ValueError:
        print(f"Error in checksum {checksum = }")

    return checksum == "0b1111111"


    
def first_handshake(sock):
    global username
    username = ""
    while True:
        
        username = input("Enter the username to log in: ")
        
        msg = f"HELLO-FROM {username}\n".encode('utf-8')

        send_full_message(sock, f"HELLO-FROM {username}\n".encode('utf-8'))
                
        msg = receive_full_msg(sock).decode('utf-8')

        if not msg:
            return False
       
        if msg == f"HELLO {username}\n":
            print(f"Welcome to the server {username}\n")
            return True
        
        elif msg == "BUSY\n":				
            print("Unfortunately servers currently reached maximum capacity of users :(")
            sock.close()
            sys.exit()
        
        elif msg == "IN-USE\n":
            print("OH NO this user name already taken :(, please create different user name")
            return False
        
        elif msg == "BAD-RQST-BODY\n":
            print("OH NO this user name is invalid :(, please create different user name")
            sock.close()
            return False
        else:
            print("An error occurred, invalid message received")  
            sock.close()
            sys.exit()



def send_message(sock):

    num_tries = 0
    while True:
        msg_event.set()
        
        user_input_text = input("Enter input: ")

        if not user_input_text:
            continue
        
        if user_input_text == "!quit":
            print("Disconnecting from server")
            sock.close()
            return
            
        elif user_input_text == "!who":
            while True :
                send_full_message(sock, "LIST\n".encode('utf-8'))
                
                timeout(4)

                if msg_acknowledged:
                    num_tries = 0
                    break  
                else:   
                    num_tries += 1
                    print("msg not received or error detected, resending")
                    msg_event.clear()
                    print(f"Number of tries attempted {num_tries}") 

        elif user_input_text[0] == '@':
            while True :
                msg_event.set()

                msg_checksum = checksum_generator(user_input_text[1:])
                send_full_message(sock, f"SEND {user_input_text[1:]}{msg_checksum}\n".encode('utf-8'))

                timeout(4)
            
                if msg_acknowledged:
                    num_tries = 0
                    break          
                else:   
                    num_tries += 1
                    print("msg not received or error detected, resending")
                    msg_event.clear() 
                    print(f"Number of tries attempted {num_tries}")

        # Change the values accordingly
        elif user_input_text == "//tests":

            set_drop = "0"  # values between 0 and 1
            set_flip = "0"   # values between 0 and 1
            set_burst = "0"
            set_burst_len_lower = "0"
            set_burst_len_upper = "0"
            set_delay = "0"
            set_delay_len_upper = "0"
            set_delay_len_lower = "0"

            user_input_text = f"SET DROP {set_drop}\nSET FLIP {set_flip}\nSET BURST {set_burst}\nSET BURST-LEN {set_burst_len_lower} {set_burst_len_upper}\nSET DELAY {set_delay}\nSET DELAY-LEN {set_delay_len_lower} {set_delay_len_upper}\n"
            send_full_message(sock, user_input_text)
            # looping error, code still works
            

        elif not (user_input_text and user_input_text[0] == '@'):
            print("Invalid input")



def get_message(sock: socket.socket):
    global msg_acknowledged
    msg_acknowledged = False

    while True:
        msg_event.wait()
        msg_acknowledged =  False

        while True:
            msg = receive_full_msg(sock).decode('utf-8')

            if not msg:
                print("No message received from server")
                msg_acknowledged = False
                break

            if msg == "BAD-DEST-USER\n":
                print("pls enter correct name, the destination user is not currently logged in.")
                msg_acknowledged = True
                msg_event.clear()
        
            elif msg == "BAD-RQST-BODY\n":            
                print("Ups body is wrong :(, please take a look at it.")
                msg_acknowledged = True
                msg_event.clear()
                break

            elif msg == "BAD-RQST-HDR\n":
                print("Ups header is wrong :(, please take a loot at it.")
                msg_acknowledged = True
                msg_event.clear()
                break

            elif msg == "SEND-OK\n":
                print("Message has been sent") 

            elif msg.startswith("VALUE"):
                print(msg)
            
            elif msg == "SET-OK\n":
                print("\nTest settings changed successfully.")

            elif msg[:8] == "DELIVERY":
                if not validate_recv_checksum(msg):
                    print(f"checksum failed validation, bit flip detected")
                    break

                msg_sender, msg_content = msg.split(" ", 2)[1:]
                msg_content = msg_content[:-10] # Erase checksum when printing

                print(f"Message from {msg_sender}: {msg_content}")

                msg_event.clear()

                if username != msg_sender:
                    send_full_message(sock, f"SEND {msg_sender} msgAcknowledged\n".encode('utf-8'))
                    break

                msg_acknowledged = True
                break
                                    
            elif msg[:7] == "LIST-OK":
                print(f"Current online users: {msg[8:]}")
                msg_event.clear()
                msg_acknowledged = True
                break
            else:
                msg_acknowledged = False



def init_new_client():
    sock, send_thread, recv_thread = None, None, None
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        send_thread = threading.Thread(target = send_message, args =(sock,), )
        recv_thread = threading.Thread(target = get_message, args = (sock,), daemon = True) 

        if first_handshake(sock):
            break

    # Sets the bit-flip rate and drop rate
    run_unreliability_tests(sock)
    
    send_thread.start()
    recv_thread.start()

    # Join the threads (recv_thread will be killed automatically)
    send_thread.join()
    
    return sock


def run_unreliability_tests(sock):
    drop_value = "0"
    tests = ["SET FLIP 0.001\n", f"SET DROP 0.1{drop_value}\n"]

    for msg in tests:
        print(f"\n{msg}")
        send_full_message(sock, msg)
        recv_msg = receive_full_msg(sock)
        print("Received test message complete\n")



if __name__ == "__main__":
    unreliable_sock = init_new_client()



def unreability_tests(sock):
    set_drop = "0"  # values between 0 and 1
    set_flip = "0"   # values between 0 and 1
    set_burst = "0"
    set_burst_len_lower = "0"
    set_burst_len_upper = "0"
    set_delay = "0"
    set_delay_len_upper = "0"
    set_delay_len_lower = "0"

    test_paramenters = f"SET DROP {set_drop}\nSET FLIP {set_flip}\nSET BURST {set_burst}\nSET BURST-LEN {set_burst_len_lower} {set_burst_len_upper}\nSET DELAY {set_delay}\nSET DELAY-LEN {set_delay_len_lower} {set_delay_len_upper}\n"

    send_full_message(sock, test_paramenters)

    # TODO make it called outside the functiom
    # TODO implement GET
    # TODO implement RESET

