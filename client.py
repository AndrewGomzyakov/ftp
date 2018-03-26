import socket
import re
import argparse
import ftp
import sys
import getpass


def main():
    a = ftp.ftp()
    args = parse_args(sys.argv)
    print(args)
    a.connect(socket.gethostbyname(args.adr), args.port)
    #a.connect(socket.gethostbyname("ftp.mccme.ru"), 21)
    print(a.ftp_ans())
    if args.login:
        psw = getpass.getpass()
        ans = (a.login(args.login, psw))
        if ans == -1:
            return
        else:
            print(ans)
    else:
        print(a.login())
    while True:
        comand = input("->")
        if comand.upper() == 'LIST':
            print(a.ls())
        elif comand.upper() == 'QUIT':
            a.close()
            break
        elif comand.upper() == "USER":
            name = input("Username: ")
            a.login(name)
        elif comand[:3].upper() == "CWD":
            dir = comand[4:]
            a.cd(dir)
        elif comand[:3].upper() == "MKD":
            dir = comand[4:]
            a.md(dir)
        elif comand[:4].upper() == "RETR":
            file_name = comand[5:]
            a.download_file(file_name)
        elif comand.upper() == "PWD":
            print(a.send_comand(comand))
        elif comand.upper() == "FEAT":
            print(a.send_comand(comand))
        elif comand.upper() == "HELP":
            print(a.send_comand(comand))
        elif comand[:4].upper() == "SIZE":
            file_name = comand[5:]
            print(a.size(file_name))
        elif comand[:4].upper() == "STOR":
            file_name = comand[5:]
            a.upload_file(file_name)
        elif comand[:2].upper() == "LA":
            cur_dir = comand[3:]
            a.rec_list(0, cur_dir)
        elif comand[:4].upper() == "LOAD":
            cur_dir = comand[5:]
            a.rec_download(cur_dir)

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest="port", help='Задает порт для подключения(по умолчанию 21)', type=int, default=21)
    parser.add_argument("--login", dest="login", type=str, help="Задает логин для входа на сервер")
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument("-a", dest="adr", type=str,  help='Адрес FTP сервера', required=True)
    rez = parser.parse_args(args[1:])
    return rez

if __name__ == '__main__':
    main()
