import bpy

class PORTAL_OT_call(bpy.types.Operator):
    """
    Use Case: bpy.ops.portal.call(ref='init')
    """
    bl_idname = "portal.call"
    bl_label = "Portal Call"
    bl_description = "Call RESTFUL API to exec codes"
    bl_options = {"REGISTER"}

    id : bpy.props.StringProperty() # type: ignore
    ref : bpy.props.StringProperty() # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, ctx):
        # id = ctx.scene.portal_active_user_addon_id
        id = self.id
        if not id:
            msg = 'SPU PK/ID not specified.'
            self.report({'INFO'}, msg)
            print(msg)
        if self.ref == '':
            msg = 'Sourcecode name not specified.'
            self.report({'INFO'}, msg)
            print(msg)
        from ..services.service_exec_code import get_code_by_name
        code = get_code_by_name(id, self.ref)
        if code == False or code is None: 
            bpy.ops.portal.msgbox('INVOKE_DEFAULT',msg='Cannot get source code.')
            return {"FINISHED"}

        try:          
            exec(code)
        except Exception as e:
            bpy.ops.portal.msgbox('INVOKE_DEFAULT',msg=str(e))
            print(e)
        return {"FINISHED"}

classes = [
    PORTAL_OT_call
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)