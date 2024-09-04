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