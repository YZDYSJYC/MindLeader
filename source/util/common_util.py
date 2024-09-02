# coding=utf-8
# 作者: 拓跋龙
# 功能: 公共接口

import tarfile

def tar_file(src_file: str, dst_file: str):
    with tarfile.open(dst_file, "w:gz") as tar:
        tar.add(src_file)
