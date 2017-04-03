import sys
sys.path.append('gen-py')

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

    for n in [1000, 10000, 100000]:
        client.reset()

        for _ in xrange(n):
            client.noop()

        print "n: %s " % n

        cs = client.count()
        print sorted(cs.items())

    transport.close()

