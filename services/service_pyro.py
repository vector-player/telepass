
import bpy
import Pyro4




def start_pyro_daemon():
    daemon = Pyro4.Daemon()    
    uri = daemon.register(bpy.context)  ## Pyro4\core.py", line 1616, in register
                                        ## obj_or_class._pyroId = objectId
                                        ## AttributeError: 'Context' object has no attribute '_pyroId'

    ns = Pyro4.locateNS()
    ns.register("holo.ctx", uri)
    print("Pyro daemon start... ctx uri =", uri)
    daemon.requestLoop()