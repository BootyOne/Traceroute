from arg_parser import prepare_parser
from utils import traceroute


def main():
    parser = prepare_parser()
    args = parser.parse_args()

    traceroute(args.t, args.p, args.n, args.v, args.ip, args.type)


if __name__ == '__main__':
    main()
