import bpy
from ..services.service_previews import update_detail_preview

class PORTAL_OT_tab(bpy.types.Operator):
    bl_idname = "portal.tab"
    bl_label = "Portal Tab"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER"}

    select_tab : bpy.props.StringProperty() # type:ignore

    @classmethod
    def poll(cls, ctx):
        return True

    def execute(self, ctx):
        from .. import settings
        if self.select_tab == 'market':
            ctx.scene.portal_tab = 'market'
            id = ctx.scene.portal_active_market_addon_id
            print("portal_ot_tab id from ctx.scene.portal_active_market_addon_id:", id)
            if id: 
                print(f"query id '{id}' in settings.portal_market_addons:",[addon for addon in settings.portal_market_addons])
                sku = settings.portal_market_addons[id]
                print("sku:",sku)
                if sku and sku.status == 'test': # and 'Addons' in sku.spu.category 
                    ctx.scene.portal_active_addon_status = 'On/Off'
            else:
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