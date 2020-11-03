# crs_db.py    06Oct2020   crs, Paired down from crs_drone_bee, drone_bee
"""
Simplest test of UDP - client (drone bee)
Usage: <pgm> [hostname/ip]
    default: localhost
    "our_name": uses gethostname()
Prompts operator for text message
Sends this message to "host"
"""
import socket
import sys

host = "localhost"
port = 12345---             # com port
sock_timeout = 5
print(sys.argv)
pgm = sys.argv[0]
our_name = socket.gethostname()
our_ip = socket.gethostbyname(our_name)
print(f"{pgm}\n run on {our_name} {our_ip}")
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
while True:
    msg = input("Enter msg:")
    data = bytes(msg, "utf-8")
    sock.sendto(data, (host, port))        # Sending message to UDP server
    try:
        rep_data, rep_addr = sock.recvfrom(1024)
        rep_msg = rep_data.decode("utf-8")
        print(f"\tReply:{rep_msg} from {rep_addr}")
    except:
        print(f"\tNo reply after {sock_timeout} seconds")
