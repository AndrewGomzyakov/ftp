import socket
import re
import argparse
import ftp
import sys


def main():
    a = ftp.ftp()
    args = parse_args(sys.argv)
    a.connect(socket.gethostbyname(args.adr), args.port)
    print(a.ftp_ans())
    print(a.login())
    while True:
        comand = input("->")
        if comand == 'LIST':
            a.ls()
        elif comand == 'QUIT':
            a.close()
            break
        elif comand == "USER":
            name = input("Username: ")
            a.login(name)
        elif comand[:3] == "CWD":
            dir = comand[4:]
            a.cd(dir)
        elif comand[:3] == "MKD":
            dir = comand[4:]
            a.md(dir)
        elif comand[:4] == "RETR":
            file_name = comand[5:]
            a.download_file(file_name)
        elif comand == "PWD":
            print(a.send_comand(comand))
        elif comand == "FEAT":
            print(a.send_comand(comand))
        elif comand == "HELP":
            print(a.send_comand(comand))
        elif comand[:4] == "SIZE":
            file_name = comand[5:]
            a.size(file_name)
        elif comand[:4] == "STOR":
            file_name = comand[5:]
            a.upload_file(file_name)

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-adr", dest="adr", type=str,  help='Адрес FTP сервера')
    parser.add_argument('-port', dest="port", help='Задает порт для подключения(по умолчанию 21)', type=int, default=21)
    rez = parser.parse_args(args[1:])
    return rez

main()