import bpy
import json
import urllib3
from .. import settings
from .._types.sku_spu import SKU_SPU_Serializer
from ..services.service_previews import load_previews_market_sku

class PORTAL_OT_guest(bpy.types.Operator):
    bl_idname = "portal.guest"
    bl_label = "Guest"
    bl_description = "Guest Request to visit market"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, ctx):
        return True

    def session_request(self, ctx, url):    
        # sss = requests.Session() ## Don't create a new SessionObj, or else it maintain different session
        sss = settings.session_obj
        print('session:',sss)
        my_headers = {
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip',
            'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
        }
        http = urllib3.PoolManager()
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
        print("market link response:+++++++++++++++++++++++++++++++++","\n",res)
        # print('session:',res['session_id'])
        return res


    def execute(self, ctx):

        ## Try market:++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        print("Start MARKET request:")
        try:      
            # api_market_sku_spus = self.csrf_login(ctx, settings.portal_market_addons_url)
            api_market_sku_spus = self.session_request(ctx, settings.portal_market_addons_url)
        except Exception as e:
            msg = 'Login Failed. Check market connection.'
            print(msg)
            self.report({'INFO'}, msg)
            print(e)
            return {"FINISHED"}

        if not api_market_sku_spus:
            msg = 'Market response is None. Check market connection.'
            print(msg)
            self.report({'INFO'}, msg)
            return {"FINISHED"}
        # code_names = self.parse_purchased_codenames(spus)
        # ctx.scene.user_addon_names = self.parse_user_spus(spus, 'title')        
        settings.portal_market_addons = SKU_SPU_Serializer(api_market_sku_spus)
        print("LOGIN INFO:portal_market_addons found:",len(settings.portal_market_addons))
        load_previews_market_sku(ctx.scene.portal_sku_market_previews, ctx)
        return {"FINISHED"}


classes = [
    PORTAL_OT_guest,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)