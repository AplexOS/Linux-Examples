#!/usr/bin/python3

from ftplib import FTP
import os,sys,string,datetime,time
import socket
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)

class ftp_upgrade():
    def __init__(self):
        pass
        #self.auto_download()

    def __del__(self):
        self.ftp.close()

    def auto_download(self):
        hostaddr = "101.201.118.185"
        username = "ftpadmin"
        password = "123456"
        port = 21
        rootdir_local  = '.' + os.sep + 'bak/'
        rootdir_remote = './'

        self.localfile = "/opt/upgrade.tar"
        self.remotefile = "upgrade.tar"

        self.hostaddr = hostaddr
        self.username = username
        self.password = password
        self.remotedir = rootdir_remote
        self.port = port
        self.ftp = FTP()
        self.file_list = []

        self.login()

        self.download_file(self.localfile, self.remotefile)

    def login(self):
        ftp = self.ftp
        try:
            timeout = 60
            socket.setdefaulttimeout(timeout)
            ftp.set_pasv(True)
            logging.debug("Start connect")
            ftp.connect(self.hostaddr, self.port)
            logging.debug("connect success")

            logging.debug("start login")
            ftp.login(self.username, self.password)
            logging.debug("login success")
        except Exception:
            logging.debug("connect or login failed")

        try:
            ftp.cwd(self.remotedir)
        except Exception:
            logging.debug("change direction error")

    def is_same_size(self, localfile, remotefile):
        try :
            remotefile_size = self.ftp.size(remotefile)
        except:
            remotefile_size = -1

        try:
            localfile_size = os.path.getsize(localfile)
        except :
            localfile_size = -1

        if (remotefile_size == localfile_size):
            return 1
        else :
            return 0

    def download_file(self, localfile, remotefile):
        if self.is_same_size(localfile, remotefile):
            logging.debug("file size same,..")
            return
        else:
            file_handler = open(localfile, 'wb')
            self.ftp.retrbinary('RETR %s' % (remotefile), file_handler.write)
            file_handler.close()

    def auto_update(self):
        os.system("sync")
        tar_cmd = "tar -xvf " + self.localfile + " -C /usr/share/sensor/"
        os.system(tar_cmd)
        os.system("sync")
        rm_cmd = "rm " + self.localfile
        os.system(rm_cmd)
        os.system("sync")

if __name__ == "__main__":
    test = ftp_upgrade()
    test.auto_download()

