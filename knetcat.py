import socket
import sys, getopt
import select, signal
#import threading
#from time import sleep

server = False
port = 6969
host = "0.0.0.0"
recv_size = 8192
#stoprequest = threading.Event()
rt = ""

def usage():
    sys.stdout.write("Server mode usage: knetcat -l <ip address> <port>\n")
    sys.stdout.write("Client mode usage: knetcat <ip address> <port>\n")

def signal_handler(signal, frame):
    #stoprequest.set()
    #rt.join(stoprequest)
    sys.exit(0)

def serverrun(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    if select.select([sys.stdin,],[],[],0.0)[0]:
        c, addr = s.accept()
        for line in sys.stdin.readlines():
            c.send(line)
    else:
        c, addr = s.accept()
        while True:
            data = c.recv(recv_size)
            if not data: break
            sys.stdout.write(data)
    try:
        c.shutdown(1)
    except socket.error as ser:
        sys.stdout.write("Socket error, continuing\n")
    c.close()

def recv_thread(s):
    while not stoprequest.isSet():
        data = s.recv(recv_size)
        sys.stdout.write(data)
        sleep(0.4)

def clientrun(host, port):
    if select.select([sys.stdin,],[],[],0.0)[0]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = socket.socket()
        s.connect((host, port))
        for line in sys.stdin.readlines():
            s.send(line)
        s.shutdown(1)
        s.close()
    elif not sys.stdout.isatty():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = socket.socket()
        s.connect((host, port))
        while True:
            data = s.recv(recv_size)
            if not data: break
            sys.stdout.write(data)
        s.shutdown(1)
        s.close()
    elif sys.stdout.isatty():
        buf = ""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = socket.socket()
        s.connect((host, port))
        #rt = threading.Thread(target=recv_thread, args=(s,)).start()
        while True:
            buf = sys.stdin.readline()
            if buf != "":
                s.send(buf)
            while True:
                data = s.recv(recv_size)
                if not data: break
			
                sys.stdout.write(data)
        s.close()

def main(server=False):
    if server == True:
        serverrun(host, port)
    elif server == False:
        clientrun(host, port)

argv = sys.argv[1:]
if len(argv) == 3:
    server = True
    host = sys.argv[2]
    port = int(sys.argv[3])
elif len(argv) == 2:
    server = False
    host = sys.argv[1]
    port = int(sys.argv[2])
else:
    usage()
    exit(0)
    
if '-h' in sys.argv[1:]:
    usage()
    exit(0)
	
signal.signal(signal.SIGINT, signal_handler)

main(server)
