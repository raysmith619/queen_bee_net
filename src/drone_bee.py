# drone_bee.py    17Sep2020  crs, Author
"""
Drone - client to QueenBee
"""
import socket

###from select_trace import SlTrace

from queen_bee import QueenBee

class DroneBee:
    
    def __init__(self, family=None, type=None,
            host=None, port=None, datalen=1024,
            timeout=5):
        """ Setup drone to talk to the QueenBee
        :family: socket family default: QueenBee.family
        :type: socket type default: QueenBee.type
        :host: queen's host default: QueenBee.host
        :host_port: com port default: QueenBee.port
        :timeout: recv timeout in sec default:5
        """
        if family is None:
            family = QueenBee.family
        self.family = family
        if type is None:
            type = QueenBee.type
        self.type = type
        if host is None:
            host = QueenBee.host
        self.host = host
        if port is None:
            port = QueenBee.port
        self.port = port
        ###SlTrace.lg(f"DroneBee host:{self.host} port:{port}")
        self.sock = socket.socket(self.family, self.type)
        self.datalen = datalen
        self.sock_timeout = timeout
        self.sock.settimeout(self.sock_timeout)
        
    def send(self, data):
        """ Send data from drone to queen
        :data: data(str or bytes) to send
        """
        if type(data) != bytes:
            data = bytes(data, "utf-8")
        self.sock.sendto(data, (self.host, self.port))        # Sending message to UDP server
         
    def get_reply(self):
        """ Get reply as string
        """
        try:
            data,addr = self.sock.recvfrom(self.datalen)
            msg = data.decode('utf-8')
        except:
            print(f"\tNo reply after {self.sock_timeout} seconds")
            msg = None
        return msg
    
