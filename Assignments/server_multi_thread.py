import socket
import struct
import threading, time
import sys

multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# allow multiple server/receiver processes on the same computer to bind to the multicast port
#
# IMPORTANT
#
# Windows does not support SO_REUSEPORT, so we need to use REUSEADDR
#
# Linux/MacOS: need to use REUSEPORT
#
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


# Receive/respond loop
while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)

    print('received %s bytes from %s' % (len(data), address))
    print(data.decode())

    print('sending acknowledgement to', address)
    sock.sendto('ack'.encode(), address)