import argparse
import sys

def get_topology():
    print('this is a topology function')

def main():
    # create the parser
    my_parser = argparse.ArgumentParser(description='Use REST API SDWAN to retrieve data')
    subparser = my_parser.add_subparsers(dest='command')

    status_interface = subparser.add_parser('status')

    # add the arguments
    status_interface.add_argument('Vmanage',
                            metavar='vmanage:port',
                            type=str,
                            help='vmanage ip address and port')
    status_interface.add_argument('Username',
                            metavar='username',
                            type=str,
                            help='username login to vmanage')
    status_interface.add_argument('-d',
                            action='store',
                            type=str,
                            help='deviceId IP address')
    status_interface.add_argument('-q',
                            action='append',
                            type=str,
                            help='attribute data to be retrieve')

    topology = subparser.add_parser('topology')
    # topology.set_defaults(func=get_topology)

    topology.add_argument('Vmanage',
                            metavar='vmanage:port',
                            type=str,
                            help='vmanage ip address and port')
    topology.add_argument('Username',
                            metavar='username',
                            type=str,
                            help='username login to vmanage')

    args = my_parser.parse_args() 

    print(vars(args))

    if args.command =='topology':
        print ('hai this is topology')
        sys.exit()

    if args.command == 'status':
        print('ini status')
        sys.exit()

    # if not args.d:
    #     print(f'get data all deviceId in {args.Vmanage}')
    # else:
    #     print(f'get data from deviceId: {args.d}')

    # if not args.q:
    #     print(f'data attribute: default')
    # else:
    #     print(f'data attribute: {args.q}')


if __name__ == "__main__":
    main()