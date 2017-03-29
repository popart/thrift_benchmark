import sys
sys.path.append('gen-py')

from echo import Echo

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class EchoHandler(object):
    def echo(self, s1):
        return s1

if __name__ == '__main__':
    handler = EchoHandler()
    processor = Echo.Processor(handler)
    transport = TSocket.TServerSocket(port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    print "starting server"
    server.serve()

    # You could do one of these for a multithreaded server
    # server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(...) <- seems to require some cleanup
    # right now, for serial test, threaded servers are slightly slower

