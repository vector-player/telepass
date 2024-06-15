import bpy




def msgbox(message="", title="Message Box", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
    
# message = "Test message"
# title = "Test Title"
# msgbox(message, title)





class TELE_OT_msgbox(bpy.types.Operator):
    bl_idname = "tele.msgbox"
    bl_label = "Notice"
    bl_description = "Message Box with confirm button"
    bl_options = {"REGISTER"}

    msg : bpy.props.StringProperty(default='') # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({'INFO'}, 'OK')
        return {"FINISHED"}
    
    def invoke(self, context, event):
        # return context.window_manager.invoke_confirm(self, event)
        return context.window_manager.invoke_props_dialog(self)

    def get_list(self, msg):
        return list(msg.split(";"))

    def draw(self, ctx):
        
        msg_list = self.get_list(self.msg)
        for msg in msg_list:
            row = self.layout
            row.label(text=msg)
    
        
        


classes = [
    TELE_OT_msgbox,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)