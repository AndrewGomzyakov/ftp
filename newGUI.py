import sys
import ftp
import argparse
import socket
import getpass
import re
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMainWindow, QLabel
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
    QInputDialog, QApplication)


class MyButton(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        button = event.button()
        if button == Qt.RightButton:
            print(self.text())
        else:
            self.click()
        return


class Dialog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn = QPushButton('Применить настройки', self)
        self.btn.move(130, 102)
        self.btn.clicked.connect(self.start_client)
        self.adrt = QLabel("Адрес", self)
        self.portt = QLabel("Порт",self)
        self.logint = QLabel("Логин", self)
        self.pswt = QLabel("Пароль", self)

        self.adrt.move(20, 22)
        self.portt.move(20, 42)
        self.logint.move(20, 62)
        self.pswt.move(20, 82)

        self.adr = QLineEdit(self)
        self.port = QLineEdit(self)
        self.login = QLineEdit(self)
        self.psw = QLineEdit(self)
        self.adr.move(130, 22)
        self.port.move(130, 42)
        self.login.move(130, 62)
        self.psw.move(130, 82)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Settings')
        self.show()

    def start_client(self):
        adr = self.adr.text()
        psw = self.psw.text()
        port = self.port.text()
        login = self.login.text()
        if adr != "" and psw != "" and port != "" and login != "":
            self.close()
            GUI(adr, port, login, psw)


class GUI(QWidget):
    def __init__(self, adr, port, login, psw):
        super().__init__()
        self.buttons = []
        self.layout = None
        self.parent_dir = ["/"]
        self.a = ftp.ftp()
        #args = self.parse_args(["q", "-a", "shannon.usu.edu.ru"])
        self.a.connect(socket.gethostbyname(adr), int(port))
        print(self.a.ftp_ans())
        if login:
            ans = (self.a.login(login, psw))
            if ans == -1:
                return
        else:
            print(self.a.login())
        self.initUI()


    def parse_args(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', dest="port", help='Задает порт для подключения(по умолчанию 21)', type=int,
                            default=21)
        parser.add_argument("--login", dest="login", type=str, help="Задает логин для входа на сервер")
        requiredNamed = parser.add_argument_group('required named arguments')
        requiredNamed.add_argument("-a", dest="adr", type=str, help='Адрес FTP сервера', required=True)
        rez = parser.parse_args(args[1:])
        return rez

    def list_info(self, ftp):
        strs = ftp.ls().split("\n")
        ans = []
        for i in strs:
            words = []
            for j in i.split(" "):
                if j != "":
                    words.append(j)
            if len(words) > 5:
                tmp = []
                tmp.append("Size: " + words[4])
                tmp.append("Last changes: " + words[6] + " " + words[5] + " " + words[7])
                dir = ftp.send_comand("PWD")
                dir = dir[5:-2]
                tmp.append(dir)
                ans.append(tmp)
        #print(ans)
        return ans

    def list_names(self, ftp):
        print(ftp.send_comand("PWD"))
        past_dir = re.findall(r"\"(.*)\"", ftp.send_comand("PWD"))[0]
        list = []
        strs = ftp.ls().split("\n")
        for i in strs:
            if len(re.findall(r" ([\w\-_\.]*)\r$", i)) > 0:
                type = -1
                text = ftp.send_comand("CWD " + i)[:3]
                i = re.findall(r" ([\w\-_\.]*)\r$", i)[0]
                if ftp.send_comand("CWD " + i)[:3] == "250":
                    ftp.send_comand("CWD " + past_dir)
                    type = 1
                else:
                    type = 0
                list.append((i, type))
        return list

    def push(self, btn, f):
        if self.sender().text()[0] == "О":
            dir2 = self.sender().text()[14:]
            self.open_dir(f, dir2)
        elif self.sender().text()[0] == "С":
            dir2 = self.sender().text()[13:]
            f.download_file(dir2)
        elif self.sender().text()[0] == "В":
            if len(self.parent_dir) > 1:
                self.parent_dir.pop(-1)
            dir2 = ""
            for i in range(1, len(self.parent_dir)):
                dir2 += "/" + self.parent_dir[i]
            if len(self.parent_dir) == 1:
                dir2 = "/"
            self.open_dir(f, self.parent_dir[0])
        else:
            dir = f.send_comand("PWD")
            dir = dir[5:]
            i = len(dir) - 1
            while dir[i] != "/":
                i -= 1
            if dir[:i] == "":
                self.open_dir(f, "/")
            else:
                self.open_dir(f, dir[:i])


    def open_dir(self, ftp, dir):
        self.parent_dir.append(dir)
        ftp.cd(dir)
        buttons_names = self.list_names(ftp)
        buttons_info = self.list_info(ftp)
        self.list_info(ftp)
        for bt in self.buttons:
            self.layout.removeWidget(bt)
            bt.setParent(None)
        self.buttons = []
        pos = [(i, j) for i in range(10) for j in range(5)]
        for i in range(len(buttons_names)):
            print(buttons_names[i])
            info = ""
            for j in buttons_info[i]:
                info += j + "\n"
            if buttons_names[i][1] == 1:
                b = MyButton("Открыть папку " + buttons_names[i][0], self)
                self.buttons.append(b)
                self.buttons[-1].setCheckable(True)
                self.buttons[-1].clicked.connect(lambda:self.push(self.buttons[-1], ftp))
                self.buttons[-1].setToolTip(info)
                self.layout.addWidget(self.buttons[-1], *pos[i])
            else:
                b = MyButton("Скачать файл " + buttons_names[i][0], self)
                self.buttons.append(b)
                self.buttons[-1].setCheckable(True)
                self.buttons[-1].clicked.connect(lambda: self.push(self.buttons[-1], ftp))
                self.buttons[-1].setToolTip(info)
                self.layout.addWidget(b, *pos[i])
        b = MyButton("Вернуться в корневую папку", self)
        self.buttons.append(b)
        self.buttons[-1].setCheckable(True)
        self.buttons[-1].clicked.connect(lambda: self.push(self.buttons[-1], ftp))
        self.layout.addWidget(b, *pos[len(buttons_names)])
        p = MyButton("Назад", self)
        self.buttons.append(p)
        self.buttons[-1].setCheckable(True)
        self.buttons[-1].clicked.connect(lambda: self.push(self.buttons[-1], ftp))
        self.layout.addWidget(p, *pos[len(buttons_names) + 1])
        self.update()
        self.show()


    def initUI(self):

        layout = QGridLayout()
        self.layout = layout
        buttons_names = self.list_names(self.a)
        buttons_info = self.list_info(self.a)
        pos = [(i, j) for i in range(max(len(buttons_names) // 3, 1)) for j in range(4)]
        for i in range(len(buttons_names)):
            info = ""
            for j in buttons_info[i]:
                info += j + "\n"
            if buttons_names[i][1] == 1:
                b = MyButton("Открыть папку " + buttons_names[i][0], self)
                b.setCheckable(True)
                b.clicked.connect(lambda:self.push(b, self.a))
                self.buttons.append(b)
                self.buttons[-1].setToolTip(info)
                self.layout.addWidget(b, *pos[i])
            else:
                b = MyButton("Скачать файл " + buttons_names[i][0], self)
                self.buttons.append(b)
                self.buttons[-1].setCheckable(True)
                self.buttons[-1].clicked.connect(lambda: self.push(self.buttons[-1], self.a))
                self.buttons[-1].setToolTip(info)
                self.layout.addWidget(b, *pos[i])
        b = MyButton("Вернуться в корневую папку", self)
        self.buttons.append(b)
        self.buttons[-1].setCheckable(True)
        self.buttons[-1].clicked.connect(lambda: self.push(self.buttons[-1], self.a))
        self.layout.addWidget(b, *pos[len(buttons_names)])
        p = MyButton("Назад", self)
        self.buttons.append(p)
        self.buttons[-1].setCheckable(True)
        self.buttons[-1].clicked.connect(lambda: self.push(self.buttons[-1], ftp))
        self.layout.addWidget(p, *pos[len(buttons_names) + 1])
        self.setLayout(layout)
        self.update()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dialog()
    sys.exit(app.exec_())