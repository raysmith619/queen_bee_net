# crs_talking_chair    06Oct2020   crs, Author
"""
Simplest test of UDP - server (queen bee)
Usage: <pgm>
    [port]        #  default 50001
    [-b [bind addr}] # bind address default addr: 0.0.0.0
Acts as target for py's and displays received message
"""
import socket
import sys

from queen_proc import QueenProc

pgm = sys.argv[0]
our_name = socket.gethostname()
our_ip = socket.gethostbyname(our_name)
port = 50001
bind_addr = "0.0.0.0"
args = sys.argv[1:] if len(sys.argv) > 1 else []
if len(args) > 0 and not args[0].startswith("-"):    
    port = int(args.pop(0))
if len(args) > 0:
    if args[0] == "-b":
        args.pop(0)
        bind_addr = "0.0.0.0" if len(args) == 0 else args.pop(0)
print(f"{pgm}\n run on {our_name} {our_ip}")
family = socket.AF_INET
sock_type = socket.SOCK_DGRAM
sock = socket.socket(family, sock_type)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print(f"{our_name} ip: {our_ip} port: {port}")
if bind_addr is not None:
    print(f"binding to address: {bind_addr}")
    sock.bind((bind_addr, port))
else:
    sock.bind((our_name, port))

qproc = QueenProc(sock=sock)
cmd_prefix = "!!"
while True:
    print("Waiting for client(s)...")
    data,addr = sock.recvfrom(1024)     #receive data from client
    msg = data.decode("utf-8")
    print(f"Received Message: {msg} addr: {addr}")
    if msg.startswith(cmd_prefix):
        cmd = msg[len(cmd_prefix):]
        qproc.cmd_proc(cmd, addr)
    else:
        ret_msg = f"{our_name} recieved:[{msg}]"
        ret_data = bytes(ret_msg, "utf-8")
        sock.sendto(data, addr)
