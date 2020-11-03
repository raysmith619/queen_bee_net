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
        """ Get most recent data as string
        """
        return self.data
    
    def get_id(self):
        return self.address
    
    def has_data(self):
        if self.data is not None and len(self.data) > 0:
            return True
        
        return False
    
    def sendto(self, data):
        """ Send data to drone
        :data: data to send to drone
        """
        if type(data) != bytes:
            data = bytes(data, "utf-8")
        self.queen_bee.sock.sendto(data, self.address)
    
    
