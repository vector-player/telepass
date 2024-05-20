import bpy

class PORTAL_OT_rig(bpy.types.Operator):
    """
    Use Case: bpy.ops.portal.rig(ref='file_name')
    """
    bl_idname = "portal.rig"
    bl_label = "Portal Call"
    bl_description = "Call RPC service for custom mission"
    bl_options = {"REGISTER"}

    ref : bpy.props.StringProperty(default='')

    @classmethod
    def poll(cls, context):  
        return True

    def execute(self, context):
        ## Check dependency
        from ..views.preferences import is_installed
        if not is_installed('rpyc'):
            msg = "RPyC is not installed. Please install it in User Preferences."
            # cls.report({'INFO'}, msg)
            from ..views.msgbox import msgbox
            # msgbox(msg, 'Warning', 'ERROR')
            bpy.ops.portal.msgbox('INVOKE_DEFAULT', msg=msg)
            print(msg)
            return {"FINISHED"}

        from ..services.service_rpyc import rpyc_tool
        if self.ref == '':
            self.report({'INFO'}, 'Ref target to call is empty.')
            return {"FINISHED"}
        rpyc_tool.slave_connect(self.ref)
        return {"FINISHED"}


classes = [
    PORTAL_OT_rig
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)