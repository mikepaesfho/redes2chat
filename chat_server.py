import socket
import sys
import traceback
from threading import Thread

connection_list = []

def main():
    start_server()


def start_server():
    host = "127.0.0.1"
    port = 5000         # arbitrary non-privileged port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    print("Initializate")

    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(50)       # queue up to 5 requests
    print("Ready")

    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

    soc.close()


def client_thread(connection, ip, port, max_buffer_size = 5120):
    is_active = True
    user = ''
    connection_list.append(connection)

    while is_active:
        try:
            client_input = receive_input(connection, max_buffer_size)
            if user == '':
                user = client_input
                client_input = user + " connected with " + ip + ":" + port

            if "--QUIT--" in client_input:
                connection.close()
                client_input = user + " connection " + ip + ":" + port + " closed"
                print(client_input)
                is_active = False
            else:
                print(client_input)
        except:
            client_input = "Connection " + ip + ":" + port + " closed"
            is_active = False

        send_all_connections(client_input.encode("utf8"))


def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    return str(decoded_input)

def send_all_connections(text):
    for connect in connection_list:
        try:
            connect.sendall(text)
        except:
            connection_list.remove(connect)

if __name__ == "__main__":
    main()