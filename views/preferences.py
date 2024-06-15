import bpy
from .. import addon_updater_ops
from bpy.app.translations import pgettext as ptext
from ..settings import addon_name, portal_user_addons_url
from .main_panel import PORTAL_PT_main_panel
import sys
import os
import importlib
import ctypes
from typing import Annotated
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s【%(levelname)s】(%(name)s-No.%(lineno)d):%(funcName)s -> %(message)s")
logger = logging.getLogger(__name__)


##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++##
## Define Functions                                                          ##
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++##


def is_console_window_open():
    # this function works only with ms-windows system
    # Get Handler of Console Window
    console_window_handle = ctypes.windll.kernel32.GetConsoleWindow()
    if console_window_handle:
        # Get visibility of Console Window
        window_visibility = ctypes.windll.user32.IsWindowVisible(console_window_handle)
        if window_visibility == 0:
            return False
        else:
            return True
    else:
        return False

def activate_console_window():
    # # get handler of console window:
    console_window_handle = ctypes.windll.kernel32.GetConsoleWindow()
    if console_window_handle:
        # # activate console window on top:
        ctypes.windll.user32.SetForegroundWindow(console_window_handle)
# if __name__ == "__main__":
# open console window

def open_bpy_console_if_not():
    if is_console_window_open() == False: bpy.ops.wm.console_toggle()
    activate_console_window()



#This code assumes your folder name is the name of your addon
#It also assumes that this function is placed inside a .py file in the base folder

#get the folder path for the .py file containing this function
def get_path():
    return os.path.dirname(os.path.realpath(__file__))

#get the name of the 'base' folder
def get_name():
    return os.path.basename(get_path())

#now that we have the addons name we can get the preferences
def get_prefs():
    return bpy.context.preferences.addons[get_name()].preferences


## Class Factory of Installing Dependency
def class_factory_ops_install_mod(mod_name):
    @classmethod
    def poll(cls, context):
        return not False
    def execute(self, context):
        import subprocess
        python_exe = sys.executable
        open_bpy_console_if_not()
        subprocess.call([python_exe, '-m', 'ensurepip', '--upgrade'])
        subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.call([python_exe, '-m', 'pip', 'install', f'{mod_name}'])
        return {"FINISHED"}
    def invoke(self, context, event):
        return self.execute(context)

    class_name = f"VP_OT_install_{mod_name}"
    class_parent = (bpy.types.Operator,)
    class_members = {
        "bl_idname" : f"vp.install_{mod_name}",
        "bl_label" : f"install_{mod_name}",
        "bl_options" : {"REGISTER"},
        "bl_description" : "press to install this module as addon dependency",
        "poll" : poll,
        "execute" : execute,
        "invoke" : invoke,    
    }

    my_class = type(class_name, class_parent, class_members)
    return my_class
# ## Usecase
# VP_OT_install_mymod = class_factory_ops_install_mod("mymod")
# bpy.utils.register_class(VP_OT_install_mymod)


## Class Factory of Uninstalling Dependency
# import bpy
# import sys
def class_factory_ops_uninstall_mod(mod_name):
    @classmethod
    def poll(cls, context):
        return not False
    def execute(self, context):
        import subprocess
        python_exe = sys.executable
        open_bpy_console_if_not()
        subprocess.call([python_exe, '-m', 'ensurepip', '--upgrade'])
        subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.call([python_exe, '-m', 'pip', 'uninstall', f'{mod_name}'])
        return {"FINISHED"}
    def invoke(self, context, event):
        return self.execute(context)

    class_name = f"VP_OT_uninstall_{mod_name}"
    class_parent = (bpy.types.Operator,)
    class_members = {
        "bl_idname" : f"vp.uninstall_{mod_name}",
        "bl_label" : f"uninstall_{mod_name}",
        "bl_options" : {"REGISTER"},
        "bl_description" : "Warning:uninstall this module from addon dependencies might cause error",
        "poll" : poll,
        "execute" : execute,
        "invoke" : invoke,    
    }
    my_class = type(class_name, class_parent, class_members)
    return my_class

