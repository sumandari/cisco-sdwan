import argparse
import getpass
import json
import re
import sys

from pprint import pprint

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from rest_api_lib import RestSdwan


class GetDataVmanage(RestSdwan):
    def __init__(self, 
                info_overview=["vdevice-host-name",
                                "vdevice-name",
                                "ifname",
                                "ip-address",
                                "if-oper-status",
                                "vpn-id",
                                "mtu",
                                "uptime",
                                "port-type",
                                "description"], 
                *args,
                **kwargs):
        super().__init__(*args, **kwargs)
        pd.set_option('display.max_rows', None)
        self.dataframe = pd.DataFrame()
        self.info_overview = info_overview

    def all_device_id(self):
        """
        get all device id from vmanage

        :return:
        list of deviceId

        :return type:
        list
        """
        response = self.get_request('/device', 'json')

        id_devices = list()
        for data in response['data']:
            id_devices.append(data['deviceId'])

        return id_devices

    def device_overview(self, deviceId):
        """
        get data from deviceid
        """
        info_overview = self.info_overview

        url = f'/device/interface?deviceId={deviceId}'
        response = self.get_request(url, 'json')

        # prepare container
        list_data = list()

        # if deviceId doesn't have attribute 'data'
        if not "data" in response:
            data_overview = dict()

            for info in info_overview:
                data_overview[info] = deviceId if info == "vdevice-name" else None

            list_data.append(data_overview)

            return list_data

        for data in response['data']:
            data_overview = dict()

            for info in info_overview:
                data_overview[info] = data[info] if info in data else None

            list_data.append(data_overview)

        return list_data

    def all_device_overview(self, devices=[]):
        for device in devices:
            data = self.device_overview(device)
            self.dataframe = self.dataframe.append(data)

        return self.dataframe


class GetTopology(RestSdwan):
    """
    Get topology from BSD session
    """

    def __init__(self, *args, **kwargs):
        """
        call init function from class RestSdwan
        include invoke login()
        """
        super().__init__(*args, **kwargs)

    def all_device_id(self):
        """
        get all device id from vmanage

        :return:
        list of deviceId

        :return type:
        list
        """
        response = self.get_request('/device', 'json')

        id_devices = list()
        for data in response['data']:
            id_devices.append(data['deviceId'])

        return id_devices

    def datakey_bsd_session_deviceId(self, deviceId):
        """
        get bsd session, attribute: vdevice-datakey
        return list of tuple
        """
        url = f'/device/bfd/sessions?deviceId={deviceId}'
        response = self.get_request(url, 'json')

        regex = r'vdevice-dataKey": "([0-9.]+-[\w]+)-([0-9.]+-[\w]+)-[\w]+"'
        tuples = re.findall(regex, json.dumps(response))

        return tuples

    def datakey_bsd_session_all(self):
        """
        get bsd session in all deviceId

        """
        deviceId = self.all_device_id()
        print('deviceId: ', end='')
        pprint(deviceId)

        tuple_data = list()
        for device in deviceId:
            tunnel = self.datakey_bsd_session_deviceId(device)
            tuple_data.append(tunnel)

        tunnels = list()
        df = pd.DataFrame()
        for data in tuple_data:
            for d in data:
                if not d in tunnels:
                    swap_d = (d[1], d[0])
                    if not swap_d in tunnels:
                        tunnels.append(d)
                        df = df.append({'from': d[0], 'to': d[1]}, ignore_index=True)

        return df


class MyParser(argparse.ArgumentParser):
    """
    overwrite error message
    """

    def error(self, err):
        sys.stderr.write(f'error: {err}\n')
        self.print_help()
        sys.exit(1)


def parser():
    # create the parser
    my_parser = MyParser(description='Use REST API SDWAN to retrieve data')
    subparser = my_parser.add_subparsers(dest='command')
    subparser.required = True

    status_interface = subparser.add_parser('status',
                                    description='Get interace status table')

    # add the arguments in subparser status_interface
    status_interface.add_argument('Vmanage',
                            metavar='vmanage:port',
                            type=str,
                            help='vmanage ip address and port')
    status_interface.add_argument('Username',
                            metavar='username',
                            type=str,
                            help='username login to vmanage')
    status_interface.add_argument('-a',
                            action='store_true',
                            help='show all deviceId')
    status_interface.add_argument('-d',
                            action='store',
                            type=str,
                            help='deviceId IP address')
    status_interface.add_argument('-q',
                            action='append',
                            type=str,
                            help='attribute data to be retrieve')

    topology = subparser.add_parser('topology',
                                    description='Get topology graph')
    # add the arguments in subparser status_interface
    topology.add_argument('Vmanage',
                            metavar='vmanage:port',
                            type=str,
                            help='vmanage ip address and port')
    topology.add_argument('Username',
                            metavar='username',
                            type=str,
                            help='username login to vmanage')
    return my_parser.parse_args()


def main():
    print('_' * 50 + '\n')
    
    args = parser()
   
    username = args.Username
    vmanage = args.Vmanage
    password = getpass.getpass(f'Password {username}: ')


    # run topology parser
    if args.command == 'topology':
        print('preparing topology data...')
        obj = GetTopology(vmanage_ip=vmanage, username=username, password=password)
        topo = obj.datakey_bsd_session_all()
        print('Network topology: ')
        pprint(topo)
        G = nx.from_pandas_edgelist(topo, 'from', 'to')
        nx.draw(G, with_labels=True)
        plt.show()
        sys.exit(0)

    elif args.command == 'status':
        # custom or default attribute will be displayed
        if not args.q:
            data_attribute = None
            obj = GetDataVmanage(vmanage_ip=vmanage, username=username, password=password)
        else:
            data_attribute = args.q
            obj = GetDataVmanage(vmanage_ip=vmanage, username=username, password=password, 
                                info_overview=data_attribute)

        if args.a:
            allDeviceId = obj.all_device_id()
            print("all deviceId : ")
            for device in allDeviceId:
                print(device, end="\n")
            sys.exit()

        if not args.d:
            # all deviceId
            allDeviceId = obj.all_device_id()
            print(f"Retrieving data {len(allDeviceId)} deviceId in {vmanage}")

            all_device_overview = obj.all_device_overview(allDeviceId)
            print(all_device_overview)

        else:
            # certain deviceId
            print(f"Retrieving data from deviceId {args.d} in {vmanage}")

            df_deviceId = pd.DataFrame()
            data_deviceId = obj.device_overview(args.d)
            df_deviceId = df_deviceId.append(data_deviceId)
            
            print(df_deviceId)

    print('_' * 50 +'\n')


if __name__ == "__main__":
    main()