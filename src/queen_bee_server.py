# queen_bee_server.py    03Nov20Nov2020  starting from stk_socket_server.py
# https://steelkiwi.com/blog/working-tcp-sockets/
"""
Thread based socket server
Setup do the server - client interaction
No automatic echoing of inputs

"""

import select, socket, sys, queue

from select_trace import SlTrace

from queen_bee_server_thread import QueenBeeServerThread
import socketserver

class QueenConversation:
    """ Conversation sockets, msg queues
    """
    def __init__(self, socket=None):
        """ Setup sockets, message queues
        :socket: socket used for input and output
        """
        self.socket = socket
        self.input_msg_queue = queue.Queue()
        self.output_msg_queue = queue.Queue()
        
class QueenBeeServer:
    
    def __init__(self, family=socket.AF_INET, stype=socket.SOCK_DGRAM,
                 port=50003):
        self.family = family
        self.stype = stype
        self.port = port
        self.server = socket.socket(self.family, self.stype)
        self.server.setblocking(0)
        self.server.bind(('localhost', self.port))
        self.inputs = [self.server]
        self.outputs = []         # sockets with with pending out
                                            
        self.conversations = {}      # conversations
        self.exitFlag = 0       # Set nonzero to quit
        SlTrace.lg("QueenBeeServer setup")
        
    def run(self):
        SlTrace.lg("QueenBeeServer running")
        while self.exitFlag == 0:        
            readable, writable, exceptional = select.select(
                self.inputs, self.outputs, self.inputs)
            for s in readable:
                if s is self.server:
                    connection, client_address = s.accept()
                    connection.setblocking(0)
                    self.inputs.append(connection)
                    qcv = QueenConversation(connection)
                    self.conversations[connection] = qcv
                    SlTrace.lg(f"New connection {connection}")
                else:
                    data = s.recv(1024)
                    if data:
                        qcv = self.self.conversations[s]
                        qcv.input_msg_queue.put(data)
                        SlTrace.lg(f"New data {s} data: {data}")
        
            for s in writable:      # TBD may want to avoid checking all
                try:
                    qcv = self.self.conversations[s]
                    next_msg = qcv.output_msg_queue.get_nowait()
                except queue.Empty:
                    self.outputs.remove(s)
                else:
                    if type(next_msg) != type(bytes):
                        next_msg = bytes(next_msg, "utf-8")
                    s.send(next_msg)
        
            for s in exceptional:
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()
                del self.message_queues[s]

    def get_msgs(self, from_addrs=None, decode=True):
        """ Get pending message(s)
        :from_addr: one or list of connections default: ALL
        :decode: convert bytes to text default: True - decode
        :returns: list of tuples (socket, message)
        """
        addr_msgs = []
        if from_addrs is None:
            from_addrs = self.conversations.keys()
        if from_addrs is not list:
            from_addrs = [from_addrs]
        for addr in from_addrs:
            qcv = self.conversations[addr]
            input_queue = qcv.input_msg_queue
            if input_queue.is_empty():
                continue
            while not input_queue.is_empty():
                addr_msgs.append((addr, input_queue.get_nowait()))
        return addr_msgs
            
    def send_msg(self, msg, to=None):
        """ Send message to one or more in the inputs socketserver
        by placing message in output queue(s)
        :msg: message to send converted to bytes if not SO
        :to: destination one or list of sockets, default: all 
        """
        if to is None:
            to = self.inputs
        if to is not list:
            to = [to]       # list of one
        for dest in to:
            qcv = self.conversatons[dest]
            qcv.output_msg_queue.put(msg)   # Add to output queue
            if dest not in self.outputs:
                self.outputs.append(dest)   # Add to output ready test
    
    def stop(self, force=False):
        """ Stop Running 
        :force: True - stop immediately
                default: False
        """
        self.exitFalg = 1
        if force:
            raise Exception     # TBD - softer stop
        
if __name__ == "__main__":
    import  time
    qbs = QueenBeeServer()
    qbs.run()
    SlTrace.lg("End of Test")    
        