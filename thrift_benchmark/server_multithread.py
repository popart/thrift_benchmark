import sys
sys.path.append('gen-py')

from collections import defaultdict
import time

from echo import Echo
from echo.ttypes import Packet

from thrift import Thrift
from thrift.transport import TSocket 
from thrift.transport import TTransport
from thrift.transport.TTransport import TFramedTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer



class EchoHandler(object):
    c = {}
    x = None

    def inc_count(self):
        t = int(time.time()) & 1023

        if t not in self.c:
            self.c[t] = 0

        self.c[t] += 1

    def echo(self, s):
        self.inc_count()
        return s

    def add(self, p):
        x = p.workout_id 
        self.inc_count()

    def count(self):
        return self.c

    def reset(self):
        self.c = {}
        return True

if __name__ == '__main__':
    handler = EchoHandler()
    processor = Echo.Processor(handler)
    transport = TSocket.TServerSocket(port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
    server.setNumThreads(4)
    print "starting server"
    try:
        server.serve()
    except (SystemExit, KeyboardInterrupt):
        server.stop()

    # You could do one of these for a multithreaded server
    # server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(...) <- seems to require some cleanup
    # right now, for serial test, threaded servers are slightly slower

