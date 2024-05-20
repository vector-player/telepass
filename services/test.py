import rpyc
# import bpy
# import views.main_panel


def main():
    global bpy
    cn = rpyc.connect('localhost',18861)
    # if cn:
    bpy = cn.root.bpy
    
    ## test single-line command
    obj = bpy.context.view_layer.objects.active
    obj.data.vertices[0].co.y=20

    ## test creating UI

    class new_panel(bpy.types.Panel):
        bl_idname = "panelname"
        bl_label = "Panelname"
        bl_space_type = "VIEW_3D"
        bl_region_type = "UI"
        bl_category = "category"

        def draw(self,ctx):
            layout = self.layout
            new_row = layout.row()
            new_row.label(test='New Row')

    classes = [
        new_panel
    ]

    def register():
        for cls in classes:
            bpy.utils.register_class(cls)

    def unregister():
        for cls in classes:
            bpy.utils.unregister_class(cls)

    register()



    # cn.disconnect()
    # cn.close()



if __name__ == "__main__":
    main()


#################################


        