import bpy
import json
import threading
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s【%(levelname)s】(%(name)s-No.%(lineno)d):%(funcName)s -> %(message)s")
logger = logging.getLogger(__name__)

from .. import settings
from .. settings import (
    ## Only for Readonly variables. 
    ## without DIR, a new local variable detach from origin would be created.
    # portal_user_addons,   
    # portal_user_addons_url, 
    # portal_market_addons, 
    # portal_market_addons_url, 
    # session_obj,
    addon_name,
)
from .._types.sku_spu import SKU_SPU_Serializer
from ..services.service_previews import load_previews_market_sku, load_previews_user_sku


class PORTAL_OT_login(bpy.types.Operator):
    bl_idname = "portal.login"
    bl_label = "Login"
    bl_description = "User request to login"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, ctx):
        return True

    # def slave_connect(self):
    #     from ..services.service_rpyc import rpyc_tool
    #     rpyc_tool.call_mission('mission-1')


    def execute(self, ctx):
        # HTTP Request
        # self.urllib_req()
        # self.urllib3_req()
        # self.get_code_form_db()  
        
        ## Start Portal Rig:
        # t1 = threading.Thread(target=self.slave_connect)
        # t1.start()

        ## Change Slave-server mode to Slave-client mode
        # from ..services.service_rpyc import rpyc_tool
        ## New python thread
        # rpyc_tool.call_mission(rpyc_tool, 'mission-1')
        ## 
        # rpyc_tool.slave_connect('mission-1')

        ## Wrap into an operator
        # bpy.ops.portal.rig(ref='mission-1')

        ## Try User request
        logger.debug("Start USER request:")
        
        # url = ctx.preferences.addons[addon_name].preferences.portal_ip
        # api_user_sku_spus = self.csrf_login(ctx, url)
        
        try: 
            url = ctx.preferences.addons[addon_name].preferences.portal_ip
            res = self.csrf_login(ctx, url)
            msg = f"Connection status:{res.status_code}"
            logger.debug("{}".format(msg))
            self.report({'INFO'}, msg)
            
            if res.status_code == 200:
                msg = "Connect successfully."
                logger.debug("{}".format(msg))
                self.report({'INFO'}, msg)

            api_user_sku_spus = json.loads(res.text)
            msg = f"response from api_user_sku_spus:{api_user_sku_spus}"
            logger.debug("{}".format(msg))
            self.report({'INFO'}, msg)

            if api_user_sku_spus == False:
                msg = 'Login Failed. Check Username and Password.'
                logger.debug("{}".format(msg))
                self.report({'INFO'}, msg)
                ## put an empty list to clear UI Previews
                SKU_SPU_Serializer([])
                load_previews_user_sku(self,ctx)
                return {"FINISHED"}
            if not api_user_sku_spus:
                msg = 'Response is None. Go to market and see what you would like.'
                logger.debug("{}".format(msg))
                self.report({'INFO'}, msg)
                return {"FINISHED"}

            
        except Exception as e:
            msg = 'Login Failed. Check user connection.'
            logger.debug("{}".format(msg))
            self.report({'INFO'}, msg)
            logger.debug("{}".format(e))
            return {"FINISHED"}

        # code_names = self.parse_purchased_codenames(spus)
        # ctx.scene.user_addon_names = self.parse_user_spus(spus, 'title')
        settings.portal_user_addons = SKU_SPU_Serializer(api_user_sku_spus)
        logger.debug("LOGIN INFO: portal_user_addons:{}".format(len(settings.portal_user_addons)))
        load_previews_user_sku(self, ctx)
        # ctx.scene.portal_sku_user_previews = str(0) ## active enum_items(1)

        ## Try Guest request
        # bpy.ops.portal.guest()
        return {"FINISHED"}



    def csrf_login(self, ctx, url):

    #登录源码：
    # def login(login_url = 'http://****.com/users/sign_in', username, password):
        
        
        #请求头
        # url = "http://192.168.1.203:8000/api-auth/login/"
        # ctx.preferences.addons[addon_name].preferences.portal_username = 'admin'
        # ctx.preferences.addons[addon_name].preferences.portal_password = '1234.abc'

        my_headers = {
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip',
            'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
        }
    
        #获取token
        # sss = requests.Session()
        sss = settings.session_obj
        logger.debug("session:{}".format(sss))
        
        try:
            # res = sss.get(url, headers = my_headers)
            res = sss.get(url)
            string = str(res.content, 'utf-8')
        except Exception as e:
            logger.debug("Connect Failed.")
            logger.debug("{}".format(e))
            return
        logger.debug("Session GET res.content string:{}".format(string))
        reg = r'<input type="hidden" name="csrfmiddlewaretoken" value="(.*)">'
        import re
        # pattern = re.compile(reg)
        # # result = pattern.findall(r.content) 
        # result = pattern.findall(string)

        result = re.findall(reg, string)

        token = result[0]
        logger.debug("csrf token:{}".format(token))
        #postdata
        my_data = {
            'commit' : '登录',
            'utf8' : '%E2%9C%93',
            # 'authenticity_token' : token,
            'csrfmiddlewaretoken' : token,
            # 'user[username]': username,
            'username': ctx.preferences.addons[addon_name].preferences.portal_username,
            # 'user[password]':password
            'password': ctx.preferences.addons[addon_name].preferences.portal_password,
        }
        
        #登录后
        # print("username:",ctx.preferences.addons[addon_name].preferences.portal_username)
        # print("password:",ctx.preferences.addons[addon_name].preferences.portal_password)
        try:
            res = sss.post(url, headers = my_headers, data = my_data)
            logger.debug("csrf POST response:+++++++++++++++++++++++++++++++++\n{}:".format(res))
            
            # print(res.data.decode('utf-8'))
            # 1. response.status_code
            # 2. response.text
            # 3. response.content
            # 4. response.encoding
            # 5. response.apparent_encoding
            # 6. response.headers
        
            # print('session:',sss)            
            # res = json.dumps(res.text)
            # res = json.dumps(res.text.encode('utf-8'))
            # res = res.body
            # res = res.content
            # res.encoding="utf-8"
            # res = res.content.decode('utf-8')

        #     dict = json.loads(res.text)
        except Exception as e:
            logger.debug("{}".format(e))
            logger.debug("Can't handle json.loads: \n{}".format(res.text))
            return False
        # print("csrf POST response to dict:+++++++++++++++++++++++++++++++++","\n",dict)
        # print('session:',res['session_id'])
        return res




    def parse_purchased_codenames(self,spus):
        spu_ids = []
        spu_code_names = []
        for spu in spus:
            for id in spu['id']:
                spu_ids.append(id)
            for codename in spu['source_codes']:
                spu_code_names.append(codename) 
        logger.debug("purchased id:{}".format([id for id in spu_ids]))
        logger.debug("code_names:{}".format([c for c in spu_code_names]))
        return spu_ids
        # return spu_code_names


    def parse_user_spus(self, spus, dict_key:str):
        values = []
        for spu in spus:
            for value in spu[f'{dict_key}']:
                values.append(value)
        logger.debug("{}:{}".format(dict_key, [v for v in values]))
        return values


classes = [
    PORTAL_OT_login,
]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)