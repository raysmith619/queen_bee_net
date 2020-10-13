# drone_bee.py    17Sep2020  crs, Author
"""
Drone - client to QueenBee
"""
import socket

class DroneBeeData:
    
    def __init__(self, queen_bee, data=None, address=None):
        """ Setup drone processing
        :queen_bee: controling instance of QueenBee
        :data: received data
        :address: received address 
        """
        self.queen_bee = queen_bee
        self.data = data
        self.address = address
        
        
    def get_data(self):
        """ Get data as string
        """
        data = self.data
        if type(data) == bytes:
            data = data.decode("utf-8")
        return data
    
    def get_id(self):
        return self.address
    
    def has_data(self):
        if self.data is not None and len(self.data) > 0:
            return True
        
        return False
    
    def replyto(self, reply):
        """ Send Reply text to drone
        :reply: reply text
        """
        if type(reply) != bytes:
            data = bytes(reply, "utf-8")
        else:
            data = reply
        self.queen_bee.sock.sendto(data, self.address)
    
    
