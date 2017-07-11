import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d','--dest', help='Destination Host', required=True)
parser.add_argument('-p','--port', help='Destination Port', required=True, type=int)
args = parser.parse_args()

s = socket.socket()
host = args.dest
port = args.port

try:
    s.connect((host,port))
    print("Connection to host:%s at port:%d is Successful!" % (host,port))
except Exception as e:
    print("Connection to host:%s at port:%d FAILED! Exception=%s" % (host,port,e))
finally:
    s.close()
