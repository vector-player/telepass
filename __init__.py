bl_info = {
    "name": "Telepass",
    "author": "vector-player@outlook.com",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > N-Panel > Telepass",
    "description": "Cloud addons market",
    "warning": "Use at your own risk",
    "wiki_url": "",
    "category": "Vector-Player",
    }



# import sys
import os
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# sys.path.append(os.path.abspath('.views')) 
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s【%(levelname)s】(%(name)s-No.%(lineno)d):%(funcName)s -> %(message)s")
logger = logging.getLogger(__name__)
import bpy
from . import addon_updater_ops
from . import settings
from .views import main_panel, preferences, global_props, msgbox
from .views import msgbox
# from .views import ops as view_opt
# from .views import preferences
# from .views import opt
from .ops import (
    portal_ot_restore_default,
    portal_ot_init,
    holo_ot_run_script,
    portal_ot_login, 
    portal_ot_guest,
    portal_ot_open_active_addon,
    portal_ot_build_rig,
    portal_ot_rig,
    portal_ot_show_detail,
    portal_ot_tab,
    tele_ot_exec,
)
from .services import service_previews
from .services.service_previews import previews
from .lib.test import TELE_OT_test_lib

# print("cwd:",os.getcwd())




def on_register():
    ## To get market info automatically
    try:
        bpy.ops.portal.init('INVOKE_DEFAULT')
    except Exception as e:
        logger.debug("Error while try to get market info on register:{}".format(e))
    ## this will happen .01 seconds after addon registration completes.
    ## according to the timer in rergister() function.
    # try:
    #     logo_path = os.path.join(settings.img_dir,'LOGO_PORTAL.png')
    #     # logo_path = "D:\\User\\Pictures\\blender_ActionClips_to_Unity.png"
    #     img = bpy.data.images.load(logo_path)
    #     # img.generated_width = 50
    #     # img.generated_height = 20
    #     img.scale(10,70)
    #     # img.display_aspect=(1,0.5)
    #     # img.update()
    #     # img.name = 'portal_logo.png'
    #     bpy.context.scene.portal_logo = img
        
    # except Exception as e:
    #     print(e)

    ## return None: the timer will be unregistered.
    ## return number:specifies the delay until the function is called again.
    ## set return number in preferences: 
    # return bpy.context.preferences.addons[addon_name].preferences.pim_recheck_time

    


def register():
    addon_updater_ops.register(bl_info)
    portal_ot_restore_default.register()
    portal_ot_init.register()
    holo_ot_run_script.register()
    portal_ot_build_rig.register()
    portal_ot_login.register()
    portal_ot_guest.register()
    portal_ot_open_active_addon.register()
    portal_ot_show_detail.register()
    portal_ot_tab.register()
    portal_ot_rig.register()
    tele_ot_exec.register()
    # view_opt.register()
    main_panel.register()
    msgbox.register()
    service_previews.register()
    preferences.register()
    global_props.register()
    TELE_OT_test_lib.register()

    ## timer for callback after register
    bpy.app.timers.register(on_register, first_interval=1)
    
    # previews = bpy.utils.previews.ImagePreviewCollection.new()
    


def unregister():
    portal_ot_restore_default.unregister()
    portal_ot_init.unregister()
    main_panel.unregister()
    msgbox.unregister()
    # view_opt.unregister()
    service_previews.unregister()
    preferences.unregister()
    global_props.unregister()
    holo_ot_run_script.unregister()
    portal_ot_build_rig.unregister()
    portal_ot_guest.unregister()
    portal_ot_login.unregister()
    portal_ot_open_active_addon.unregister()
    portal_ot_show_detail.unregister()
    portal_ot_tab.unregister()
    portal_ot_rig.unregister()
    tele_ot_exec.unregister()
    TELE_OT_test_lib.unregister()
    # bpy.utils.previews.remove(previews['global'])
    # bpy.utils.previews.remove(previews['market_sku'])
    # bpy.utils.previews.remove(previews['user_sku'])
    for pcoll in previews:
        if type(pcoll) is bpy.types.ImagePreview:
            bpy.utils.previews.remove(pcoll)
    previews.clear()


if __name__ == "__main__":
    register()