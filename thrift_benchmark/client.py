import sys
sys.path.append('gen-py')

import time

from echo import Echo
from echo.ttypes import Packet

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def create_client():
    # Make socket
    transport = TSocket.TSocket('localhost', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = Echo.Client(protocol)

    return (client, transport)

if __name__ == '__main__':

    for rps in xrange(1000, 10000, 1000):
        client, transport = create_client()
        transport.open()

        # reset the server counts
        client.reset()

        #run some load tests
        success = True

        for s in xrange(5):
            start = time.time()

            for _ in xrange(rps):
                client.echo('hello world')

            elapsed = time.time() - start

            if elapsed < 1:
                time.sleep(1 - elapsed)
            else:
                success = False

        # get the server counts
        cs = client.count()
        transport.close()

        if success:
            print "** PASS: rps: %d **" % rps
        else:
            print '-- FAIL: rps: %d --' % rps
        print cs

