import bpy
import sys
from . import service_task
import threading

  


class rpyc_tool:

    import rpyc 
    # import rpyc.utils.server
    # import rpyc.utils.helpers 
    

    @staticmethod        
    def start_server(service:rpyc.Service, port:int=18861):  
    # def start_server(service, port:int=18861):

        import rpyc
        # try:
        #     service_task.Task_tool.clear_port(port)
        # except Exception as e:
        #     print(e)
        service_task.Task_tool.clear_port(port)
        
        # service_with_args = rpyc.utils.helpers.classpartial(service, ctx)
        # t = rpyc.OneShotServer\
        t = rpyc.utils.server.ThreadedServer\
        (
            service,
            hostname= '0.0.0.0' ,##'183.27.155.54', #"192.168.1.203",
            port=port,
            # auto_register=True,
            protocol_config=\
            {
                'allow_all_attrs': True, 
                'allow_delattr': True, 
                'allow_exposed_attrs': True, 
                'allow_getattr': True, 
                'allow_pickle': True, 
                'allow_public_attrs': True, 
                'allow_safe_attrs': True, 
                'allow_setattr': True, 
                'before_closed': None, 
                'bind_threads': False, 
                'close_catchall': False, 
                'connid': None, 
                'credentials': None, 
                'endpoints': None, 
                'exposed_prefix': 'exposed_', 
                'import_custom_exceptions': True, 
                'include_local_traceback': True, 
                'include_local_version': True, 
                'instantiate_custom_exceptions': True, 
                'instantiate_oldstyle_exceptions': False, 
                'log_exceptions': True, 
                'logger': None, 
                'propagate_KeyboardInterrupt_locally': True, 
                'propagate_SystemExit_locally': False, 
                'sync_request_timeout': 30,
                'safe_attrs': \
                {
                    '__abs__', 
                    '__add__', 
                    '__and__', 
                    '__bool__', 
                    '__cmp__', 
                    '__contains__', 
                    '__delitem__', 
                    '__delslice__', 
                    '__div__', 
                    '__divmod__', 
                    '__doc__', 
                    '__enter__', 
                    '__eq__', 
                    '__exit__', 
                    '__float__', 
                    '__floordiv__', 
                    '__format__', 
                    '__ge__', 
                    '__getitem__', 
                    '__getslice__', 
                    '__gt__', 
                    '__hash__', 
                    '__hex__', 
                    '__iadd__', 
                    '__iand__', 
                    '__idiv__', 
                    '__ifloordiv__', 
                    '__ilshift__', 
                    '__imod__', 
                    '__imul__', 
                    '__index__', 
                    '__int__', 
                    '__invert__', 
                    '__ior__', 
                    '__ipow__', 
                    '__irshift__', 
                    '__isub__', 
                    '__iter__', 
                    '__itruediv__', 
                    '__ixor__', 
                    '__le__', 
                    '__len__', 
                    '__length_hint__', 
                    '__long__', 
                    '__lshift__', 
                    '__lt__', 
                    '__mod__', 
                    '__mul__', 
                    '__ne__', 
                    '__neg__', 
                    '__new__', 
                    '__next__', 
                    '__nonzero__', 
                    '__oct__', 
                    '__or__', 
                    '__pos__', 
                    '__pow__', 
                    '__radd__', 
                    '__rand__', 
                    '__rdiv__', 
                    '__rdivmod__', 
                    '__repr__', 
                    '__rfloordiv__', 
                    '__rlshift__', 
                    '__rmod__', 
                    '__rmul__', 
                    '__ror__', 
                    '__rpow__', 
                    '__rrshift__',
                    '__rshift__',
                    '__rsub__', 
                    '__rtruediv__',
                    '__rxor__', 
                    '__setitem__', 
                    '__setslice__', 
                    '__str__', 
                    '__sub__', 
                    '__truediv__', 
                    '__xor__', 
                    'next'
                }, 
            }
        )
        t.start()



    @staticmethod
    def slave_connect(ref:str):
        # rpyc.connect(master, port, service=slave)

        import rpyc

        
        # bpy.ops.portal.init('INVOKE_DEFAULT')
        
        ip = '192.168.1.203'
        port = 18860
        slave = rpyc_tool.BpyService()
        slave.exposed_ref = ref

        conn = rpyc.connect(ip, port, service=slave, keepalive=True)

        ## SocketStream
        # stream_r = rpyc.SocketStream.connect(ip, port, timeout=5.0)        
        # conn = rpyc.connect_stream(stream_r, service=slave)    # conn = rpyc.connect_stream(stream_r, config=config)

        ## Try async
        # conn._config['sync_request_timeout'] = None
        # rpyc.core.stream.SocketStream.MAX_IO_CHUNK = 2000000 
        # conn.root.hello()

        ## Try BgSvr: keep connection in New RpycSpawnThread
        bg_server = rpyc.BgServingThread(conn)
        # bg_server.stop()


    @staticmethod
    def call_mission(self, ref:str):
        t = threading.Thread(target=self.slave_connect, args=(self,ref))
        t.start()


    # @rpyc.service    
    class BpyService(rpyc.Service):
    # class BpyService(object):
        """
        argument: 
        - object<rpyc.Service> : Use 'object' instead of 'rpyc.Service' 
        to avoid error on blender launch when rpyc module is not installed in blender;
        or wrap this class into functions if you have to specify some rpyc class.

        """
        import rpyc
        import rpyc.utils.helpers
        import rpyc.utils.server

        exposed_ref = ''
        exposed_sys = sys
        exposed_bpy = bpy    
        exposed_ctx = None
        exposed_obj = None
        
        # @rpyc.exposed
        def exposed_get_modules(self):
            import sys
            modules = sys.modules
            return modules

        @rpyc.exposed
        def invoke_callback(self, callback):
            return callback()

        # exposed_bpy_data = bpy.data
        # exposed_bpy_ctx = bpy.context
        
        # def exposed_get_act_obj(self):
        #     return bpy.context.object
        
        # def __init__(self,ctx):
        #     self.exposed_ctx = ctx
            
        # def exposed_get_ctx(self):
        #     self.exposed_ctx = bpy.context.scene.ctx
        #     return bpy.context.scene.ctx

        def exposed_get_obj(self):
            # import bpy
            # # bpy.ops.holo.get_obj()
            # bpy.ops.portal.build_rig('INVOKE_DEFAULT')      
            
            # self.exposed_obj = bpy.context.object
            # return self.exposed_obj
            pass

        def exposed_exec(self):
            # exec('import bpy;bpy.context.object.data.vertices[0].co.y=20')
            exec('import bpy; bpy.context.view_layer.objects.active.data.vertices[0].co.y=20')

        
        def exposed_dir(self):
            import os
            return os.getcwd()
        
        def exposed_example_move(self):
            import bpy
            # bpy.context.object.data.vertices[0].co.y=20
            bpy.context.view_layer.objects.active.data.vertices[0].co.y=20

