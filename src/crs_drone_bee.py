# crs_drone_bee.py    17Sep2020  crs, Author
""" Simple case of drone to test crs_queen_bee
"""
import argparse
import socket

###from select_trace import SlTrace

from queen_bee import QueenBee
from drone_bee import DroneBee
host = None             # host name - default from QueenBee
port = None             # com port - default from QueenBee
parser = argparse.ArgumentParser()

parser.add_argument('--host', dest='host', default=host)
parser.add_argument('--port', type=int, dest='port', default=port)
args = parser.parse_args()             # or die "Illegal options"
host = args.host
port = args.port
###SlTrace.lg("args: %s\n" % args)

qb = QueenBee(host=host, port=port)
if host is None:
    host = qb.get_host()
if port is None:
    port = qb.get_port()
host_ip = socket.gethostbyname(host) 

print(f"host:{host} IP: {host_ip} port: {port}")

db = DroneBee(host=host, port=port)
while True:
    cmd = input("Enter command:")
    db.send(cmd)
    reply = db.get_reply()
    if reply is not None:
        print(f"Reply from server: \"{reply}\"")
