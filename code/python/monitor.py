#!/usr/bin/python
import socket
import cv2
import numpy
import argparse
from utils.VJ_Logging import VJ_Logging


logger = VJ_Logging('monitor',0)

parser = argparse.ArgumentParser(description='monitor for watching stream of raspberry pi')
parser.add_argument('--ip',metavar='-ip', default='localhost', help='ip of monitor (Default = localhost)')
parser.add_argument('--port',metavar='-port', default=5001, help='port of monitor (Default = 5001)')
args = parser.parse_args()

TCP_IP = args.ip
TCP_PORT = int(args.port)

def recvall(sock, count):
    buf = b''
    if (sock is None or count is None):
        return 0
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print msg
        logger.print_log(2,'main','could not open socket')
        return
    try:
        s.bind((TCP_IP, TCP_PORT))
        s.listen(True)
    except socket.error as msg:
        print msg
        logger.print_log(2,'main','could not listen to socket')
        return
    logger.print_log(0,'main','socket created and listening on port')
    while(True):
        try:
            conn, addr = s.accept()
            length = recvall(conn,16)
            stringData = recvall(conn, int(length))
            data = numpy.fromstring(stringData, dtype='uint8')
            decimg=cv2.imdecode(data,1)
            cv2.imshow('Monitor',decimg)
            cv2.waitKey(1)
        except socket.error as msg:
            print msg
            logger.print_log(2,'main','error while reading TCP connection')

    s.close()
    cv2.destroyAllWindows()
    return


if __name__ == "__main__":
    logger.print_log(0,'main','starting Monitor')
    main()
    logger.print_log(2,'main','error while executing main')
