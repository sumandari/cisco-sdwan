# CISCO SDWAN - Get interface status from Vmanage
You can get attribute from all deviceIds in your Vmanage either prefer to retrieve data from a deviceId

## Prerequisites
* python3

## Installing
* download source code or do git clone
```
git clone https://github.com/sumandari/cisco-sdwan.git
```
* create virtual environment
```
python3 -m venv venv
```
* activate virtual env
  * macOS
  ```
  . venv/bin/Activate
  ```
  * windows
  ```
  venv\Scripts\Activate
  ```
* install package
  ```
  pip install -r requirements.txt
  ```
 
 ## Usage
 ```
 python sdwan.py -h
 ```
 
 ```
 python sdwan.py status vmanage:port username [option]
 ```
 ![all deciveid](/images/status.png)

```
 python sdwan.py topology vmanage:port username
 ```
 ![all deciveid](/images/topo.png)

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
