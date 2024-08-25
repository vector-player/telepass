import os
import bpy
import requests
# addon_name = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
# root_path = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
# img_dir = os.path.join(root_path,'images')

python_modules = [
    {  'install_name':'requests',  'check_installed_name':'request', },
    {  'install_name':'rpyc',  'check_installed_name':'rpyc', },
    {  'install_name':'pywebview',  'check_installed_name':'webview', },
]
root_dir = os.path.realpath("./")
addon_name = os.path.basename(root_dir)
img_dir = os.path.realpath("./images/")
portal_domain =  "https://telepass.app" # "https://telepass.app"  # "http://127.0.0.1:8000"  #
portal_spu = f"{portal_domain}/spu"
portal_market_addons = {}
portal_market_addons_url = f"{portal_domain}/shop_plus/market.json"
portal_user_addons = {}
portal_user_addons_url = f"{portal_domain}/api-auth/login/" 
portal_user_source_codes = f"{portal_domain}/shop_plus/user/source_codes/"
portal_test_source_codes = f"{portal_domain}/shop_plus/test/source_codes/"
session_obj = requests.session()
portal_sku_detail_image_list = []
portal_sku_detail_image_dict = {}
# print("root_path:",root_path)



