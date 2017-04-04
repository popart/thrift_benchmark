import sys
sys.path.append('gen-py')

from multiprocessing import Pool

from echo import Echo
from echo.ttypes import Packet

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import timeit

def worker(n):
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

    client.reset()

    for _ in xrange(n):
        client.add(Packet(
            ride_id='ride_0', 
            workout_id='workout_0', 
            seconds_since_pedaling_start=10,
            total_work=5.5))


    cs = client.count()

    transport.close()
    return max(cs.values())

if __name__ == '__main__':

    for n in xrange(1,4):
        pool = Pool(processes=n)
        ress = []
        for i in xrange(n):
            ress.append(pool.apply_async(worker, (50000,)))

        pool.close()
        pool.join()

        print "clients: %d" % n
        for res in ress:
            print res.get()

