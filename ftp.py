import socket
import re

class ftp:
    def __init__(self):
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket = None
        self.control_socket.settimeout(2)

    def connect(self, adr, port):
        self.control_socket.connect((adr, port))

    def send_comand(self, comand):
        self.control_socket.sendall(bytes(comand + "\n", 'ASCII'))
        return self.ftp_ans()


    def download_file(self, file_name):
        file_size = int(self.size(file_name))
        recv = 0
        res = b''
        with open(file_name, "wb") as out:
            self.pasv()
            print(self.send_comand("TYPE I"))
            print(self.send_comand("RETR " + file_name))
            ans = b""
            while recv < file_size:

                    tmp = self.data_socket.recv(65535)
                    if not tmp:
                        break
                    recv += len(tmp)
                    ans += tmp
            out.write(ans)
            print(recv)

        self.data_socket.close()

        print(self.ftp_ans())

    def upload_file(self, file_name):
        self.pasv()
        print(self.send_comand("STOR " + file_name))
        with open(file_name, "rb") as inp:
            for i in inp:
              self.data_socket.sendall(i)

    def ftp_ans(self):
        reply = ''
        tmp = self.control_socket.recv(65535).decode('ASCII')
        reply += tmp
        first_reply_reg = re.compile(r'^\d\d\d .*$', re.MULTILINE)
        while not re.findall(first_reply_reg, tmp):
            try:
                tmp = self.control_socket.recv(65535).decode('ASCII')
                reply += tmp
            except TimeoutError:
                break
        return reply

    def cd(self, dir):
        print(self.send_comand("CWD " + dir))

    def md(self, dir):
        print(self.send_comand("MKD " + dir))

    def size(self, file_name):
        self.send_comand("TYPE I")
        s = self.send_comand("SIZE " + file_name).split(" ")[1]
        self.send_comand("TYPE A")
        return s

    def login(self, name=None):
        if name == None:
            nm = self.send_comand("USER anonymous")
            print(nm)
            pas = self.send_comand("PASS pass")
        else:
            nm = self.send_comand("USER " + name)
            print(nm)
            psw = input("Password: ")
            pas = self.send_comand("PASS " + psw)
        print(pas)

    def pasv(self):
        reply = self.send_comand('PASV')
        print(reply)
        reg = r'(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)'
        res = re.findall(reg, reply)[0]
        ip_address = '.'.join(res[:4])
        port_number = int(res[4]) * 256 + int(res[5])
        parameters = (ip_address, port_number)
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket.connect(parameters)
        print(parameters)
        self.data_socket.settimeout(3)


    def ls(self):
        self.pasv()
        print(self.send_comand("LIST"))
        print(self.data_socket.recv(65535).decode('ASCII'))
        print(self.data_socket.recv(65535).decode('ASCII'))
        self.data_socket.close()
        print(self.ftp_ans())

    def port(self):
        pass

    def close(self):
        rep = self.send_comand("QUIT")
        if self.data_socket:
            self.data_socket.close()
        self.control_socket.shutdown(socket.SHUT_RDWR)
        self.control_socket.close()
        return rep

    def feat(self):
        print(self.send_comand("FEAT"))


