import socket
import subprocess


s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
s.bind(("lo",0 ))


subprocess.call(['ip', 'link', 'set', 'dev', 'enp2s0', 'promisc', 'on'])


s.settimeout(None)
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)


while True:
    raw_data, addr = s.recvfrom(4096)


    dest, src, protocol = socket.ntohs(addr[0]), socket.ntohs(addr[1]), socket.ntohs(addr[2])


    print(f'\nDestination: {dest}\nSource: {src}\nProtocol: {protocol}')


    subprocess.call(['ip', 'link', 'set', 'dev', 'enp2s0', 'promisc', 'off'])


    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    s.close()
