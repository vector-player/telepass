import bpy
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s【%(levelname)s】(%(name)s-No.%(lineno)d):%(funcName)s -> %(message)s")
logger = logging.getLogger(__name__)


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
        logger.info(msg)
        self.report({'INFO'}, msg)
        # bpy.ops.tele.msgbox('INVOKE_DEFAULT',msg=msg)

        if not id:
            msg = 'SPU PK/ID not specified.'
            self.report({'INFO'}, msg)
            bpy.ops.tele.msgbox('INVOKE_DEFAULT',msg=msg)
            print(msg)
        if self.ref == '':
            msg = 'Sourcecode name not specified.'
            self.report({'INFO'}, msg)
            bpy.ops.tele.msgbox('INVOKE_DEFAULT',msg=msg)
            print(msg)
        from ..services.service_exec_code import get_code_by_name
        res = get_code_by_name(id, self.ref)
        print(res)
        
        if res['has_error']:
            msg = f"Error: user api:{res['user_api_status_code']}; {res['user_api_res']}; \ntest api status_code:{res['test_api_status_code']}; {res['test_api_res']};\nException:{res['exception']}"
            self.report({'INFO'}, msg)
            bpy.ops.tele.msgbox('INVOKE_DEFAULT',msg=msg)
            return {"FINISHED"}
        
        elif res['code'] is None:
            msg = "No code to execute."
            self.report({'INFO'}, msg)
            bpy.ops.tele.msgbox('INVOKE_DEFAULT',msg=msg)
            return {"FINISHED"}
        
        else:
        
            try:          
                exec(res['code'])
            except Exception as e:                
                bpy.ops.tele.msgbox('INVOKE_DEFAULT',msg="Error: " + str(e))
                print(e)
                

            return {"FINISHED"}
        
        # if res['has_error'] == True:
        #     msg = res['user_api_code'] + ';' + res['test_api_code'] + ";"

        # if res['code'] is None:
        #     msg += 'Cannot get source code.'

        # bpy.ops.tele.msgbox('INVOKE_DEFAULT',msg)
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