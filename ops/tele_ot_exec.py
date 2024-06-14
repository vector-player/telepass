import bpy

class TELE_OT_exec(bpy.types.Operator):
    """
    Use Case: bpy.ops.tele.exec(ref='init')
    """
    bl_idname = "tele.exec"
    bl_label = "tele.exec"
    bl_description = "Execute function of cloud addon"
    bl_options = {"REGISTER"}

    # id : bpy.props.StringProperty() # type: ignore
    ref : bpy.props.StringProperty() # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, ctx):        
        
        # id = self.id
        ## let operator decides the id, so that calling this operator in other addon is much more simple 
        if ctx.scene.portal_tab == 'market':
            id = ctx.scene.portal_active_market_addon_id
        else:
            id = ctx.scene.portal_active_user_addon_id

        msg = f"Call cloud function '{self.ref}' of Product No._{id}_, ..."
        print(msg)
        self.report({'INFO'}, msg)

        if not id:
            msg = 'SPU PK/ID not specified.'
            self.report({'INFO'}, msg)
            print(msg)
        if self.ref == '':
            msg = 'Sourcecode name not specified.'
            self.report({'INFO'}, msg)
            print(msg)
        from ..services.service_exec_code import get_code_by_name
        res = get_code_by_name(id, self.ref)
        
        
        try:          
            exec(res['code'])
        except Exception as e:
            
            bpy.ops.portal.msgbox('INVOKE_DEFAULT',msg="Error: " + str(e))
            print(e)
        return {"FINISHED"}
        
        # if res['has_error'] == True:
        #     msg = res['user_api_code'] + ';' + res['test_api_code'] + ";"

        # if res['code'] is None:
        #     msg += 'Cannot get source code.'

        # bpy.ops.portal.msgbox('INVOKE_DEFAULT',msg)
        # return {"FINISHED"}



classes = [
    TELE_OT_exec
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)