import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s【%(levelname)s】(%(name)s-No.%(lineno)d):%(funcName)s -> %(message)s")
logger = logging.getLogger(__name__)
# logger.setLevel(level = logging.INFO)
import threading
import multiprocessing
from multiprocessing import current_process
# logger.debug("portal_ot_show_detail.Ln.8:current_process().name:{}".format(current_process().name))
from bpy.types import Operator, Scene
from bpy.props import StringProperty, BoolProperty
from bpy.utils import register_class, unregister_class
from .. import settings
from ..services.service_subwindow import create_window
from ..services.service_image import parse_image_from_text, parse_image_from_text_re
from ..services.service_previews import load_image_list, load_image_dict
from ..services.service_pywebview import display_html_string, new_process_display, new_thread_display,  new_thread_with_js
from ..views.preferences import check_installed
from ..views.msgbox import msgbox





class PORTAL_OT_show_detail(Operator):
    bl_idname = "portal.show_detail"
    bl_label = "Detail"
    bl_description = "Show detail info about selected item"
    bl_options = {"REGISTER"}

    string : StringProperty

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, ctx):
        ## handle text

        try:
            if check_installed('webview'):
                
                # display_html_string(self.string)
                # new_process_display(self.string)
                # new_thread_display(self.string)
                # new_thread_with_js(self.string)
                self.threads_handler(ctx, header='', on_top=True,)

                
                

                # t = threading.Thread(target=self.webview) # args=()
                # t.start()

                # p = multiprocessing.Process(target=display_html_string, args=(self.string, ))
                # p.daemon = True
                # p.start()                
                # p.join()
                
            else:
                msg = "For better experience, install pywebview in addon's preferences panel."
                msgbox(msg)
                create_window('TEXT_EDITOR', 640, 480, string=self.string)  
        except Exception as e:
            msg = f"webview error:{e}."
            print(msg)
            self.report({'INFO'}, msg)   
            msgbox(msg)         
            create_window('TEXT_EDITOR', 640, 480, string=self.string) 

        return {"FINISHED"}
    
    def invoke(self, ctx, event):
        try:

            if ctx.scene.portal_tab == 'market':
                id = ctx.scene.portal_active_market_addon_id
                # print("total market addons:", len(settings.portal_market_addons))
                self.string = settings.portal_market_addons[id].spu.content
            if ctx.scene.portal_tab == 'my':
                id = ctx.scene.portal_active_user_addon_id
                self.string = settings.portal_user_addons[id].spu.content       
            
        except Exception as e:
            print("Error:cannot get addons data.")
            print(e)
            return {"FINISHED"}
        return self.execute(ctx)
    ## Use Case: skip invoke for custom arguments:
    # bpy.ops.wm.mouse_position('EXEC_DEFAULT', x=20, y=66)

    


    # def webview(self):
    #     # display_html_string(self.string)
    #     try:
    #         display_html_string(self.string)
    #     except Exception as e:
    #         msg = f"webview error:{e}."
    #         print(msg)
    #         self.report({'INFO'}, msg)


    def threads_handler(self, ctx, header:str='', on_top:bool=True):
        threads = threading.enumerate()
        threads_count = 0
        has_pywebview = False
        for thread in threads:
            threads_count += 1
            print(f"\nthread {threads_count} name:", thread.name)

        logger.debug("{}: threads count:{}".format(__class__.__name__, threads_count))

        if not ctx.scene.pywebview_flag:            
            logger.debug("{}: Use MainThread for webview.".format(__class__.__name__))
            display_html_string(self.string, header=header, on_top=on_top)
            ctx.scene.pywebview_flag = True          
                               
        else:
            ## enable multi-threading for not blocking main-thread
            logger.debug("{}: Create new thread for webview.".format(__class__.__name__))
            new_thread_display(self.string, header=header, on_top=on_top) 


classes = [
    PORTAL_OT_show_detail
]

def register():
    for cls in classes:
        register_class(cls)
    
    Scene.pywebview_flag = BoolProperty(default=False)


def unregister():
    for cls in classes:
        unregister_class(cls)
    
    del Scene.pywebview_flag