import bpy


class PORTAL_OT_init(bpy.types.Operator):
    bl_idname = "portal.init"
    bl_label = "Refresh"
    bl_description = "Refresh, restart or recover from errors"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, ctx):
        self.try_guest(ctx)
        # self.try_rpyc(ctx)
        
        return {"FINISHED"}

    def try_guest(self,ctx):
        try:
            bpy.ops.portal.guest('INVOKE_DEFAULT')        
        except Exception as e:
            msg = 'Something wrong while connecting...'
            # msgbox(msg, 'Warning')
            bpy.ops.tele.msgbox('INVOKE_DEFAULT', msg=msg)
            self.report({'INFO'}, msg)
            print(e) 


    # def try_rpyc(self,ctx):
    #     try:
    #         bpy.ops.portal.build_rig('INVOKE_DEFAULT')
    #     except Exception as e:
    #         msg = 'Portal Rig server init error.'
    #         # msgbox(msg, 'Warning')
    #         bpy.ops.tele.msgbox('INVOKE_DEFAULT', msg=msg)
    #         self.report({'INFO'}, msg)
    #         print(e)




classes = [
    PORTAL_OT_init,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)