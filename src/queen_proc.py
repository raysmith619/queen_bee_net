# queen_proc.py    19Oct2020  crs, Author
"""
Testout queen bee Control
"""
import socket

class CmdInfo:
    def __init__(self, addr):
        self.addr = addr
        
class QueenProc:
    def __init__(self, sock=None):
        """ Setup processing
        :sock: socket to use
                default: create socket
        """
        self.cmd_info = {}
        if sock is None:
            family = socket.AF_INET
            sock_type = socket.SOCK_DGRAM
            sock = socket.socket(family, sock_type)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock = sock
        
    def cmd_send(self, cmd, addr):
        """ Send command to address
        :cmd: command
        :addr: destination
        """
        print(f"cmd_send: cmd:{cmd} addr:{addr}")
        data = bytes(cmd, "utf-8")
        self.sock.sendto(data, addr)
        
        
    def cmd_resend(self, cmd, addr):
        """ Resend cmd to all others
        :cmd: command from drone
        :addr: our address - don't send to us
        """
        for ad in self.cmd_info:
            if ad != addr:
                self.cmd_send(cmd, ad)
            else:
                self.cmd_send("==" + cmd, ad)     
    def cmd_proc(self, cmd, addr):
        """ process drone commands
        :cmd: command from drone
        :addr: drone Address
        """
        print(f"queen_proc: cmd:{cmd} addr:{addr}")
        if addr not in self.cmd_info:
            self.cmd_info[addr] = CmdInfo(addr)
        self.cmd_resend(cmd, addr)
    
    
    