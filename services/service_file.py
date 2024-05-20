import os
import json
import bpy
# import view.menu

# _file_dir = r'E:\\ProgramData\\Blender\\addon_dev\\mocap'
# _file_name = 'data.csv'
# _file_path = os.path.join(_file_dir, _file_name)
# # _file_dir = os.path.dirname(_file_path)


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__

class fileTool:

    @staticmethod
    def read_file(file_path:str):
        with open(file_path, 'r', encoding='utf-8') as byte:
            data = byte.read()
        return data

    @staticmethod
    def readline_file(file_path:str, line_idx:int):
        with open(file_path, 'r', encoding='utf-8') as byte:
            for i in range(line_idx):            
                data = byte.readline()
        return data

    @staticmethod
    def readjson_file(file_path:str):
        with open(file_path, 'r', encoding='utf-8') as byte:
            data = json.load(byte)
        return data

    @staticmethod
    def readjson_string(json_obj:json):
        python_obj = json.loads(json_obj)
        return python_obj

    @staticmethod
    def writejson_file(python_obj:object, file_path:str):
        with open(file_path, 'w', encoding='utf-8') as byte:
            json.dump(python_obj, byte, indent=4)

    @staticmethod
    def writejson_string(python_obj:object,separators=(',',':')):    
        json_obj = json.dumps(python_obj,separators=separators)
        return json_obj
    
    @staticmethod
    def bpy_obj_writejson_string(bpy_obj:bpy.types.Object):
        json_obj = json.dumps(bpy_obj)
        return json_obj

    @staticmethod
    def encoder_writejson_string(python_obj:object, cls=MyJSONEncoder):
        json_obj = json.dumps(python_obj,cls=cls)
        return json_obj

    @staticmethod
    def bpy_obj_encoder_writejson_string(bpy_obj:bpy.types.Object, cls=MyJSONEncoder):
        json_obj = json.dumps(bpy_obj, cls=cls)
        return json_obj

    @staticmethod
    def is_blendfile_saved():
        is_save = bpy.data.is_saved
        return is_save
    

    @staticmethod
    def blendfile_load(filepath:str):
        bpy.ops.wm.read_homefile(filepath=filepath)


    @staticmethod
    def blendfile_save(filepath:str ,check_existing=True, relative_remap=True):
        bpy.ops.wm.save_mainfile(filepath,check_existing, relative_remap)

    
    @staticmethod
    def get_blendfile_path():
        if fileTool.is_blendfile_saved() == False:
            msg = "No file path since blend file not saved yet."
            print(msg)
            # view.menu.msgbox(title='Error', icon='ERROR', line=msg)
            return False

        filepath = bpy.data.filepath
        return filepath
    

    @staticmethod
    def get_blendfile_dir():
        if fileTool.is_blendfile_saved() == False:
            msg = "No file path since blend file not saved yet."
            print(msg)
            # view.menu.msgbox(title='Error', icon='ERROR', line=msg)
            return False
        
        dir = bpy.path.abspath('//')
        return dir


    @staticmethod
    def run_py_external(file_path:str):
        # file_path = "/full/path/to/myscript.py"    
        exec(compile(open(file_path).read(), file_path, 'exec'))
        
    @staticmethod
    def run_py_relative(full_file_name:str):
        # import bpy
        # filepath = bpy.path.abspath("//myscript.py")
        file_path = bpy.path.abspath(f"//{full_file_name}")
        exec(compile(open(file_path).read(), file_path, 'exec'))

    @staticmethod
    def run_py_internal(text_name):
        bpy.data.texts[text_name].as_module()
    