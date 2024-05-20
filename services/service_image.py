import urllib.request  
import urllib.parse
import re  
import os,sys,time,json,time
import socket,random,hashlib
import requests,configparser
import json
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
from .. import settings

def parse_image_from_text_re(html):

    img_list = []
    settings.portal_sku_detail_image_dict = {}
    i = 0
    img_urls = re.findall('img src="(.*?)"',html,re.S)
    for key in img_urls:
        print(key + "\r\n")
        img_url = settings.portal_domain + key
        print(img_url)
        img_list.append(img_url)
        img_name = os.path.basename(img_url) 
        img = {
            'url' : img_url,
            'name' : img_name,
        }
        settings.portal_sku_detail_image_dict[str(i)] = img
        i = i + 1
    return img_list

def getpicurl(url):
    # url = "http://www.mzitu.com/zipai/comment-page-352"
    html = requests.get(url).text
    pic_url = re.findall('img src="(.*?)"',html,re.S)
    for key in pic_url:
        print(key + "\r\n")
    #print(pic_url)

## Use Case    
# getpicurl("http://www.mzitu.com/zipai/comment-pag.e-352")




def open_url(url):
    req = urllib.request.Request(url)
    # add header in requesst to disguise web browser
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 '
                   'Safari/537.36 SE 2.X MetaSr 1.0')
    # get web-page data
    page = urllib.request.urlopen(req)
    # decode page data
    html_text = page.read().decode('utf-8')
 
    return html_text
 
 
def parse_image_from_text(html_text):
    # html_text = html_text.encode('utf-8')
    print("parsing html text:", html_text)
    # [^"]+\.jpg 匹配除"以外的所有字符多次,后面跟上转义的.和png
    # p = r'(http.:[\S]*?.(jpg|jpeg|png|gif|bmp|webp))'
    # p = '\/\(\?<=\(img\[\^>\]\*src="\)\)\[\^"\]\*\/g'
    # p = r'/<img[^>]+src=\"?([^\"\\s]+)\"?[^>]*>/g'
    p = '\/<img\[\^>\]\+src=\\"\?\(\[\^\\"\\\\s\]\+\)\\"\?\[\^>\]\*>\/g'

    # 返回正则表达式在字符串中所有匹配结果的列表
    imglist = re.findall(p, html_text)
    print("List of Img: " + str(imglist))
    return imglist

def get_img(imglist):
    # 循环遍历列表的每一个值
    for img in imglist:
        # 以/为分隔符，-1返回最后一个值
        filename = img[0].split("/")[-1]
        # 访问each，并将页面的二进制数据赋值给photo
        photo = urllib.request.urlopen(img[0])
        w = photo.read()
        # 打开指定文件，并允许写入二进制数据
        f = open('D:/test/' + filename, 'wb')
        # 写入获取的数据
        f.write(w)
        # 关闭文件
        f.close()
        print(filename + " have been download...")
 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

newline = []
def save_image(url, save_path, filename):
    response = urllib.request.get(url)
    response.raise_for_status()
    with open(os.path.join(save_path, filename), 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def parse_image_from_file():
    # import os
    from bs4 import BeautifulSoup
    from lxml import etree
    
    html_path = "D:\\mg"
    for root, dirs, files in os.walk(html_path):
        for file in files:
            htmlfile = os.path.join(root, file)
            if "html" in htmlfile:
                parser = etree.HTMLParser()
                html = etree.parse(htmlfile, parser=parser)
                html_txt = etree.tostring(html, encoding="utf-8")
                info = html_txt.decode("utf-8")
                soup = BeautifulSoup(info, "html.parser")
                div_tags = soup.find_all("div", class_="col-md-4 col-sm-4 col-xs-6 pro-list")
                if div_tags != []:
                    for div in div_tags:
                        img_src = div.find_all("img", src=True)
                        for img in img_src:
                            imginfo = img["src"]
                            newline.append(imginfo)
                else:
                    div_tags = soup.find_all("div", class_="scale")
                    for div in div_tags:
                        img_src = div.find_all("img", src=True)
                        for img in img_src:
                            imginfo = img["src"]
                            newline.append(imginfo)



# 该模块既可以导入到别的模块中使用，另外该模块也可自我执行
if __name__ == '__main__':
    # 定义url
    url = "https://movie.douban.com/top250"
    # 将url作为open_url()的参数，然后将open_url()的返回值作为参数赋给get_img()
    get_img(parse_img_path(open_url(url)))
    print("all over...")