import bpy
import os
from bpy.types import PropertyGroup
from bpy.props import CollectionProperty, IntProperty, StringProperty, BoolProperty, EnumProperty
from . import spu
from ..services import service_previews,  global_variable

# global PORTAL_SKU_SPUS
# PORTAL_SKU_SPUS = {}

class PORTAL_SKU_SPU(object):
    id : int
    spu = {}
    add_date : str
    pub_date : str
    is_delete : bool
    img : str
    price : str
    cost_price : str
    discount_price : str
    stock : int
    sales : int
    code : str
    volume : str
    weight : str
    specs = []

class PORTAL_PG_SKU_SPU(PropertyGroup):
    id : IntProperty()
    spu : CollectionProperty(type=spu.VP_PG_SPU)    
    add_date : StringProperty()
    pub_date : StringProperty()
    is_delete : BoolProperty()
    img : StringProperty()
    price : StringProperty()
    cost_price : StringProperty()
    discount_price : StringProperty()
    stock : IntProperty()
    sales : IntProperty()
    code : StringProperty()
    volume : StringProperty()
    weight : StringProperty()
    specs : CollectionProperty(type=bpy.types.Text)
    


def SKU_SPU_Serializer(api_sku_spus):
    # bpy.context.scene.portal_sku_spus.clear() 
    # global PORTAL_SKU_SPUS
    PORTAL_SKU_SPUS = {}   
    for api in api_sku_spus:
        # portal_sku_spu = bpy.context.scene.portal_sku_spus.add()
        portal_sku_spu = PORTAL_SKU_SPU()

        portal_sku_spu.id = api['id']
        portal_sku_spu.spu = spu.SPUS_Serializer([api['spu'],])[str(api['id'])]
        portal_sku_spu.add_date = api['add_date']
        portal_sku_spu.pub_date = api['pub_date']
        portal_sku_spu.is_delete = api['is_delete']
        portal_sku_spu.img = api['img']
        portal_sku_spu.price = api['price']
        portal_sku_spu.cost_price = api['cost_price']
        portal_sku_spu.discount_price = api['discount_price']
        portal_sku_spu.stock = api['stock']
        portal_sku_spu.sales = api['sales']
        portal_sku_spu.code = api['code']
        portal_sku_spu.volume = api['volume']
        portal_sku_spu.weight = api['weight']
        portal_sku_spu.specs = api['specs']

        PORTAL_SKU_SPUS[str(portal_sku_spu.id)] = portal_sku_spu
        # print("共序列化SKU数量:",len(PORTAL_SKU_SPUS))
    return PORTAL_SKU_SPUS
    


