# queen_bee_server_thread.py    03Nov2020  crs
"""
QueenBeeServer's thread
"""
import threading
import time
from select_trace import SlTrace
exitFlag = 0

class QueenBeeServerThread (threading.Thread):
    def __init__(self, run_proc):
        """ Setup queen bee processing
        :run_proc: process to do server work
        """
        threading.Thread.__init__(self)
        self.run_proc = run_proc
      
    def run(self):
        SlTrace.lg("Starting Queen Bee Server Thread Processing")
        self.run_proc()
        print ("Exiting Queen Bee Server Thread Processing")


if __name__ == "__main__":
    def rpt():
        global exitFlag
        count = 0
        max_count = 5
        while count < max_count:
            count += 1
            SlTrace.lg(f"...running {count}")
            time.sleep(1)
            
    qbt = QueenBeeServerThread(rpt)
    qbt.start()
    qbt.join()