import socket
import re
import argparse
import ftp


def main():
    a = ftp.ftp()
    a.connect("212.193.68.227", 21)
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








def parse_args():
    parser = argparse.ArgumentParser(prog='ftp.py', description='Connects to ftp server')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('address', help='address to connect')
    parser.add_argument('port', help='port', nargs='?', type=int, default=21)
    parser.add_argument('--passive', help='use passive mode instead of active', action='store_true')
    group.add_argument('--get', '-g', help='dowload file', action='store_true')
    group.add_argument('--put', '-p', help='upload file', action='store_true')
    parser.add_argument('--local', '-l', help='local file to handle')
    parser.add_argument('--remote', '-r', help='remote file to handle')
    return parser.parse_args()

main()