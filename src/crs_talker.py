# crs_talker.py    06Oct2020   crs, Paired down from crs_drone_bee, drone_bee
"""
UDP - chat client (drone bee)
Usage: <pgm> [hostname/ip]
    default: localhost
    "our_name": uses gethostname()
Uses tkinter to graphically display talker with
messages from other talkers
Sends messages to host
"""
import socket
import sys
import os 
import tkinter as tk

port = 12345             # com port
sock_timeout = 5
print(sys.argv)
pgm = sys.argv[0]
our_name = socket.gethostname()
our_ip = socket.gethostbyname(our_name)
print(f"{pgm}\n run on {our_name} {our_ip}")
qbinfo = "qb.txt"   # Get host, info from file
if os.path.exists(qbinfo):
    with open(qbinfo) as qbif:
        qbinfo_line = qbif.read()
        host, port = qbinfo_line.split()
        port = int(port)

if len(sys.argv) > 1:
    host_name = sys.argv[1]
    if host_name == "our_name":
        host_name = our_name     # Used internal name
    host = host_name
if len(sys.argv) > 2:
    port = sys.argv[2]
    port = int(port)
host_ip = socket.gethostbyname(host)
print(f"host:{host} IP: {host_ip} port: {port}")
family = socket.AF_INET
sock_type = socket.SOCK_DGRAM
sock = socket.socket(family, sock_type)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.settimeout(sock_timeout)
print("Press the space key to Enter msg")

def print_if_msg():
    ck_time = .01    
    try:
        sock.settimeout(ck_time)
        rep_data, rep_addr = sock.recvfrom(1024)
        rep_msg = rep_data.decode("utf-8")
        from_loc, msg = rep_msg.split(maxsplit=1)
        print(f"{from_loc}({rep_addr}): {msg}")
    finally:
        sock.settimeout(sock_timeout)
    
mw = tk.Tk()
msg_entry = None        # Set when ready

def msg_proc():
    print("entry change")
    msg = msg_entry.get
    data = bytes(msg, "utf-8")
    sock.sendto(data, (host, port))        # Sending message to UDP server
    sock.settimeout(sock_timeout)
    try:
        rep_data, rep_addr = sock.recvfrom(1024)
        rep_msg = rep_data.decode("utf-8")
        print(f"\tReply:{rep_msg} from {rep_addr}")
    except:
        print(f"\tNo reply after {sock_timeout} seconds")

ml_frame = tk.Frame(mw)
ml_frame.pack(side=tk.TOP)
ml_label = tk.Label(ml_frame, text="Enter Message")
ml_label.pack(side = tk.LEFT)
ml_send_btn = tk.Button(ml_frame, text="Send")
ml_send_btn.pack(side=tk.RIGHT)
msg_entry = tk.Entry(mw, bd =5)
msg_entry.pack(side = tk.TOP)
msg_label = tk.Label(mw, text="From Others")
msg_label.pack(side = tk.TOP)
msg_entry = tk.Entry(mw, bd=5)
msg_entry.pack(side=tk.TOP)


tk.mainloop()
 