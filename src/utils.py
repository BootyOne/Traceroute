import socket
from typing import NoReturn

import scapy.layers.inet
import scapy.layers.inet6
from cymruwhois import Client


def set_type(connection_type: str, udp, icmp):
    if connection_type == 'udp':
        return udp()
    elif connection_type == 'icmp':
        return icmp()
    else:
        return None


def rearrange(result):
    sorted_result = []

    for snd, rcv in result:
        sorted_result.append((snd.ttl, rcv.src, rcv.time))

    return sorted(sorted_result)


def conclusion(sorted_result):
    c = Client()
    ip = socket.gethostbyname('globalresearch.ca')
    asn = ''

    for i in sorted_result:
        for r in c.lookupmany([ip, i[1]]):
            asn = r.asn
        print(f'{i[0]:<5}  {i[1]:<16}  {i[2]:<12}  {asn:<60}')


def traceroute(time_out: int, port: int, number_requests: int, protocol_definition: bool, ip: str, connection_type: str) -> NoReturn:
    if ':' in ip:
        l4 = set_type(connection_type, scapy.layers.inet6.UDP, scapy.layers.inet6.ICMPv6RPL)
        result, u = scapy.layers.inet6.traceroute6(ip, port, maxttl=number_requests, timeout=time_out, l4=l4, verbose=False)
    else:
        l4 = set_type(connection_type, scapy.layers.inet.UDP, scapy.layers.inet.ICMP)
        result, u = scapy.layers.inet.traceroute(ip, port, maxttl=number_requests, timeout=time_out, l4=l4, verbose=False)

    sorted_result = rearrange(result)
    if protocol_definition:
        conclusion(sorted_result)
    else:
        for i in sorted_result:
            print(f'{i[0]:<5}  {i[1]:<16}  {i[2]:<12}')
