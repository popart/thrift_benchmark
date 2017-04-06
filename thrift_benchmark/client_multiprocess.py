import sys
sys.path.append('gen-py')

import time
from multiprocessing import Pool

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

def worker(rps):
    client, transport = create_client()

    # Connect!
    transport.open()

    for s in xrange(5):
        start = time.time()

        for _ in xrange(rps):
            client.echo('hello world')

        elapsed = time.time() - start
        #if elapsed > 1:
            #return False

        if elapsed < 1:
            time.sleep(1 - elapsed)

    transport.close()
    return True

if __name__ == '__main__':

    for n in xrange(2,3):
        for rps in xrange(1000, 10000, 1000):
            # reset the server counts
            client, transport = create_client()
            transport.open()
            client.reset()

            #run some load tests
            pool = Pool(processes=n)
            ress = []
            for _ in xrange(n):
                ress.append(pool.apply_async(worker, (rps,)))

            pool.close()
            pool.join()

            # get the server counts
            cs = client.count()
            transport.close()

            if all(res.get() for res in ress):
                print "** PASS: clients: %d, rps: %d **" % (n, rps)
                print cs
            else:
                print '-- FAIL: clients: %d, rps: %d --' % (n, rps)
                print cs
                break

