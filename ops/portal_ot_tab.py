import bpy
from ..services.service_previews import update_detail_preview

class PORTAL_OT_tab(bpy.types.Operator):
    bl_idname = "portal.tab"
    bl_label = "Portal Tab"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER"}

    select_tab : bpy.props.StringProperty()

    @classmethod
    def poll(cls, ctx):
        return True

    def execute(self, ctx):
        if self.select_tab == 'market':
            ctx.scene.portal_tab = 'market'
            ctx.scene.portal_active_addon_status = 'Subscribe'
            update_detail_preview(ctx)
        if self.select_tab == 'my':
            ctx.scene.portal_tab = 'my'
            ctx.scene.portal_active_addon_status = 'On/Off'
            update_detail_preview(ctx)
        return {"FINISHED"}



classes = [
    PORTAL_OT_tab
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)