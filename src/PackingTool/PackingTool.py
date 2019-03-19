#!/usr/bin/env python
# encoding: utf-8

import os.path
import shutil
import re
from treelib import Node, Tree

'''
1、读取指定目录下的所有文件
2、正则匹配出需要的文件
3、复制到指定位置
'''

addedFilesArray = []
filePath = ''
pathTree = Tree()
pathTree.create_node("/", "id")

addFileTree = Tree()
addFileTree.create_node("/", "id")

# 遍历指定目录下所有文件，生成文件目录 pathTree
def handlePathFile(sourcePath, allowFile = True, parentKey = 'id'):
  fileDir = os.listdir(sourcePath)
  for index, dir in enumerate(fileDir):
    child = os.path.join('%s\%s' % (sourcePath, dir))
    if os.path.isfile(child) and allowFile:
      key = parentKey + (str(index) if index > 9 else '0' + str(index))
      pathTree.create_node(dir + '  ' + key, key, parentKey)

    if os.path.isdir(child) and len(os.listdir(child)) > 0:
      key = parentKey + (str(index) if index > 9 else '0' + str(index))
      pathTree.create_node(dir + '  ' + key, key, parentKey)

      handlePathFile(child, False, key)

# 根据key添加父节点
def createParentNode(key):
  parentKey = key[:-2]
  if addFileTree.contains(parentKey):
    addFileTree.create_node(pathTree.nodes[key].tag, key, parentKey)
  else:
    keyLen = len(key)
    curLen = 4
    while curLen < keyLen:
      if addFileTree.contains(key[:curLen]) and not addFileTree.contains(key[:curLen + 2]):
        addFileTree.create_node(pathTree.nodes[key[:curLen + 2]].tag, key[:curLen + 2], key[:curLen])


# 处理树结构数据
def handleTree(actionType, key):
  if actionType == 'add':
    if addFileTree.contains(parentKey):
      createParentNode(key)
      addFileTree.show()
    else:
      addFileTree.contains(key)

  elif actionType == 'rm':
    addFileTree.remove_node(key)



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

# 树状展示文件目录
def filesTree(startpath):
  levelCountArr = [1 for i in range(10)]
  for root, dirs, files in os.walk(startpath):
    level = root.replace(startpath, '').count(os.sep)
    dir_indent = "|   " * (level-1) + "|-- "
    file_indent = "|   " * level + "|-- "
    if not level:
      print('.')
    else:
      index = levelCountArr[level] if(levelCountArr[level] > 9) else '0' + str(levelCountArr[level])
      print('{}{}{}{}{}'.format(dir_indent, os.path.basename(root), ' ', level, index))
      print(levelCountArr)
      levelCountArr[level] = levelCountArr[level] + 1
    for f in files:
      if level == 0:
        print('{}{}{}{}'.format(file_indent, f, ' ', levelCountArr[level]))
        levelCountArr[level] = levelCountArr[level] + 1

# 根据指令处理文件
def handleAction(sourcePath, action):
  print('handleAction:' + sourcePath)
  while True:
    if action == 'addall':
      print('addall')
      addedFilesArray = handleFile(sourcePath, True)
      filesTree(filePath)
      print('\n已选文件：\n')
      print(addedFilesArray)
      action = input("\nadd: 添加， rm: 移除， addall: 添加所有， rmall:移除所有， #: 完成\n请选择操作：指令 文件/文件夹名称（add filename/rm filename)\n")
      print(action)
    elif action == 'rmall':
      print('rmall')
      addedFilesArray = []
      filesTree(filePath)
      print('\n已选文件：\n')
      print(addedFilesArray)
      action = input("\nadd: 添加， rm: 移除， addall: 添加所有， rmall:移除所有， #: 完成\n请选择操作：指令 文件/文件夹名称（add filename/rm filename)\n")
      print(action)
    elif str(action).startswith('add'):
      # add file
      key = str(action).replace('add ', '')
      handleTree('add', key)
      action = input("\nadd: 添加， rm: 移除， addall: 添加所有， rmall:移除所有， #: 完成\n请选择操作：指令 文件/文件夹名称（add filename/rm filename)\n")
      print(action)
    elif str(action).startswith('rm'):
      # rm file
      fileName = str(action).replace('rm ', '')
      handleActionFile(sourcePath, 'rm', fileName, True)
      action = input("\nadd: 添加， rm: 移除， addall: 添加所有， rmall:移除所有， #: 完成\n请选择操作：指令 文件/文件夹名称（add filename/rm filename)\n")
      print(action)
    elif action == '#':
      print('选择完毕，开始打包')
      break
    elif action == '*':
      print('您已取消打包并退出')
      break

