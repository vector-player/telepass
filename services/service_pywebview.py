
## Method A
import multiprocessing
# import sys
# ORIG_SYS_PATH = list(sys.path) # Make a new instance of sys.path
# import bpy # Here, the sys.path is severely messed with, screws up the import 
#            # in the new process that is created in multiprocessing.Pool()
# BPY_SYS_PATH = list(sys.path) # Make instance of `bpy`'s modified sys.path
# sys.path = ORIG_SYS_PATH
# # sys.path = BPY_SYS_PATH

## Method B
# import multiprocessing
# from multiprocessing import current_process
# if current_process().name == 'MainProcess':
#     import bpy

from ..views.preferences import check_installed
import threading
from .. import settings
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s【%(levelname)s】(%(name)s-No.%(lineno)d):%(funcName)s -> %(message)s")
logger = logging.getLogger(__name__)
# logger.setLevel(level = logging.INFO)

is_webview_installed = check_installed('webview')

def display_html_string(html_string, header:str="", on_top:bool=True):
    # logger.debug("display_html_string:header='{}', on_top={}".format(header, on_top))
    try:
        if is_webview_installed:
            import webview
            webview.create_window(header, html=html_string, on_top=on_top, background_color='#FFFFFF', )
            webview.start()
            # webview.start(blocking = False)
            # webview.start(daemon=True)
        else:
            print("service_pywebview: pywebview is not installed.")
    except Exception as e:
        print('\n',e,'\n')

def display_html_online(url, header:str="", on_top:bool=True, background_color='#FFFFFF',):
    try:
        if is_webview_installed:
            import webview
            webview.create_window(header, url, on_top=on_top)
            webview.start()
            # webview.start(block=False)
            # webview.start(daemon=True)
        else:
            print("service_pywebview: pywebview is not installed.")
    except Exception as e:
        print('\n',e,'\n')


def create_window(html_string, header:str='', on_top:bool=True):
    import webview
    window = webview.create_window(header, html=html_string, on_top=on_top, background_color='#FFFFFF',)


def new_process_display(html_string, header:str="", on_top:bool=True):
    import sys
    sys.path = settings.BPY_SYS_PATH
    # import multiprocessing
    p = multiprocessing.Process(target=display_html_string, args=(html_string, ))
    # import bpy
    # sys.path = settings.BPY_SYS_PATH
    # p.daemon = True
    p.start()
    # p.join()

def new_thread_display(html_string, header:str="", on_top:bool=True):
    t = threading.Thread(
        target=display_html_string, 
        args=(html_string, ), 
        kwargs={'header':header,'on_top':on_top,},
    )
    t.setName("pywebview") 
    # t.setDaemon(True) # kill t if main_thread close. ## causing conflict ?
    t.start()
    # t.join()




def new_thread_with_js(html_string, header:str=""):
    def evaluate_js(window):
        window.evaluate_js('alert("welcome")')
    import webview
    window = webview.create_window(header, html=html_string)
    webview.start(evaluate_js, window)
    # anything below this line will be executed after program is finished executing
    print("webview closed.")





if __name__ == "__main__":
    display_html_string("<h1>h1</h1>")