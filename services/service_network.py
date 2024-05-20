
import json  # 用于处理 JSON 数据
import urllib.request  # 用于向公网IP地址查询 API 发送请求

def public_ip():

    # 获取公网出口IP地址
    url = "https://api.ipify.org/?format=json"  # 定义查询 API 的 URL
    try:
        response = urllib.request.urlopen(url)  # 向查询 API 发送请求并获取响应
        data = response.read()  # 读取响应中的数据（字节流）
        data = data.decode("utf-8")  # 将响应数据从字节流转换为字符串
        data = json.loads(data)  # 将响应数据解析为 JSON 格式
        public_ip = data["ip"]  # 从 JSON 数据中提取公网IP地址
        print("My Public IP：", public_ip)

    except:
        err_msg = "无法获取公网出口IP地址"     # 查询失败时输出提示信息
        print(err_msg)
        public_ip = ''

    return public_ip
