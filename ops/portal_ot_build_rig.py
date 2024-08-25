import bpy
import threading    
from ..views.preferences import check_installed
from ..views.msgbox import msgbox
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s【%(levelname)s】(%(name)s-No.%(lineno)d):%(funcName)s -> %(message)s")
logger = logging.getLogger(__name__)



class PORTAL_OT_build_rig(bpy.types.Operator):
    bl_idname = "portal.build_rig"
    bl_label = "Portal Rig"
    bl_description = "Start Portal Rig service"
    bl_options = {"REGISTER"}

    # ip : bpy.props.StringProperty(default="")
    # act_obj:bpy.props.PointerProperty(type=bpy.types.Object)
    ## Error:PointerProperty is not for operator?
    ## apparently operators can only take basic properties
    ##  (e.g. string, bool, int, float, collections of the property types just mentioned), 
    ## and PointerProperties only work if they’re stored within at the scene level 
    ## (e.g. bpy.types.Scene) or inside a PropertyGroup.

    @classmethod
    def poll(cls, ctx):
        return True

    def execute(self, ctx): 
        if not check_installed('rpyc'):
            msg = "RPyC is not installed. Please install it in User Preferences."
            # cls.report({'INFO'}, msg)
            # msgbox(msg, 'Warning', 'ERROR')
            bpy.ops.tele.msgbox('INVOKE_DEFAULT', msg=msg)
            logger.debug("{}".format(msg))

            return {"FINISHED"}

        from ..services.service_network import public_ip
        ctx.scene.portal_rig_service_ip = public_ip()
        if ctx.scene.portal_rig_service_ip == "":
            msg = "Operator abort: Portal Rig root IP address is empty."
            # cls.report({'ERROR'}, err)
            # msgbox(err, 'Warning', 'ERROR')
            bpy.ops.tele.msgbox('INVOKE_DEFAULT', msg=msg)
            logger.debug("{}".format(msg))           
            return {"FINISHED"}

        # services.global_variable.set('ctx',ctx)
        # ctx.scene.obj = ctx.object
        # myobj_py = {'data': ctx.object}
        # myobj_json = services.service_file.fileTool.string_writejson(myobj_py) ## Error:Object of type Object is not JSON serializable
        # myobj_pickle = pickle.dumps(ctx.object)  ## Error:can not pickle 'Object' object
        # myobj_pickle = pickle.dumps(myobj_py)  ## Error:can not pickle 'Object' object
        # myobj_json = services.service_file.fileTool.string_encoder_writejson(myobj_py) ## AttributeError: 'Object' object has no attribute '__dict__'. Did you mean: '__doc__'?
        # myobj_json = services.service_file.fileTool.bpy_obj_encoder_writejson_string(ctx.object)
        # multiprocessing.managers.BaseManager.register('act_obj',ctx.object)

        # x = requests.post(url, json = myobj_json)
        # print('object name:',myobj_py.data.name)
        # print(x.text)

        # services.service_pyro.start_pyro()
        # services.service_zerorpc.start_zerorpc()
        
        # t1 = threading.Thread(target=self.start_rpyc,args=(ctx,))  ## the real 'ctx' will lost after opt 'FINISHED', so a wrong and empty 'ctx' would be pass to thread
        # t1 = threading.Thread(target=self.start_rpyc(ctx))  ## To catch the real 'ctx' by instancing before Opt 'FINISHED'. However, thread instance causes sync blocking and screen freezing.
        msg = 'Start Portal Rig service.'
        self.report({'INFO'}, msg)
        logger.debug("{}".format(msg))

        ## Comment out python threading to avoid multi-threads conflict: Using RPyC ThreadedServer
        # self.start_rpyc()

        ## Detached from main thread to avoid blocking operator's 'FINISHED' process.
        t1 = threading.Thread(target=self.start_rpyc)
        t1.start()
        
        return {"FINISHED"}
    

    def start_rpyc(self):      
        import rpyc
        import rpyc.utils.helpers 
        from ..services import service_rpyc
        from ..services.service_rpyc import rpyc_tool

        # srv = services.service_rpyc.Service_bpy(ctx)
        # ctx = services.global_variable.get('ctx')
        # print('ctx.object:',ctx.object)
        # srv = services.service_rpyc.Service_bpy(ctx)                
        # srv = service_rpyc.Service_bpy() 
        
        ## Start service: BpyService
        srv = rpyc_tool.BpyService()
        # rpyc_tool.start_server(srv)
        rpyc_tool.start_server(srv)


classes = [
    PORTAL_OT_build_rig,
]
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)