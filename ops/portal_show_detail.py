from bpy.types import Operator
from bpy.props import StringProperty
from bpy.utils import register_class, unregister_class
from .. import settings
from ..services.service_subwindow import create_window
from ..services.service_image import parse_image_from_text, parse_image_from_text_re
from ..services.service_previews import load_image_list, load_image_dict

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


classes = [
    PORTAL_OT_show_detail
]

def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in classes:
        unregister_class(cls)