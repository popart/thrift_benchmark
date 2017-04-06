import sys
sys.path.append('gen-py')

from echo import Echo
from echo.ttypes import Packet

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
    print 'made a client'
    # Connect!
    transport.open()
    print 'opened'

    client.reset()

    client.echo('hello world')
    client.add(Packet(ride_id='ride_0', workout_id='workout_0', seconds_since_pedaling_start=10, total_work=5.0))

    cs = client.count()
    print sorted(cs.items())

    transport.close()

