import getpass
import json
import sys

import pandas as pd

from rest_api_lib import RestSdwan


class GetDataVmanage(RestSdwan):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pd.set_option('display.max_rows', None)
        self.dataframe = pd.DataFrame()
        self.default_info_overview = [
            "vdevice-host-name",
            "vdevice-name"
            "ifname", 
            "ip-address", 
            "if-oper-status", 
            "vpn-id", 
            "mtu", 
            "uptime", 
            "port-type", 
            "desc"
        ]

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

    def device_overview(self, deviceId, info_overview=self.default_info_overview):
        """
        get data from deviceid
        """
        url = f'/device/interface?deviceId={deviceId}'
        response = self.get_request(url, 'json')

        # prepare container
        list_data = list()

        # if deviceId doesn't have attribute 'data'
        if not "data" in response:
            data_overview = dict()

            for info in info_overview:
                if info == "ip-address":
                    data_overview = deviceId
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


def main(args):
    if not len(sys.argv[1:]) == 2:
        sys.exit(print('\nuse > python rest_api_lib.py <vmanage_ip:port> <username>'))

    vmanage_ip, username= args[0], args[1]

    password = getpass.getpass(f'Password {username}: ')

    obj = GetDataVmanage(vmanage_ip, username, password)
    
    allDeviceId = obj.all_device_id()
    print(f"Retrieving data {len(allDeviceId)} deviceId...")
    
    all_device_overview = obj.all_device_overview(allDeviceId)
    print(all_device_overview)


if __name__ == "__main__":
    main(sys.argv[1:])