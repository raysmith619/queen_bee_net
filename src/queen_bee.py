# queen_bee.py    17Sep2020  crs, Author
"""
Establish a centralized "queen bee" process to facilitate
communications betwee separate clients
"""
import socket
###from numpy import block

from select_trace import SlTrace

from drone_bee_data import DroneBeeData

class QueenBee:
    family = socket.AF_INET
    type = socket.SOCK_DGRAM
    host = socket.gethostname()
    port = 12345
    sock = None             # Socket for listening, setup on first get_drone
    """Centralized controling server
    """
    def __init__(self, family=socket.AF_INET, type=socket.SOCK_DGRAM,
            host=None, bind_addr=None, port=None):
        """ Setup queen_bee as server
        :family: socket family default: AF_INET
        :type: socket type default: UDP
        :host: default: this computer
        :bind_addr: binding address default: 0.0.0.0
        :port: default: QueenBee.port
        """
        self.family = family
        self.type = type
        if host is None:
            host = QueenBee.host
        self.host = host
        if port is None:
            port = QueenBee.port
        self.port = port
        if bind_addr is None:
            bind_addr = "0.0.0.0"
        self.bind_addr = bind_addr
 
    def get_family(self):
        return self.family
    
    def get_type(self):
        return self.type
    
    def get_host(self):
        return self.host
    
    def get_port(self):
        return self.port
    
    
    def get_drone(self, wait=None, length=1024):
        """ Get next drone communication
        :wait: ammount of seconds to wait/block 
            default: block
        :length: max number of bytes to read buffer
                default: 1024
        """
        if self.sock is None:
            SlTrace.lg(f"QueenBee host:{self.host} port:{self.port}")
            self.sock = socket.socket(self.family, self.type)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.bind_addr,self.port))

        data,addr = self.sock.recvfrom(1024)            #receive data from client
        return DroneBeeData(self, data, addr)
