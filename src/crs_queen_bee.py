# crs_queen_bee.py    17Sep2020   crs, Author
"""
Simple centralized server handling / observing a number of 
clients which send asynchronous messages / requests
"""
import argparse
import socket

from select_trace import SlTrace

from queen_bee import QueenBee

parser = argparse.ArgumentParser()

host = None             # host name - default from QueenBee
port = None             # com port - default from QueenBee
parser.add_argument('--host', dest='host', default=host)
parser.add_argument('--port', type=int, dest='port', default=port)
args = parser.parse_args()             # or die "Illegal options"
host = args.host
port = args.port
SlTrace.lg("args: %s\n" % args)


qb = QueenBee(host=host, port=port)
host = qb.get_host()
port = qb.get_port()
host_ip = socket.gethostbyname(host) 

print(f"host:{host} IP: {host_ip} port: {port}")
while True:
    print("Waiting for client(s)...")
    drone = qb.get_drone()
    if drone.has_data():
        from_drone = drone.get_data()
        print("Received Message:", from_drone,
               "from", drone.get_id())
        drone.replyto(f"Got your data:[{from_drone}]")
