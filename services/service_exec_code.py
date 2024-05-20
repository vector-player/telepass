import requests
import urllib
import urllib3
import json
import os


def urllib_req():
    url = "http://192.168.1.203:8000/shop_plus/ui_test"
    res = urllib.request.urlopen(url)
    code = res.read()
    print(code)
    exec(code)

def urllib3_req():
    url = "http://192.168.1.203:8000/shop_plus/ui_test"
    http = urllib3.PoolManager()
    response = http.request("GET", url)
    print("response status:",response.status) # Prints 200
    code = response.data.decode("utf-8")
    print(code)
    exec(code)

def get_code_from_db():
    url = "http://192.168.1.203:8000/shop_plus/code/1"
    http = urllib3.PoolManager()
    _res = http.request("GET", url)
    print("response status:",_res.status) # Prints 200
    _res = _res.data
    print("res :" + "\n",_res) ## err: can only concatenate str (not 'bytes')

    _res = _res.decode("utf-8")
    # _res = _res['code']
    print("res utf8:"+"\n" + _res)        
    # print(code.json()['data']['cityname']) 
    exec(_res)


def get_code_by_name(spu_pk, code_name):
    from .. import settings
    root_url = settings.portal_user_source_codes
    sub_url = f'{spu_pk}/{code_name}.json'
    url = os.path.join(root_url, sub_url)
    res = session_request(url)
    if len(res) == 0:
        print('No content.')
        return None
    dict = res[0]
    code = dict['code_content']
    return code



def session_request(url):    
    # sss = requests.Session() ## Don't create a new SessionObj, or else it maintains different session
    from .. import settings

    sss = settings.session_obj
    # print('session:',sss)
    my_headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip',
        'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
    }
    # http = urllib3.PoolManager()
    try:
        # res = http.request("GET", url)
        res = sss.get(url, headers = my_headers)
        print("market link response:+++++++++++++++++++++++++++++++++","\n",res)
        print('Response status code:',res.status_code)
        # print("Response headers:",res.headers)
        # print(res.body.decode('utf-8'))

        res = json.loads(res.text)

    except Exception as e:
        print(e)
        print("Can't handle json.loads: \n")
        return False
    print("Response:+++++++++++++++++++++++++++++++++","\n",res)
    # print('session:',res['session_id'])
    return res