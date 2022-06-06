import argparse
import scapy.layers.inet6
import scapy.layers.inet
from cymruwhois import Client
import socket


def prepare_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='Тайм-аут ответа (по умолчанию 2 секунды)', type=int, default=2)
    parser.add_argument('-p', help='Порт', type=int, default=80)
    parser.add_argument('-n', help='Максимальное количество запросов', type=int, default=30)
    parser.add_argument('-v', help='Определение протокола приложения', default=False, action='store_true')
    parser.add_argument('ip', help='IP, чтобы проверить')
    parser.add_argument('type', help='Тип подключения')
    return parser


def set_type(args, udp, icmp):
    if args.type == 'udp':
        return udp()
    elif args.type == 'icmp':
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


def IPV6(args):
    l4 = set_type(args, scapy.layers.inet6.UDP, scapy.layers.inet6.ICMPv6RPL)
    result, u = scapy.layers.inet6.traceroute6(args.ip, args.p, maxttl=args.n, timeout=args.t, l4=l4, verbose=False)
    sorted_result = rearrange(result)
    if args.v:
        conclusion(sorted_result)
    else:
        for i in sorted_result:
            print(f'{i[0]:<5}  {i[1]:<16}  {i[2]:<12}')


def IPV4(args):
    l4 = set_type(args, scapy.layers.inet.UDP, scapy.layers.inet.ICMP)
    result, u = scapy.layers.inet.traceroute(args.ip, args.p, maxttl=args.n, timeout=args.t, l4=l4, verbose=False)
    sorted_result = rearrange(result)
    if args.v:
        conclusion(sorted_result)
    else:
        for i in sorted_result:
            print(f'{i[0]:<5}  {i[1]:<16}  {i[2]:<12}')


if __name__ == '__main__':
    parser = prepare_parser()
    args = parser.parse_args()
    if ':' in args.ip:
        IPV6(args)
    else:
        IPV4(args)
