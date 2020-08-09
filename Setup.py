# -*- coding:utf-8 -*-
"""
**************************************************************************************************
Project Name:编程猫社区(shequ.codemao.cn)操作类
Version:1.9.0
Author:wojiaoyishang
Email:422880152@qq.com
如果你调用class中有任何疑问或建议，请通过邮箱发送给我，邮箱的主题
请以 “ #编程猫社区操作类# ” 开头并在后面跟上你的问题，如：#编程猫社区操作类# 我发现了一个BUG。

版本说明：目前版本仅支持论坛的操纵与一些基本的个人信息操纵。
**************************************************************************************************
"""
import os, sys, shutil


if __name__ == '__main__':
    my_dir = sys.executable
    my_dir = my_dir[:my_dir.rfind(os.sep)] + os.sep
    lib_dir = my_dir + 'lib' + os.sep
    print(f"Python.exe运行目录：\"{my_dir}\"\nlib目录：\"{lib_dir}\"")
    if os.path.exists("CodemaoShequAPIs.py") == False:
        print("缺少 CodemaoShequAPIs.py 操作终止！无法安装！")
        exit()
    else:
        try:
            if os.path.exists(lib_dir + "CodemaoShequAPIs.py"):
                os.remove(lib_dir + "CodemaoShequAPIs.py")
            shutil.copy(os.path.realpath("CodemaoShequAPIs.py"), lib_dir + "CodemaoShequAPIs.py")
            os.rename("CodemaoShequAPIs.py", "CodemaoShequAPIs.py")
            print("操作成功！正在检测是否有效！")
            try:
                exec("import CodemaoShequAPIs")
            except:
                print("文件复制是成功的，但是无法正常使用！请重试！")
                os.rename("CodemaoShequAPIs.py", "CodemaoShequAPIs.py")
                exit()
            os.rename("CodemaoShequAPIs.py", "CodemaoShequAPIs.py")
            print("安装成功了！")
        except BaseException as error:
            print("操作失败！原因：",str(error))
