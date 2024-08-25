

import bpy

def set_image(image_editor, img):
    '''
    <mode>   
    VIEW:View--View the image.
    UV:UV Editor--UV edit in mesh editmode.
    PAINT:Paint--2D image painting mode.
    MASK:Mask--Mask editing.    
    '''
    image_editor.image = img
    image_editor.mode = 'VIEW'


def set_text(text_editor, string):
    
    ## create text
    filename = "mynewfile.txt"
    if filename not in bpy.data.texts:
       bpy.data.texts.new(filename)
    text = bpy.data.texts[filename]    
    
    ## write text
    text.clear()
    text.write(string + "\n")
#    text.write(string + "\n")
#    text.write(string + "\n")
#    text.write("def funcction():")

    ## load text
    text_editor.text = text     

    ## replace text
#    text_editor.find_text = 'world'
#    text_editor.replace_text = 'sky'
#    bpy.ops.text.replace(all=True)

    # set editor
    text_editor.show_line_numbers = True
    text_editor.show_word_wrap = True
    text_editor.show_syntax_highlight = True
    text_editor.font_size = 20 
    
    ## scroll editor
    text_editor.top = 0  #  line number to scroll to
    
    

def create_window(type:str,x:int,y:int,**kwargs):
    # Modify render settings
    render = bpy.context.scene.render
    res_x = render.resolution_x
    res_y = render.resolution_y
    render.resolution_x = x
    render.resolution_y = y
    #render.resolution_percentage = 100

    # Modify preferences (to guaranty new window)
    prefs = bpy.context.preferences
    dirty_value = prefs.is_dirty
    prefs.view.render_display_type = "WINDOW"

    # Call image editor window
    bpy.ops.render.view_show("INVOKE_DEFAULT")

    # Change area type
    area = bpy.context.window_manager.windows[-1].screen.areas[0]
    area.type = type
    #area.header_text_set(None)
    #area.type = "TEXT_EDITOR"    
    #area.type = 'GRAPH_EDITOR'
    #area.type = 'VIEW_3D'
    #area.type = "CONSOLE"
    

    if type == 'IMAGE_EDITOR' and 'image' in kwargs.keys(): 
        set_image(area.spaces[0], kwargs['image'])
    
    if type == 'TEXT_EDITOR' and 'string' in kwargs.keys():
        set_text(area.spaces[0], kwargs['string'])
    
        
    # Restore render settings and preferences
    render.resolution_x = res_x
    render.resolution_y = res_y
    # ...

    # I also restore is_dirty tag which affects preferences autosave feature
    prefs.is_dirty = dirty_value


if __name__ == '__main__':
    '''
    bl_space_type:

    <General>
    VIEW_3D - 3D Viewport area
    IMAGE_EDITOR - UV/Image Editor area
    NODE_EDITOR - Node Editor area
    SEQUENCE_EDITOR - Video Sequencer area
    CLIP_EDITOR - Movie Clip Editor area

    <Animation>
    DOPESHEET_EDITOR - Dope Sheet area
    GRAPH_EDITOR - Graph Editor area
    NLA_EDITOR - Nonlinear Animation area

    <Scripting>
    TEXT_EDITOR - Text Editor area
    INFO
    CONSOLE
    TOPBAR
    STATUSBAR

    <data>
    OUTLINER
    PROPERTIES - Properties area
    FILE_BROWSER - File Browser area
    SPREADSHEET - Spreadsheet area
    PREFERENCES
    '''
#    img = bpy.data.images.load(img_path)
#    img = bpy.data.images['portal_logo.png']
#    create_window('IMAGE_EDITOR', 640, 480, image=img,)
    
    
    string = "hello world"
#    string = "中文测试"
    create_window('TEXT_EDITOR', 640, 480, string=string,)