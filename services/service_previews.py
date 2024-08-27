import requests
import os
import bpy
from .. import settings
from .._types import sku_spu
from bpy.props import EnumProperty
import bpy.utils.previews
from .service_image import parse_image_from_text_re




#++++++++++++++++++++++++++++++++++++++++++++

img_dir = settings.img_dir
previews = {}
previews['global'] = bpy.utils.previews.new()
previews['market_sku'] = bpy.utils.previews.new()
previews['user_sku'] = bpy.utils.previews.new()
previews['load_image_list'] = bpy.utils.previews.new()
previews['load_image_dict'] = bpy.utils.previews.new()



def has_img(img_name):    
    img_path = os.path.join(img_dir, img_name)
    return os.path.exists(img_path)

def get_img_path(img_name):
    return os.path.join(img_dir, img_name)

def get_img_name_from_url(img_url):
    # img_name = os.path.basename(img_url)
    ## Considering 3rd-party objects storages path with concating signiture arguments,
    ## which start with '?' and should be removed while retrieving clean file name.
    img_name = os.path.basename(img_url.split('?')[0]) 
    return img_name


def new_image_texture(name:str, img:bpy.types.Image, ext:str='CLIP'):
    texture = bpy.data.textures.new(name=name, type="IMAGE")
    texture.image = img
    texture.extension = ext #EXTEND # CLIP # CLIP_CUBE # REPEAT # CHECKER

def download_img(img_url, img_name:str='default'):

    # headers for faking browser behaviours
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0;Win64;x64)AppleWebKit/537.36 (KHTML,like Gecko)Chrome/58.0.3'
    }
    # url = img_url
    # response = requests.get(url,headers=headers)

    # img_urls = ['https://www.example.com/imagel.jpg','https://www.example.com/image2.jpg']

  
    if not os.path.exists(img_dir):
        # print("Create image dir for previews.")
        os.makedirs(img_dir)

    # for img_url in img_urls:
        
    response = requests.get(img_url,headers=headers)
    #获取文件名
    if img_name == 'default':
        img_name = get_img_name_from_url(img_url)
    # print("Image name:", img_name)

    img_path = os.path.join(img_dir, img_name)
    with open(img_path,'wb') as f:
        # print("Downloading image for previews.")
        f.write(response.content)
    return img_path


def pcoll_from_local(img_path):    
    
    # global pcoll

    ## new preview
    # pcoll = previews['global']    
    # bpy.utils.previews.remove(pcoll)
    # previews['global'] = bpy.utils.previews.new()

    # pcoll = previews['global']
    # previews['local'] = bpy.utils.previews.new()
    pcoll = previews['local']

    # img_name = os.path.basename(img_path)
    (img_dir, img_name) = os.path.split(img_path)
    icon = pcoll.get(img_name)
    if not icon:
        thumb = pcoll.load(img_name, img_path, 'IMAGE')  
    else:
        thumb = pcoll[img_name]
    
    # bpy.utils.previews.remove(pcoll) # try to eliminate WARNING of 'previews left open'

    return thumb.icon_id


def pcoll_from_sku_spus(sku_spus):

    # global pcoll

    ## new preview
    # pcoll = previews['market_sku']    
    # bpy.utils.previews.remove(pcoll)
    # previews['market_sku'] = bpy.utils.previews.new()

    pcoll = previews['market_sku']

    for sku_spu in sku_spus:
        img_url = sku_spu.img
        # img_name = os.path.basename(img_url) 
        img_name = get_img_name_from_url(img_url)

        ## Download image if not LOCAL      
        # print("读取image url:",img_url)
        if not has_img(img_name):
            download_img(img_url, 'default')
        img_path = get_img_path(img_name)

        ## Create new thumb in not EXIST
        icon = pcoll.get(img_name)
        if not icon:
            pcoll.load(img_name, img_path, 'IMAGE')  
    return pcoll


