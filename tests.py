# !/usr/bin/env python3
import os
import tempfile
import unittest
import unittest.mock
import ftp
from stubserver import FTPStubServer


class FTPTests(unittest.TestCase):
    def setUp(self):
        self.server = FTPStubServer(0)
        self.server.run()
        self.port = self.server.server.server_address[1]
        self.ftp = ftp.ftp()
        self.ftp.connect('127.0.0.1', self.port)

    def tearDown(self):
        self.ftp.close()
        self.server.stop()

    def test_connection(self):
        serv_ans = self.ftp.ftp_ans()
        self.assertEqual(serv_ans, "220 (FtpStubServer 0.1a)\r\n")

    def test_login(self):
        self.ftp.ftp_ans()
        serv_ans = self.ftp.login()
        self.assertEqual(serv_ans, "331 Please specify password.\r\n230 You are now logged in.\r\n")

    def test_list(self):
        self.ftp.ftp_ans()
        self.server.add_file("1.txt", "abracarabra")
        serv_ans = self.ftp.ls()
        self.assertEqual(serv_ans, "1.txt")

    def test_download(self):
        self.ftp.ftp_ans()
        self.server.add_file("1.txt", "abracarabra")
        with unittest.mock.patch.object(self.ftp, 'size', return_value=100):
            self.ftp.download_file("1.txt")
        with open("1.txt", "r") as file:
            ans = file.read()
        self.assertEqual(ans, "abracarabra")

    def test_pasv(self):
        reply = self.ftp.ftp_ans()
        reply = self.ftp.pasv()
        self.assertTrue(reply.startswith("227 Entering Passive Mode."))

    def test_cd(self):
        dir_name = "new_dir"
        expected = '250 OK. Current directory is "' + dir_name + '"\r\n'
        self.ftp.cd(dir_name)
        self.assertEqual(self.ftp.send_comand("PWD"), expected)

if __name__ == '__main__':
    unittest.main()
