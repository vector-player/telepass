import bpy
from ..services import service_ctx
# from ..services import service_ctx
import runpy

class HOLO_OT_run_script(bpy.types.Operator):
    bl_idname = "holo.run_script"
    bl_label = "run script"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER"}

    filepath:bpy.props.StringProperty
    
    @classmethod
    def poll(cls, ctx):
        return True

    def execute(self, ctx):
        #overwrite ctx
        context = service_ctx.prepare_script_context(self.filepath)
        runpy.run_path(self.filepath, init_globals={"CTX" : context})
        self.redraw_all()
        return {"FINISHED"}

    def redraw_all():
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                area.tag_redraw()


classes = [
    HOLO_OT_run_script,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)