def enum_from_pcoll(pcoll):
    enum_items = []
    for i,icon in enumerate(pcoll):
        enum_items.append(
            (
                str(i),             ## id
                str(i),             ## name
                "",                 ## description
                icon.icon_id,       ## icon
                i,                  ## index
            )
        )
    return enum_items

## portal_sku_detail_previews.items (Plan A)
def load_image_list(self, ctx):
    # previews['load_image_list'] = bpy.utils.previews.new()
    pcoll = previews['load_image_list']

    enum_items = []
    from .. import settings
    image_list = settings.portal_sku_detail_image_list
    for i,img_url in enumerate(image_list):
        # print("image list enum index:",i, "item:", img_url)

        # img_name = os.path.basename(img_url) 
        # img_url = img['url'] 
        img_name = get_img_name_from_url(img_url)
        # print("load_image_list:img_url:",img_url)
        # print("load_image_list:img_name:",img_name)
        
        

        ## Download image if not LOCAL      
        # print("image url:",img_url)
        if not has_img(img_name):
            # download_img(img_url, 'default')
            download_img(img_url, img_name)
        img_path = get_img_path(img_name)

        ## Create new thumb in not EXIST
        icon = pcoll.get(img_name)
        if not icon:
            thumb = pcoll.load(img_name, img_path, 'IMAGE')  
        else:
            thumb = pcoll[img_name]

        ## Format thumb to Enumerator to feed UI
        enum_items.append((str(i), img_name, img_url, thumb.icon_id, i))

    # print("load_image_list: market enum_items:",len(enum_items))
    bpy.context.view_layer.update()
    bpy.context.area.tag_redraw()
    # bpy.utils.previews.remove(pcoll) # try to eliminate WARNING of 'previews left open'
    return enum_items

## ## portal_sku_detail_previews.items (Plan B)
## use for sub-window, to lookup image name to embed image into sub-window by selected index.
def load_image_dict(self, ctx):    
    # previews['load_image_dict'] = bpy.utils.previews.new()
    pcoll = previews['load_image_dict']
    enum_items = []
    
    from .. import settings
    image_dict = settings.portal_sku_detail_image_dict
    print("len(image_dict.keys()):", len(image_dict.keys()))
    # if len(image_dict.keys()) == 0: 
    #     return None
    for i in range(len(image_dict.keys())):
    # for i,img in enumerate(image_dict):
        
        print("load_image_dict:", i)
        img = image_dict[str(i)]
        img_name = img['name']  
        img_url = img['url'] 
        # print("img_url",img_url)
        # print("image list enum index:",i + 1, "item:", img_url)
        ## Download image if not LOCAL      
        # print("image url:",img_url)
        if not has_img(img_name):
            download_img(img_url, 'default')
        img_path = get_img_path(img_name)
        img.update({'path' : img_path})
        ## Create new thumb in not EXIST
        icon = pcoll.get(img_name)
        if not icon:
            thumb = pcoll.load(img_name, img_path, 'IMAGE')  
        else:
            thumb = pcoll[img_name]

        ## Format thumb to Enumerator to feed UI
        ## Since 'i' is for enum assignment, it should start with '1'(i + 1), not '0',        
        enum_items.append((str(i + 1), img_name, img_url, thumb.icon_id, i + 1))

    print("load_image_dict: market enum_items:",len(enum_items))
    bpy.context.view_layer.update()
    bpy.context.area.tag_redraw()
    # bpy.utils.previews.remove(pcoll) # try to eliminate WARNING of 'previews left open'
    return enum_items

