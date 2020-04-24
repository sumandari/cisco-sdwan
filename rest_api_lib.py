# https://sdwan-docs.cisco.com/Product_Documentation/Command_Reference/Command_Reference/vManage_REST_APIs/vManage_REST_APIs_Overview/Using_the_vManage_REST_APIs
"""
Class with REST Api GET and POST libraries

Example: python rest_api_lib.py vmanage_hostname username password

PARAMETERS:
    vmanage_hostname : Ip address of the vmanage or the dns name of the vmanage
    username : Username to login the vmanage
    password : Password to login the vmanage

Note: All the three arguments are manadatory
"""
import requests
import sys

from requests.exceptions import HTTPError
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# disable unverified HTTPS
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RestSdwan:
    def __init__(self, vmanage_ip, username, password):
        self.vmanage_ip = vmanage_ip
        self.session = dict()
        self.username = username
        self.password = password
        self.login()

    def login(self):
        """Login to vmanage and establish"""
        base_url_str = f"https://{self.vmanage_ip}"
        login_action = '/j_security_check'

        #Format data for loginForm
        login_data = {'j_username' : self.username, 'j_password' : self.password}

        #Url for posting login data
        login_url = base_url_str + login_action

        # establish session
        sess = requests.session()

        #If the vmanage has a certificate signed by a trusted authority change verify to True
        try:
            login_response = sess.post(url=login_url, data=login_data, verify=False)
        except HTTPError as http_err:
            sys.exit(print(f'HTTP error occurred: {http_err}'))
        except Exception as err:
            sys.exit(print(f'Other error occurred: {err}'))

        if b'<html>' in login_response.content:
            print(f"{login_url} --> Login Failed")
            sys.exit(0)

        self.session[self.vmanage_ip] = sess
        print(f'{login_url} --> Login Succeed!')

    def get_request(self, mount_point, return_type='content'):
        """
        GET request
        
        :return: data response
        :return type:
        - content : byte
        - text : string
        - json : dict
        """
        url = f"https://{self.vmanage_ip}/dataservice{mount_point}"
        try:
            response = self.session[self.vmanage_ip].get(url, verify=False)
        except HTTPError as http_err:
            sys.exit(print(f'HTTP error occurred: {http_err}'))
        except Exception as err:
            sys.exit(print(f'Other error occurred: {err}'))

        if return_type == 'text':
            response.encoding = 'utf-8'
            data = response.text
        elif return_type == 'json':
            data = response.json()
        else:
            data = response.content
        return data

    def post_request(self, mount_point, payload, headers={'Content-Type': 'application/json'}):
        """POST request"""
        url = f"https://{self.vmanage_ip}/dataservice{mount_point}"
        payload = json.dumps(payload)
        print("trying post data: {payload}")
        
        try:
            response = self.session[self.vmanage_ip].post(url=url, data=payload, headers=headers, verify=False)
        except HTTPError as http_err:
            sys.exit(print(f'HTTP error occurred: {http_err}'))
        except Exception as err:
            sys.exit(print(f'Other error occurred: {err}'))

        data = response.content
        return data
        

def main(args):
    if not len(args) == 4:
        print('\nuse > python rest_api_lib.py <vmaanage_ip:port> <username> <password> </get_api_path>')
        return
    vmanage_ip, username, password, get_path = args[0], args[1], args[2], args[3]
    obj = RestSdwan(vmanage_ip, username, password)
    
    #Example request to get devices from the vmanage "url=https://vmanage.viptela.com/dataservice/device"
    response = obj.get_request(get_path)
    from pprint import pprint
    pprint(response)
    # #Example request to make a Post call to the vmanage "url=https://vmanage.viptela.com/dataservice/device/action/rediscover"
    # payload = {"action":"rediscover","devices":[{"deviceIP":"172.16.248.105"},{"deviceIP":"172.16.248.106"}]}
    # response = obj.post_request('device/action/rediscover', payload)
    # print response

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))