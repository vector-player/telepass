
import json  
import urllib.request  

def public_ip():

    url = "https://api.ipify.org/?format=json"  # this url is used to get public ip address
    try:
        response = urllib.request.urlopen(url)  # 
        data = response.read()  # get bytes data from response
        data = data.decode("utf-8")  # decode bytes to string
        data = json.loads(data)  # load string to json data
        public_ip = data["ip"]  # get public ip from json data
        print("My Public IP: ", public_ip)

    except:
        err_msg = "Can not get public internet."    
        print(err_msg)
        public_ip = ''

    return public_ip