## portal_sku_market_previews.items
def load_previews_market_sku(self, ctx):
    ## prepare enumproperty for ui
    enum_items = []
    # global pcoll
    pcoll = previews['market_sku']
    # print("pcoll type:", type(pcoll))
    # for portal_sku_spu in bpy.context.scene.portal_sku_spus:
    # print("PORTAL_SKU_SPUS:",len(PORTAL_SKU_SPUS))
    for portal_sku_spu in settings.portal_market_addons.values():
        img_url = portal_sku_spu.img
        # img_name = str(portal_sku_spu.id)
        # img_name = os.path.basename(img_url)  
        # img_name = get_img_name_from_url(img_url)
        img_name = f"{portal_sku_spu.spu.title}_{portal_sku_spu.title}" 

        ## Download image if not LOCAL      
        # print("image url:",img_url)
        if not has_img(img_name):
            # download_img(img_url, 'default')
            download_img(img_url, img_name)
        img_path = get_img_path(img_name)

        ## Create new thumb in not EXIST
        icon = pcoll.get(img_name)
        if not icon:
            thumb = pcoll.load(img_name, img_path, 'IMAGE')  
        else:
            thumb = pcoll[img_name]

        ## Format thumb to Enumerator to feed UI
        ## [(identifier, name, description, icon, number), ...]
        enum_items.append((str(portal_sku_spu.id), f"{portal_sku_spu.spu.title}_{portal_sku_spu.title}", portal_sku_spu.spu.content, thumb.icon_id, portal_sku_spu.id ))  # portal_sku_spu.id

    # print("Preview INFO: market enum_items:",len(enum_items))
    # ctx.view_layer.update()
    # ctx.area.tag_redraw()
    # bpy.utils.previews.remove(pcoll) # try to eliminate WARNING of 'previews left open'
    return enum_items

## portal_sku_user_previews.items
def load_previews_user_sku(self, ctx):
    ## prepare enumproperty for ui
    enum_items = []
    # global pcoll
    pcoll = previews['user_sku']
    # print("pcoll type:", type(pcoll))
    # for portal_sku_spu in bpy.context.scene.portal_sku_spus:
    # print("PORTAL_SKU_SPUS:",len(PORTAL_SKU_SPUS))
    for portal_sku_spu in settings.portal_user_addons.values():
        img_url = portal_sku_spu.img
        # img_name = str(portal_sku_spu.id)
        # img_name = os.path.basename(img_url)  
        # img_name = get_img_name_from_url(img_url)
        img_name = f"{portal_sku_spu.spu.title}_{portal_sku_spu.title}" 

        ## Download image if not LOCAL      
        # print("image url:",img_url)
        if not has_img(img_name):
            # download_img(img_url, 'default')
            download_img(img_url, img_name)
        img_path = get_img_path(img_name)

        ## Create new thumb if not EXIST
        icon = pcoll.get(img_name)
        if not icon:
            thumb = pcoll.load(img_name, img_path, 'IMAGE')  
        else:
            thumb = pcoll[img_name]

        ## Format thumb to Enumerator to feed UI
        enum_items.append((str(portal_sku_spu.id), portal_sku_spu.spu.title, portal_sku_spu.spu.content, thumb.icon_id, portal_sku_spu.id ))

        ## Preview Window show has_content.png
        # ctx.scene.portal_sku_user_previews = "has_content.png"
    ## add images for cover
    # enum_items.append(('has_content', 'has_content', 'has_content', 'COLORSET_04_VEC', 99999 ))  
    # enum_items.append(('no_content', 'no_content', 'no_content', 'COLORSET_10_VEC', 0 ))  
    # set_preview(self, 99999)
    # print("Preview INFO: user enum_items:",len(enum_items))
    # bpy.context.view_layer.update()
    # bpy.context.area.tag_redraw()
    # bpy.utils.previews.remove(pcoll) # try to eliminate WARNING of 'previews left open'
    return enum_items

def update_button(ctx, id):
    print("seletcted id status:",settings.portal_market_addons[id].status)
    sku = settings.portal_market_addons[id]
    if sku.status == 'test' :   # and 'Addons' in sku.spu.category
        ctx.scene.portal_active_addon_status = 'On/Off'
    else:
        ctx.scene.portal_active_addon_status = 'Subscribe'


