import requests
import urllib
import urllib3
import json
import os
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s【%(levelname)s】(%(name)s-No.%(lineno)d):%(funcName)s -> %(message)s")
logger = logging.getLogger(__name__)



def urllib_req():
    url = "http://192.168.1.203:8000/shop_plus/ui_test"
    res = urllib.request.urlopen(url)
    code = res.read()
    logger.debug("code={}".format(code))
    exec(code)

def urllib3_req():
    url = "http://192.168.1.203:8000/shop_plus/ui_test"
    http = urllib3.PoolManager()
    response = http.request("GET", url)    
    logger.debug("response status:{}".format(response.status))
    code = response.data.decode("utf-8")
    print(code)
    exec(code)

def get_code_from_db():
    url = "http://192.168.1.203:8000/shop_plus/code/1"
    http = urllib3.PoolManager()
    _res = http.request("GET", url)
    logger.debug("response status:{}".format(_res.status))
    _res = _res.data
    logger.debug("res:\n{}".format(_res)) ## err: can only concatenate str (not 'bytes')

    _res = _res.decode("utf-8")
    # _res = _res['code']
    logger.debug("res utf8:\n{}".format(_res))      
    # print(code.json()['data']['cityname']) 
    exec(_res)


def get_code_by_name(spu_pk, code_name):
    from .. import settings
    
    try:
        user_api_root_url = settings.portal_user_source_codes
        sub_url = f'{spu_pk}/{code_name}.json'
        user_api = os.path.join(user_api_root_url, sub_url)
        user_api_res = session_request(user_api)
        logger.debug("【serice_exec_code】 res from user API:{}".format(user_api_res))

        test_api_root_url = settings.portal_test_source_codes
        sub_url = f'{spu_pk}/{code_name}.json'
        test_api = os.path.join(test_api_root_url, sub_url)
        test_api_res = session_request(test_api)
        logger.debug("【serice_exec_code】 res from test API:{}".format(test_api_res))
        

        # if len(user_api_res) == 0:
        user_api_status_code = user_api_res.status_code if hasattr(user_api_res, "status_code") else None
        if user_api_status_code == 200:
            dict = json.loads(user_api_res.text)

        else:
            logger.debug("User API error with code:'{}',now try market-test API...".format(user_api_status_code))

            test_api_status_code = test_api_res.status_code if hasattr(test_api_res, "status_code") else None
            if test_api_status_code == 200:
                dict = json.loads(test_api_res.text)
                # print(test_api_res.text)
            else:
                logger.debug("Market-test API error with code:{}".format(test_api_status_code))
                res = {
                    "user_api_status_code":user_api_status_code,                    
                    "test_api_status_code":test_api_status_code,
                    "user_api_res": user_api_res,
                    "test_api_res": test_api_res,
                    "exception": None,
                    "has_error": True,
                    "code": None
                }
                return res
    
        if len(dict) == 0:
            logger.info("No code to execute.")
            res = {
                "user_api_status_code":user_api_status_code,
                "test_api_status_code":test_api_status_code,
                "user_api_res": user_api_res,
                "test_api_res": test_api_res,
                "exception": None,
                "has_error": False,
                "code": None
            }
            return res
        else:
            dict = dict[0]
            code = dict['code_content']
            res = {
                "user_api_status_code":user_api_status_code,
                "test_api_status_code":test_api_status_code,
                "exception": None,
                "has_error": False,
                "code": code
            }
            return res
    except Exception as e:
        logger.debug("Exception:{}".format(e))
        res = {
            "user_api_status_code":"unknown",
            "test_api_status_code":"unknown",
            "user_api_res": "unknown",
            "test_api_res": "unknown",
            "exception": e,
            "has_error": True,
            "code": None,
        }



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
        logger.debug("market link response:+++++++++++++++++++++++++++++++++\n{}".format(res))
        logger.debug("Response status code:{}".format(res.status_code))
        # print("Response headers:",res.headers)
        # print(res.body.decode('utf-8'))

        # res = json.loads(res.text)

    except Exception as e:
        logger.debug("Exception:{}".format(e))
        return e
    logger.debug("Response:+++++++++++++++++++++++++++++++++\n{}".format(res))
    # print('session:',res['session_id'])
    return res