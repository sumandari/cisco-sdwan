import argparse
import getpass
import json
import sys

import pandas as pd

from rest_api_lib import RestSdwan


class GetDataVmanage(RestSdwan):
    def __init__(self, 
                info_overview=["vdevice-host-name",
                                "vdevice-name"
                                "ifname",
                                "ip-address",
                                "if-oper-status",
                                "vpn-id",
                                "mtu",
                                "uptime",
                                "port-type",
                                "desc"], 
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
                if info == "ip-address":
                    data_overview[info] = deviceId
                else:
                    data_overview[info] = None
            
                list_data.append(data_overview)
            
            return list_data

        for data in response['data']:
            data_overview = dict()

            for info in info_overview:
                data_overview[info] = data[info] if info in data else None

            list_data.append(data_overview)

        return list_data

    def all_device_overview(self, devices = []):

        for device in devices:
            data = self.device_overview(device)
            self.dataframe = self.dataframe.append(data)
        
        return self.dataframe


def main():
    print('_' * 50 +'\n')

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

    username = args.Username
    vmanage = args.Vmanage
    password = getpass.getpass(f'Password {username}: ')
    
    obj = GetDataVmanage(vmanage_ip=vmanage, username=username, password=password)

    # custom or default attribute will be displayed
    if not args.q:
        data_attribute = None
    else:
        data_attribute = args.q

    if not args.d:
        # all deviceId
        if not data_attribute:
            allDeviceId = obj.all_device_id()
        else:
            allDeviceId = obj.all_device_id(info_overview=data_attribute)

        print(f"Retrieving data {len(allDeviceId)} deviceId in {vmanage}")

        all_device_overview = obj.all_device_overview(allDeviceId)
        print(all_device_overview)

    else:
        # certain deviceId
        print(f"Retrieving data from deviceId {args.d} in {vmanage}")

        df_deviceId = pd.DataFrame()
        data_deviceId = device_overview(args.d)
        df_deviceId = df_deviceId.append(data)
        
        print(df_deviceId)

    print('_' * 50 +'\n')

    


# def main(args):
#     if not len(sys.argv[1:]) == 2:
#         sys.exit(print('\nuse > python rest_api_lib.py <vmanage_ip:port> <username>'))

#     vmanage_ip, username= args[0], args[1]

#     password = getpass.getpass(f'Password {username}: ')

#     obj = GetDataVmanage(vmanage_ip, username, password)
    
#     allDeviceId = obj.all_device_id()
#     print(f"Retrieving data {len(allDeviceId)} deviceId...")
    
#     all_device_overview = obj.all_device_overview(allDeviceId)
#     print(all_device_overview)


if __name__ == "__main__":
    main()