def update_detail_preview(ctx):
    ## handle preview images   
    atlas_url_list = []
    try:
        if ctx.scene.portal_tab == 'market':
            id = ctx.scene.portal_active_market_addon_id
            if id == '' or id is None: 
                string = ""
            # elif int(id) > len(settings.portal_market_addons.keys()): 
            #     string = ""
            # print("total market addons:", len(settings.portal_market_addons))
            else:
                string = settings.portal_market_addons[id].spu.content
                atlas = settings.portal_market_addons[id].atlas                
                for item in atlas:
                    atlas_url_list.append(item['img'])
                    

        if ctx.scene.portal_tab == 'my':
            id = ctx.scene.portal_active_user_addon_id
            if id == '' or id is None: 
                string = ""
            # elif int(id) > len(settings.portal_user_addons.keys()): 
            #     print('addon id:', str(id), ' > user addons count:',len(settings.portal_user_addons.keys()))
            #     string = ""
            else:
                string = settings.portal_user_addons[id].spu.content 
                atlas = settings.portal_user_addons[id].atlas
                for item in atlas:
                    atlas_url_list.append(item['img'])

    except Exception as e:
        print("Error on preview update: something wrong with spu content.")
        print("update_detail_preview:",e)
        string = ""
    # imglist = parse_image_from_text(self.string)  、
    ## Add <img> elements embeded in html content  
    imglist = parse_image_from_text_re(string) 
    ## Add images from atlas    
    imglist += atlas_url_list
    print("imglist:",[img for img in imglist])
    settings.portal_sku_detail_image_list = imglist
    load_image_list(ctx.scene, ctx)
    # load_image_dict(ctx.scene, ctx)

## portal_sku_market_previews.update
def on_select_market_preview(self, ctx):
    id = self.portal_sku_market_previews
    ctx.scene.portal_active_market_addon_id = id
    update_button(ctx,id)
    update_detail_preview(ctx)
    print('selected preview icon:',id)
    sku = settings.portal_market_addons[str(id)]
    print("selected product title:", f"{sku.spu.title}_{sku.title}")

## portal_sku_user_previews.update
def on_select_user_preview(self, ctx):
    id = self.portal_sku_user_previews
    ctx.scene.portal_active_user_addon_id = id
    update_detail_preview(ctx)
    print('selected preview icon:',id)
    sku = settings.portal_user_addons[str(id)]
    print("test serialize:", f"{sku.spu.title}_{sku.title}")

## portal_sku_detail_previews.update
def on_select_detail_preview(self, ctx):
    id = self.portal_sku_detail_previews
    # ctx.scene.portal_active_sku_detail_id = id
    print('selected preview icon:',id)
    # print("test serialize:", settings.portal_user_addons[str(id)].spu.title)
    from ..services.service_subwindow import create_window
    img_path = settings.portal_sku_detail_image_dict[str(id)]['path']
    img = bpy.data.images.load(img_path)
    create_window('IMAGE_EDITOR', 640, 480, image=img)



def set_preview(self, value:int):
    print("setting value", value)

def get_preview(self):
    import random
    # return random.randint(1, 4)
    return 1


def register():

    ## Setting items with function other than static enums, is good for dynamicly checking images,
    ## but such function would be invoked again and again since UI keep examinating EnumProperty items frequently. 
    ## So that calling 'set=' function within load-items-function might not run collectly.
    bpy.types.Scene.portal_sku_market_previews = EnumProperty( items=load_previews_market_sku, update=on_select_market_preview,  ) 
    bpy.types.Scene.portal_sku_user_previews = EnumProperty( items=load_previews_user_sku, update=on_select_user_preview,  )  ## items=load_previews_sku, set=set_preview,  ## get=get_preview
    bpy.types.Scene.portal_sku_detail_previews = EnumProperty( items=load_image_list, update=on_select_detail_preview, ) 

def unregister():
    del bpy.types.Scene.portal_sku_user_previews
    del bpy.types.Scene.portal_sku_market_previews
    del bpy.types.Scene.portal_sku_detail_previews
