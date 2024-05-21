import bpy
from bpy.types import PropertyGroup
from bpy.props import CollectionProperty, IntProperty, StringProperty, BoolProperty, EnumProperty

VP_SPUS = {}

class VP_SPU(object):
    id : str
    brand : str
    source_codes = []
    category = []
    subclass = []
    add_date : str
    pub_date : str
    is_delete : bool
    title : str
    subtitle : str
    content : str
    unit : str
    shipping_price : str
    status : bool
    preview = ()



class VP_PG_SPU(PropertyGroup):
    id : IntProperty
    brand : StringProperty
    source_codes : CollectionProperty(type=bpy.types.Text) # type: ignore
    category : CollectionProperty(type=bpy.types.Text) # type: ignore
    subclass : CollectionProperty(type=bpy.types.Text) # type: ignore
    add_date : StringProperty
    pub_date : StringProperty
    is_delete : BoolProperty
    title : StringProperty
    subtitle : StringProperty
    content : StringProperty
    unit : StringProperty
    shipping_price : StringProperty
    status : BoolProperty
    preview : EnumProperty



def SPUS_Serializer(api_spus):
    # bpy.context.scene.vp_spus.clear()
    global VP_SPUS ## global function varible to update
    VP_SPUS = {}
    for spu in api_spus:
        vp_spu = VP_SPU()
        vp_spu.id = spu['id']
        vp_spu.brand = spu['brand']
        for sc in spu['source_codes']:            
            vp_spu.source_codes.append(sc)
            
        for cg in spu['category']:
            vp_spu.category.append(cg)
            
        # for scls in spu['subclass']:
            # vp_spu.subclass.append(scls)
            
        vp_spu.add_date = spu['add_date']
        vp_spu.pub_date = spu['pub_date']
        vp_spu.is_delete = spu['is_delete']
        vp_spu.title = spu['title']
        vp_spu.subtitle = spu['subtitle']
        vp_spu.content = spu['content']
        vp_spu.unit = spu['unit']
        vp_spu.shipping_price = spu['shipping_price']
        vp_spu.status = spu['status']

        VP_SPUS[str(vp_spu.id)] = vp_spu
        return VP_SPUS




# def register():

    # bpy.utils.register_class(VP_PG_SPU)
    # bpy.types.Scene.vp_spus = CollectionProperty(type=VP_PG_SPU)


# def unregister():
    # del bpy.types.Scene.vp_spus
    # bpy.utils.unregister_class(VP_PG_SPU)

