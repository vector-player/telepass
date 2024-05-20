import zerorpc

def call_zerorpc():
    ctx = zerorpc.Client()
    ctx.connect("tcp://127.0.0.1:4242")
    print(ctx.object.name)

if __name__ == "__main__":
    call_zerorpc()