import sys
sys.path.append('gen-py')

from multiprocessing import Process

from echo import Echo

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import timeit

if __name__ == '__main__':
    # Make socket
    transport = TSocket.TSocket('localhost', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = Echo.Client(protocol)

    # Connect!
    transport.open()

    def run():
        client.echo('hello world')

    for n in [1000, 10000, 100000]:
        start_time = timeit.default_timer()
        for _ in xrange(n):
            Process(target=run)
        elapsed_time = timeit.default_timer() - start_time
        print "elapsed: %s s for %s reqs" % (elapsed_time, n)

    transport.close()

