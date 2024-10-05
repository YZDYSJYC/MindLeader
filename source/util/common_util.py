# coding=utf-8
# 作者: 拓跋龙
# 功能: 公共接口

import sys
import tarfile
from PIL import Image

def tar_file(src_file: str, dst_file: str):
    with tarfile.open(dst_file, "w:gz") as tar:
        tar.add(src_file)

def img_to_icon(png_path, ico_path):    
    # 转换图像
    img = Image.open(png_path)
    img.save(ico_path)

def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000

# 设置超链接
def get_hyper_link(url: str, url_name: str=None) -> str:
    if not url_name:
        url_name = url
    return f"<a href='{url}' style='color: skyblue;font-size:16px;font-family:Microsoft YaHei'><b>{url_name}</b></a>"