# 根据指令处理文件
# def handleAction(sourcePath, action):
#   print('handleAction:' + sourcePath)
#   while True:
#     if action == 'addall':
#       print('addall')
#       addedFilesArray = handleFile(sourcePath, True)
#       filesTree(filePath)
#       print('\n已选文件：\n')
#       print(addedFilesArray)
#       action = input("\nadd: 添加， rm: 移除， addall: 添加所有， rmall:移除所有， #: 完成\n请选择操作：指令 文件/文件夹名称（add filename/rm filename)\n")
#       print(action)
#     elif action == 'rmall':
#       print('rmall')
#       addedFilesArray = []
#       filesTree(filePath)
#       print('\n已选文件：\n')
#       print(addedFilesArray)
#       action = input("\nadd: 添加， rm: 移除， addall: 添加所有， rmall:移除所有， #: 完成\n请选择操作：指令 文件/文件夹名称（add filename/rm filename)\n")
#       print(action)
#     elif str(action).startswith('add'):
#       # add file
#       fileName = str(action).replace('add ', '')
#       handleActionFile(sourcePath, 'add', fileName, True)
#       action = input("\nadd: 添加， rm: 移除， addall: 添加所有， rmall:移除所有， #: 完成\n请选择操作：指令 文件/文件夹名称（add filename/rm filename)\n")
#       print(action)
#     elif str(action).startswith('rm'):
#       # rm file
#       fileName = str(action).replace('rm ', '')
#       handleActionFile(sourcePath, 'rm', fileName, True)
#       action = input("\nadd: 添加， rm: 移除， addall: 添加所有， rmall:移除所有， #: 完成\n请选择操作：指令 文件/文件夹名称（add filename/rm filename)\n")
#       print(action)
#     elif action == '#':
#       print('选择完毕，开始打包')
#       break
#     elif action == '*':
#       print('您已取消打包并退出')
#       break

# 遍历指定目录，找出对应文件或者文件夹
def handleFile(sourcePath, allowFile = True):
  print('handleFile:' + sourcePath)
  fileDir = os.listdir(sourcePath)
  filesArray = []
  for dir in fileDir:
    child = os.path.join('%s\%s' % (sourcePath, dir))
    if os.path.isfile(child) and allowFile:
      print(dir)
      print(child)
      filesArray.append(dir)

    if os.path.isdir(child) and len(os.listdir(child)) > 0:
      print(dir)
      print(child)
      filesArray.append(dir)

      childfilesArray = handleFile(child, False)  
      if len(childfilesArray) > 0:
        filesArray.append(childfilesArray)

  return filesArray

# 遍历指定目录，找出对应文件或者文件夹，并作出对应操作
def handleActionFile(sourcePath, action, fileName, allowFile = True):
  fileDir = os.listdir(sourcePath)
  for dir in fileDir:
    # print(dir)
    child = os.path.join('%s\%s' % (sourcePath, dir))
    # print(child)
    
    if os.path.isfile(child) and allowFile:
      
      if(str(dir).lower() == str(fileName).lower()):
        if action == 'add':
          addedFilesArray.append(dir)
        elif action == 'rm':
          addedFilesArray.remove(dir)

        filesTree(filePath)
        print('已选文件\n')
        print(addedFilesArray)

    elif os.path.isdir(child) and len(os.listdir(child)) > 0:
      if(str(dir).lower() == str(fileName).lower()):
        if allowFile:
          if action == 'add':
            addedFilesArray.append(dir)
          elif action == 'rm':
            addedFilesArray.remove(dir)

          filesTree(filePath)
          print('已选文件\n')
          print(addedFilesArray)

        else:
          print('level not 1 rm')
          if action == 'add':
            addedFilesArray.append(dir)
          elif action == 'rm':
            addedFilesArray.remove(dir)

          filesTree(filePath)
          print('已选文件\n')
          print(addedFilesArray)

      else:
        handleActionFile(child, action, fileName, False)

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
  # E:\\code\\github\\antd-admin\\src\\components

  # 输入路径
  # filePath = input("请输入文件路径：")
  filePath = 'E:\\code\\github\\antd-admin\\src\\components'
  while True:
    if os.path.exists(filePath):
      break
    else:
      filePath = input("该目录不存在，请重新输入：")

  # # 查看文件  
  # filesTree(filePath)
  handlePathFile(filePath)
  pathTree.show()

  # 处理文件
  action = input("\nadd: 添加， rm: 移除， addall: 添加所有， rmall:移除所有， #: 完成\n请选择操作：指令 文件/文件夹名称（add filename/rm filename)\n")
  handleAction(filePath, action)


