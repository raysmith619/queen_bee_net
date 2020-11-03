# queen_bee.py    17Sep2020  crs, Author
"""
Establish a centralized "queen bee" process to facilitate
communications between
    1. queen bee and clients
The queen keeps a set of clients and for each client:
    1. send address
    2. name
"""
import socket
###from numpy import block

from select_trace import SlTrace
from queen_bee_server import QueenBeeServer
from drone_bee_data import DroneBeeData

class QueenBee:
    sock = None             # Socket for listening, setup on first get_drone
    """Centralized controling server
    """
    def __init__(self, family=socket.AF_INET, stype=socket.SOCK_DGRAM,
            port=None):
        """ Setup queen_bee as server
        :family: socket family default: AF_INET
        :type: socket type default: UDP
        :port: default: QueenBee.port
        """
        self.family = family
        self.stype = stype
        self.port = port
        self.bind_addr = "localhost"
        self.drones = {}    # drones (DroneBeeData) by address
        self.server = QueenBeeServer(family=self.family,
                                      stype=self.stype,
                                      port=self.port)
    def get_family(self):
        return self.family
    
    def get_type(self):
        return self.type
    
    def get_port(self):
        return self.port

    def get_drones(self, pending_input=True, ):
        """ Get active drones
        :pending_input: True - just with pending input
                    default: True
        :returns: list of DroneBeeData
        """
        pass
    
    def send_msg(self, msg, drones=None):
        """ Send message to zero or more drones
        :msg: message to send, if not bytes convert to bytes
        :drones: DroneBeeData or list of
                None - send to all drones
        """
        if drones is None:
            drones = self.drones.keys()
        if drones is not list:
            drones = [drones]   # list of one
        for drone in drones:
            self.send_msg_to(msg, drone)
