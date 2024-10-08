# import sys
# import os
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import bpy
from .. import addon_updater_ops
import os
from bpy.app.translations import pgettext as ptext
from .. settings import addon_name, img_dir
from .. services import service_previews


class PORTAL_PT_main_panel(bpy.types.Panel):
    bl_idname = "PORTAL_PT_main_panel"
    
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "TELEPASS"
    bl_label = "TELEPASS: my cloud addons"

    def draw(self, ctx):
        scn = ctx.scene
        layout = self.layout
        # try:
        #     box = layout.box()
        #     # box.scale_y = 0.2
        #     row_logo = box.row()        
        #     # row_logo.template_preview(bpy.data.images['LOGO_PORTAL'])
        #     # row_logo.template_preview(bpy.data.textures["LOGO_PORTAL"])
            
            
        #     icon_id = service_previews.pcoll_from_local(os.path.join(img_dir,'LOGO_PORTAL.png'))
        #     row_logo.template_icon(icon_value=icon_id, scale=1)
        #     # row_logo.template_icon_view(scn,'portal_logo', show_labels=False, scale=5,)
        # except Exception as e:
        #     print("Panel Error:logo" + "\n")
        #     print(e)

        # addon_updater_ops.check_for_update_background(ctx)
        addon_updater_ops.check_for_update_background()

        row_login = layout.row()
        # if not ctx.scene.is_login:
        row_login_1 = layout.row()
        row_login_1.prop(ctx.preferences.addons[addon_name].preferences,"portal_ip", text=ptext("HOST"))
        row_login_1.operator('portal.default', text='', icon='RECOVER_LAST')
        row_login_2 = layout.row()
        row_login_2.prop(ctx.preferences.addons[addon_name].preferences,"portal_username", text=ptext("USER"), icon='COMMUNITY')
        row_login_3 = layout.row()
        row_login_3.prop(ctx.preferences.addons[addon_name].preferences,"portal_password",text=ptext("PASSWORD"), icon='KEYINGSET')
        row_login_4 = layout.row()
        row_login_4.operator('portal.init', text='', icon='FILE_REFRESH')
        row_login_4.operator('portal.login')
        row_login_4.operator('preferences.addon_show',icon='PREFERENCES',).module=addon_name
        # row_login_4.prop(ctx.preferences.addons[addon_name],"preferences", toggle=-1, icon='PREFERENCES',icon_only=True, )


        box_tab = layout.box()
        row_tab = box_tab.row()
        # row_tab.prop_menu_enum(scn, 'portal_tab',text='text')
        row_tab_col = row_tab.column()
        row_tab_col.operator('portal.tab',text=ptext('market'),emboss=scn.portal_tab=='market', depress=scn.portal_tab=='market').select_tab='market'
        row_tab_col = row_tab.column()
        row_tab_col.operator('portal.tab',text=ptext('my'),emboss=scn.portal_tab=='my', depress=scn.portal_tab=='my').select_tab='my'
        # row_tab_col = row_tab.column()
        # row_tab_col.operator('render.render')

        if scn.portal_tab == 'market' :
            # scn.portal_active_addon_status = 'Subscribe'
            # count = 0
            # for i,item in enumerate(ctx.scene.bl_rna.properties['portal_sku_market_previews'].enum_items):
            #     count = i
            # print('Panel INFO: market enum_items:',count)

            row_preview = layout.row()
            row_preview.template_icon_view(
                ctx.scene, 
                "portal_sku_market_previews",
                show_labels=True,                
                scale=6.0, 
                scale_popup=5.0,
            )
            row_droplist = layout.row()
            row_droplist.prop(ctx.scene, "portal_sku_market_previews")

        if scn.portal_tab == 'my':
            
            # scn.portal_active_addon_status = 'Open'
            # print('Panel preview user items:',len(ctx.scene.bl_rna.properties['portal_sku_user_previews'].enum_items))
            row_preview = layout.row()
            row_preview.template_icon_view(
                ctx.scene, 
                "portal_sku_user_previews",
                show_labels=True,
                scale=6.0, 
                scale_popup=5.0,
            )
            row_droplist = layout.row()
            row_droplist.prop(ctx.scene, "portal_sku_user_previews")

        row_current_images = layout.row()

        # if len(ctx.scene.portal_sku_detail_previews) > 0: ## Error: current value '0' matches no enum in 'Scene', 'Scene', 'portal_sku_detail_previews'
        row_preview = row_current_images.row()            
        row_preview.template_icon_view(
            ctx.scene, 
            "portal_sku_detail_previews",
            show_labels=True,
            scale=6.0, 
            scale_popup=5.0,
        )

        grid = layout.grid_flow(columns=5, even_columns=True, even_rows=False)
        grid.scale_y = 3
        pcoll = service_previews.previews['global']
        for i,name in enumerate(pcoll):
            cell = grid.column().box()
            cell.template_icon(icon_value=pcoll[name].icon_id, scale=1)
            cell.label(text=name)
            cell.label(text=str(pcoll[name].icon_id))
            o = cell.operator("render.render")

        ## detail webpage content showed with webview   
        row_current_detail = layout.row() 
        col_current_summary = row_current_detail.column()
        col_current_summary.operator('portal.show_detail')  ## operator('vp.popup_confirm')
        
        ## active addon has 2 different functions to switch in realtime, to open website or to exec current addon.
        ## depend on the global variable of 'scn.portal_active_addon_status'
        ## this variable will be change by 'portal_ot_tab' & 'service_preview'
        col_current_open = row_current_detail.column()
        col_current_open.operator('portal.open_active_addon', text=ptext(scn.portal_active_addon_status))

        ## test: UI Condition
        # row_lbl = layout.row()
        # row_lbl.label(text="Select an object in scene")        
        # if ctx.object:
            # row_obj = layout.row()
            # row_obj.prop(ctx.object,"name")            
            # row_btn = layout.row()
            # opt_cn = row_btn.operator('portal.build_rig')

        
        

        row_test = layout.row()
        row_test.operator("tele.test_lib")

        addon_updater_ops.update_notice_box_ui(self, ctx)

        

        

classes = [
    PORTAL_PT_main_panel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


# if __name__ == "__main__":
# unregister()
# register()
    


##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