# ## Usecase
# VP_OT_uninstall_mymod = class_factory_ops_uninstall_mod("mymod")
# bpy.utils.register_class(VP_OT_uninstall_mymod)


def is_installed(mod_name) -> bool:
    """ Checks if dependency is installed. """
    try:
        spec = importlib.util.find_spec(mod_name)
    except (ModuleNotFoundError, ValueError, AttributeError): 
        print(mod_name,"is not installed")           
        return False

    # only accept it as valid if there is a source file for the module - not bytecode only.
    if issubclass(type(spec), importlib.machinery.ModuleSpec):
        print(mod_name,"is installed")         
        return True

    print(mod_name,"is not installed")  
    return False


## UPDATE-listening function
def on_switch_has_n_panel(self,ctx):
    
    property_name = 'has_n_panel'
    panel_class = PORTAL_PT_main_panel
    # if ctx.preferences.addons[addon_name].preferences.has_n_panel == True:
    if getattr(ctx.preferences.addons[addon_name].preferences,property_name) == True:
        if not hasattr(bpy.types,panel_class.__name__):
            bpy.utils.register_class(panel_class)
    else:
        if hasattr(bpy.types,panel_class.__name__):
            bpy.utils.unregister_class(panel_class)


##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++##
## Define Class                                                                         ##
##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++##
# VP_OT_install_pywin32 = class_factory_ops_install_mod("pywin32")
# VP_OT_uninstall_pywin32 = class_factory_ops_uninstall_mod("pywin32")
PORTAL_OT_install_rpyc = class_factory_ops_install_mod('rpyc')
PORTAL_OT_uninstall_rpyc = class_factory_ops_uninstall_mod('rpyc')

