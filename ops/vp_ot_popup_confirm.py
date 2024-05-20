import bpy
from ..services.service_previews import load_previews_market_sku, load_previews_user_sku, pcoll_from_local

class VP_OT_popup_confirm(bpy.types.Operator):
    """Really?"""
    bl_idname = "vp.popup_confirm"
    bl_label = "Show How"
    bl_options = {'REGISTER', 'INTERNAL'}

    prop1: bpy.props.BoolProperty()
    prop2: bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({'INFO'}, "YES!")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        # layout.scale_x = 5
        # layout.scale_y = 10
        # row = layout.row()
        # row.prop(self, "prop1", text="Property A")
        # row = layout.row()
        # row.prop(self, "prop2", text="Property B")
        
        box = layout.box()
        box.scale_x = 2
        box.scale_y = 3
        row = box.row()
        img = row.template_preview(
            bpy.data.textures["LOGO_PORTAL"],
            show_buttons=True,
        )
        
        # row.template_image_layers(bpy.data.images["LOGO_PORTAL.png"],bpy.data.textures[0].image_user)
        # row.template_image(bpy.data, 'images["LOGO_PORTAL.png"]',bpy.data.textures[0].image_user)
        ## icon (low resolution)
        # icon_id = pcoll_from_local("D:\\User\\Pictures\\blender_ActionClips_to_Unity.png")
        # row.template_icon(icon_id,scale=5)


classes = [
    VP_OT_popup_confirm,
]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)