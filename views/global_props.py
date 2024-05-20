import bpy

def register():
    bpy.types.Scene.portal_tab = bpy.props.EnumProperty(
        items = [
            #(identifier, name, description, icon, number),
            ('market', 'market', 'market'),
            ('my', 'my', 'my'),
        ],
        name = 'portal_tab',
        description='portal_tab',
        # update=on_update,
    )
  
         
    # bpy.types.Scene.portal_username = bpy.props.StringProperty()
    # bpy.types.Scene.portal_password = bpy.props.StringProperty(subtype='PASSWORD')
    # bpy.types.Scene.is_login = bpy.props.BoolProperty(default=False)
    # bpy.types.Scene.portal_ip = bpy.props.StringProperty(default="127.0.0.1")
    # bpy.types.Scene.obj = bpy.props.PointerProperty(type=bpy.types.Object)
    # bpy.types.Scene.user_addon_names
    bpy.types.Scene.portal_active_market_addon_id = bpy.props.StringProperty()
    bpy.types.Scene.portal_active_user_addon_id = bpy.props.StringProperty()
    bpy.types.Scene.portal_logo = bpy.props.PointerProperty(type=bpy.types.Image)
    bpy.types.Scene.portal_rig_service_ip = bpy.props.StringProperty(default='')
    bpy.types.Scene.portal_active_addon_status = bpy.props.StringProperty()

def unregister():

    del bpy.types.Scene.portal_tab
    # del bpy.types.Scene.portal_username
    # del bpy.types.Scene.portal_password
    # del bpy.types.Scene.portal_ip
    del bpy.types.Scene.portal_active_user_addon_id
    del bpy.types.Scene.portal_active_market_addon_id
    del bpy.types.Scene.portal_logo
    del bpy.types.Scene.portal_rig_service_ip
    del bpy.types.Scene.portal_active_addon_status