PORTAL_OT_install_requests = class_factory_ops_install_mod('requests')
PORTAL_OT_uninstall_requests = class_factory_ops_uninstall_mod('requests')
##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ExampleAddonPreferences(bpy.types.AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    # bl_idname = __name__
    # bl_idname = __package__
    bl_idname = addon_name

    ## Preferences Props: referenced with 'ctx.preferences.addons[addon_name].preferences.props'
    ## type ignore: see https://github.com/microsoft/pylance-release/issues/5457
    
    has_n_panel : bpy.props.BoolProperty(name=ptext('Show in N-Panel'),default=True, update=on_switch_has_n_panel) # type: ignore
    # is_some : bpy.props.BoolProperty(default=False)

    portal_ip : bpy.props.StringProperty(default=portal_user_addons_url) # type: ignore
    portal_username : bpy.props.StringProperty() # type: ignore
    portal_password : bpy.props.StringProperty(subtype='PASSWORD') # type: ignore

    filepath: bpy.props.StringProperty(
        name='Example File Path',
        subtype='FILE_PATH',
    ) # type: ignore
    number: bpy.props.IntProperty(
        name='Example Number',
        default=4,
    ) # type: ignore
    boolean: bpy.props.BoolProperty(
        name='Example Boolean',
        default=False,
    ) # type: ignore


    # addon updater preferences from `__init__`, be sure to copy all of them
    auto_check_update : bpy.props.BoolProperty(
        name = "Auto-check for Update",
        description = "If enabled, auto-check for updates using an interval",
        default = False,
    ) # type: ignore

    updater_interval_months : bpy.props.IntProperty(
        name='Months',
        description = "Number of months between checking for updates",
        default=0,
        min=0
    ) # type: ignore


    updater_interval_days : bpy.props.IntProperty(
        name='Days',
        description = "Number of days between checking for updates",
        default=7,
        min=0,
    ) # type: ignore
    updater_interval_hours : bpy.props.IntProperty(
        name='Hours',
        description = "Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    ) # type: ignore
    updater_interval_minutes : bpy.props.IntProperty(
        name='Minutes',
        description = "Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    ) # type: ignore



    def draw(self, ctx):
        RPyC_installed = is_installed('rpyc')  ## is_installed('win32api') and is_installed('win32gui') and is_installed('win32con')
        REQUESTS_installed = is_installed('requests')

        layout = self.layout        
        row = layout.row()

        col_install = row.column()
        col_install.enabled = not RPyC_installed
        op_install_mod = col_install.operator(PORTAL_OT_install_rpyc.bl_idname, text=ptext('Install RPyC'), icon_value=36, emboss=not RPyC_installed, depress=not RPyC_installed)
        col_uninstall = row.column()
        col_uninstall.enabled = RPyC_installed
        op_uninstall_mod = col_uninstall.operator(PORTAL_OT_uninstall_rpyc.bl_idname, text=ptext('remove RPyC'), icon_value=19, emboss=RPyC_installed, depress=RPyC_installed)
        row = layout.row()
        col_install = row.column()
        col_install.enabled = not REQUESTS_installed
        op_install_mod = col_install.operator(PORTAL_OT_install_requests.bl_idname, text=ptext('Install Requests'), icon_value=36, emboss=not REQUESTS_installed, depress=not REQUESTS_installed)
        col_uninstall = row.column()
        col_uninstall.enabled = REQUESTS_installed
        op_uninstall_mod = col_uninstall.operator(PORTAL_OT_uninstall_requests.bl_idname, text=ptext('remove Requests'), icon_value=19, emboss=REQUESTS_installed, depress=REQUESTS_installed)

        layout.label(text='This is a preferences view for our add-on')
        row  = layout.row()
        row.operator('portal.init')  # 
        layout.prop(self, 'filepath')
        layout.prop(self, 'number')
        layout.prop(self, 'boolean')

        row_ui_wigets = layout.row()
        col = row_ui_wigets.column()
        col.prop(self,'has_n_panel',text=ptext('Show in N-Panel:'))
        col = row_ui_wigets.column()
        col.prop(get_user_keyconfig(HOT_KEY_NAME_001), 'type', text=ptext('Hot Key'), full_event=True)

        addon_updater_ops.update_settings_ui(self,ctx)

##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++##
## Define HOT-KEY                                           ##
##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++##
    
## Step for Hotkey Mapping:
## 1. Register a new keymap with a custom name, bind a key to a bpy.ops, and append it into a custom keymaps dictionary for later retrieving.
## 2. define a function (get_user_keyconfig) to retrieve any keymap item by giving the custom name
## 3. call the function in layout, better to call in PREFERENCES so that keymap could be customized and auto saved for changes. like:
## layout.prop(get_user_keyconfig(HOT_KEY_NAME_001), 'type', text=ptext('Hot Key:'), full_event=True)

addon_keymaps = {} 
## keymap item should be name with String, and define in hotkey register file
HOT_KEY_NAME_001 = 'PIM_PANEL_HOT_KEY'

def get_user_keyconfig(key):
    km, kmi = addon_keymaps[key]
    for item in bpy.context.window_manager.keyconfigs.user.keymaps[km.name].keymap_items:
        found_item = False
        if kmi.idname == item.idname:
            found_item = True
            for name in dir(kmi.properties):
                if not name in ["bl_rna", "rna_type"] and not name[0] == "_":
                    if name in kmi.properties and name in item.properties and not kmi.properties[name] == item.properties[name]:
                        found_item = False
        if found_item:
            return item

    logger.debug("Couldn't find keymap item for '{}', using addon keymap instead. This won't be saved across sessions!".format(key))
    return kmi


##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++##
## Register                                                      ##
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++##
classes = [
    PORTAL_OT_install_rpyc,
    PORTAL_OT_uninstall_rpyc,
    PORTAL_OT_install_requests,
    PORTAL_OT_uninstall_requests,
    ExampleAddonPreferences,
]

def register():

    ## Register hot key map 001:
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='Window', space_type='EMPTY')
    kmi = km.keymap_items.new('wm.call_panel', 'P', 'PRESS',
        ctrl=True, alt=True, shift=True, repeat=True)
    kmi.properties.name = 'PORTAL_PT_main_panel'##'PIM_MT_menu'
    kmi.properties.keep_open = True  ## for 'panel' not for 'menu'
    addon_keymaps[HOT_KEY_NAME_001] = (km, kmi)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    ## unregister hot key map
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()





