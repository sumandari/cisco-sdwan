import argparse


# create the parser
my_parser = argparse.ArgumentParser(description='Use REST API SDWAN to retrieve data')

# add the arguments
my_parser.add_argument('Vmanage',
                        metavar='vmanage:port',
                        type=str,
                        help='vmanage ip address and port')
my_parser.add_argument('Username',
                        metavar='username',
                        type=str,
                        help='username login to vmanage')
my_parser.add_argument('-d',
                        action='store',
                        type=str,
                        help='deviceId IP address')
my_parser.add_argument('-q',
                        action='append',
                        type=str,
                        help='attribute data to be retrieve')

args = my_parser.parse_args()

print(vars(args))

if not args.d:
    print(f'get data all deviceId in {args.Vmanage}')
else:
    print(f'get data from deviceId: {args.d}')

if not args.q:
    print(f'data attribute: default')
else:
    print(f'data attribute: {args.q}')