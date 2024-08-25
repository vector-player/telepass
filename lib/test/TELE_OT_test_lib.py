import bpy
# import test_html_file
# import pywebview_test

class TELE_OT_test_lib(bpy.types.Operator):
    bl_idname = "tele.test_lib"
    bl_label = "Test Library"
    bl_description = "Test standalone library"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # test_html_file.render_index()
        # pywebview_test.display_html_string()
        return {"FINISHED"}



classes = [
    TELE_OT_test_lib
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)