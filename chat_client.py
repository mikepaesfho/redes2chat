from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

lastSend = '##first##'

# classe para manipular o socket
class Send:
    def __init__(self):
        self.__msg = ''
        self.new = True
        self.con = None

    def put(self, msg):
        self.__msg = msg
        if self.con != None:
            # envia um mensagem atravez de uma conexão socket
            self.con.send(str.encode(self.__msg))

    def get(self):
        return self.__msg

    def loop(self):
        return self.new


def listen(tcp, send, host, user, port=5000):
    destino = (host, port)
    # conecta a um servidor
    tcp.connect(destino)

    while send.loop():
        # atribui a conexão ao manipulador
        send.con = tcp
        if lastSend == '##first##':
            send.put(user)

        while send.loop():
            # aceita uma mensagem
            msg = tcp.recv(1024)
            if not msg or msg == lastSend or msg == lastSend.encode("utf8"): break
            print(str(msg, 'utf-8'))


if __name__ == '__main__':
    print('chose an user name: ')
    user = input()

    host = '127.0.0.1'

    # cria um socket
    tcp = socket(AF_INET, SOCK_STREAM)
    send = Send()
    processo = Thread(target=listen, args=(tcp, send, host, user))
    processo.start()
    print('')

    msg = input()
    while True:
        lastSend = user + ': ' + msg
        send.put(lastSend)
        msg = input()

    processo.join()
    tcp.close()
    exit()
