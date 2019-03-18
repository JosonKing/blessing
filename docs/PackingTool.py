#!/usr/bin/env python
# encoding: utf-8
'''
1、读取指定目录下的所有文件
2、正则匹配出需要的文件
3、复制到指定位置
'''
import os.path




# 遍历指定目录，显示目录下的所有文件名
def eachFile(filePath, allowFile = True):
    

    filesArray = []
    for dir in pathDir:
        child = os.path.join('%s\%s' % (filePath, dir))
        if os.path.isfile(child) and allowFile:
            # print(child)
            filesArray.append(dir)

        if os.path.isdir(child) and len(os.listdir(child)) > 0:
            # print(child)
            filesArray.append(dir)

            childfilesArray = eachFile(child, False)
            if len(childfilesArray) > 0:
                filesArray.append(childfilesArray)

    return filesArray

def filesTree(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        dir_indent = "|   " * (level-1) + "|-- "
        file_indent = "|   " * level + "|-- "
        if not level:
            print('.')
        else:
            print('{}{}'.format(dir_indent, os.path.basename(root)))
        for f in files:
            if level == 0:
                print('{}{}'.format(file_indent, f))
    


# 遍历出结果 返回文件的名字
# def readFile(filenames):
    # fopen = open(filenames, 'r', encoding='UTF-8')  # r 代表read
    # fileread = fopen.read()
    # fopen.close()
    #
    # print("匹配到的文件是:"+fileread)
    # filesArray.append(fileread)


if __name__ == "__main__":
    # filePath = 'D:\\dev\\github\\antd-admin\\src\\components'  # refer root dir
    # eachFile(filenames)
    # for i in filesArray:
    #     print(i)
    # filesArray = []
    filePath = input("请输入文件所在路径：")
    while True:
        if os.path.exists(filePath):
            break
        else:
            filePath = input("该目录不存在，请重新输入：")
    
    filesTree(filePath)  # refer root dir

    print('\n已选择文件：')

    action = input("\n请选择操作：(a: 添加， r: 移除， all: 添加所有， #: 完成")

    while True:
        if action == 'all':
            print('all')
        else if action == 'a':
            fileName = input("请输入要添加的文件夹名称：")
            print(fileName)
        else if action == 'r':
            fileName = input("请输入要添加的文件夹名称：")
            print(fileName)
        else if action == '#':
            break

    


    # filesArray = eachFile(filePath)
    # for i in filesArray:
    #     print(i)