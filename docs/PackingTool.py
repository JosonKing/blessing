#!/usr/bin/env python
# encoding: utf-8
'''
1、读取指定目录下的所有文件
2、正则匹配出需要的文件
3、复制到指定位置
'''
import os.path


# 遍历指定目录，显示目录下的所有文件名
def eachFile(filePath):
    arr = []
    pathDir = os.listdir(filePath)
    for dir in pathDir:
        print(dir)
        arr.append(dir)

        child = os.path.join('%s\%s' % (filePath, dir))
        print(child)
        if os.path.isdir(child):
            return eachFile(child)

    return arr


# 遍历出结果 返回文件的名字
# def readFile(filenames):
    # fopen = open(filenames, 'r', encoding='UTF-8')  # r 代表read
    # fileread = fopen.read()
    # fopen.close()
    #
    # print("匹配到的文件是:"+fileread)
    # arr.append(fileread)


if __name__ == "__main__":
    filePath = 'E:\\code\\github\\antd-admin\\src\\components'  # refer root dir
    # eachFile(filenames)
    # for i in arr:
    #     print(i)

    arr = eachFile(filePath)
    print('all dir:')
    for i in arr:
        print(i)