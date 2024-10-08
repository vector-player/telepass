import bpy
from .. import settings

class PORTAL_OT_open_active_addon(bpy.types.Operator):
    bl_idname = "portal.open_active_addon"
    bl_label = "Open"
    bl_description = "Open active addon"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, ctx):
        return True

    def execute(self, ctx):
        if ctx.scene.portal_tab == 'market':
            import webbrowser
            id = ctx.scene.portal_active_market_addon_id
            
            print('id:',id)
            if id == '':
                msg = 'Please select an item first.'
                self.report({'INFO'}, msg)
                print(msg)
                return {"FINISHED"}
            
            if not id in settings.portal_market_addons:
                msg = f"Error: check key value {id} exists."
                self.report({'INFO'}, msg)
                print(msg)
                return {"FINISHED"}
            
            sku = settings.portal_market_addons[id]
            if sku.status == 'test':                
                bpy.ops.tele.exec(ref='init')
                return {"FINISHED"}

            spu_id = sku.spu.id
            # url = f"http://192.168.1.203:8000/spu/{id}/"
            url = f"{settings.portal_spu}/{spu_id}/"
            webbrowser.open(url)
        if ctx.scene.portal_tab == 'my':
            # ctx.scene.portal_sku_user_previews = str(1)
            id = ctx.scene.portal_active_user_addon_id
            print('id:',id)
            if id == '':
                msg = 'Please select an item first.'
                self.report({'INFO'}, msg)
                print(msg)
                return {"FINISHED"}
            print(settings.portal_user_addons[id].spu.title)
            bpy.ops.tele.exec(ref='init')
        return {"FINISHED"}

classes = [
    PORTAL_OT_open_active_addon,
]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)