import bpy
from ..settings import addon_name,portal_user_addons_url

class PORTAL_OT_restore_default(bpy.types.Operator):
    bl_idname = "portal.default"
    bl_label = "restore default"
    bl_description = "restore default settings"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.preferences.addons[addon_name].preferences.portal_ip = portal_user_addons_url
        return {"FINISHED"}



classes = [
    PORTAL_OT_restore_default,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)




def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)