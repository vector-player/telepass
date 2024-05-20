import bpy
import zerorpc

def start_zerorpc():
    s = zerorpc.Server(bpy.types.Context)
    # s.bind("tcp://0.0.0.0:4242")
    s.bind("tcp://127.0.0.1:4242")
    s.run()
    print("zeroRPC started...")