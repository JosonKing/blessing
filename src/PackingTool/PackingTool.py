#!/usr/bin/env python
# encoding: utf-8

import os.path
import shutil
import re
from treelib import Node, Tree

'''
1、读取指定目录下的所有文件
2、匹配出需要的文件
3、复制到指定位置
'''

addedFilesArray = []
filePath = ''
pathTree = Tree()
pathTree.create_node("/", "id")

addFileTree = Tree()
addFileTree.create_node("/", "id")

actionTip = "\n+------------------------------------------------------------------------------------------------------------------------------------------------------------------------+\n| add: 添加 | rm: 移除 | addall: 添加所有 | rmall:移除所有 | lsm:查看所有模块 | lss:查看已选模块 | lsa: 查看所有模块及已选模块 | done: 完成 | exit:取消 | help: 查看指令 |\n+------------------------------------------------------------------------------------------------------------------------------------------------------------------------+"
actionResponse = "[请选择操作]$ "

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

def addAll(sourcePath, allowFile = True, parentKey = 'id'):
  fileDir = os.listdir(sourcePath)
  for index, dir in enumerate(fileDir):
    child = os.path.join('%s\%s' % (sourcePath, dir))
    if os.path.isfile(child) and allowFile:
      key = parentKey + (str(index) if index > 9 else '0' + str(index))
      if not addFileTree.contains(key):
        addFileTree.create_node(dir + '  ' + key, key, parentKey)

    if os.path.isdir(child) and len(os.listdir(child)) > 0:
      key = parentKey + (str(index) if index > 9 else '0' + str(index))
      if not addFileTree.contains(key):
        addFileTree.create_node(dir + '  ' + key, key, parentKey)

      addAll(child, False, key)

def rmAll(sourcePath):
  fileDir = os.listdir(sourcePath)
  for index, dir in enumerate(fileDir):
    key = 'id' + (str(index) if index > 9 else '0' + str(index))
    if addFileTree.contains(key):
      addFileTree.remove_node(key)


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
    if not addFileTree.contains(key):
      print("该模块未选中，无需移除")
    else:
      addFileTree.remove_node(key)
      print("模块移除成功")

# 遍历指定目录，显示目录下的所有文件名
def eachFile(filePath, allowFile = True):
  filesArray = []
  for dir in pathDir:
    child = os.path.join('%s\%s' % (filePath, dir))
    if os.path.isfile(child) and allowFile:
      filesArray.append(dir)

    if os.path.isdir(child) and len(os.listdir(child)) > 0:
      filesArray.append(dir)

      childfilesArray = eachFile(child, False)
      if len(childfilesArray) > 0:
        filesArray.append(childfilesArray)

  return filesArray

# 根据指令处理文件
def handleAction(sourcePath, action):
  while True:
    if action == 'addall':
      rmAll(sourcePath)
      addAll(sourcePath, Tree, 'id')
      print("=> 所有模块添加成功\n")
      action = input(actionResponse)
    elif action == 'rmall':
      rmAll(sourcePath)
      print("=> 所有模块移除成功\n")
      action = input(actionResponse)
    elif str(action).startswith('add'):
      # add file
      key = str(action).replace('add ', '')
      handleTree('add', key)

      

      print("=> 模块添加成功\n")
      action = input(actionResponse)
    elif str(action).startswith('rm'):
      # rm file
      key = str(action).replace('rm ', '')
      if key == "id" or not addFileTree.contains(key):
        print("=> 该模块未添加，无需移除\n")
      else:
        addFileTree.remove_node(key)
        print("=> 模块移除成功\n")
        
      action = input(actionResponse)
    elif action == 'lsm':
      print("\n所有模块：")
      pathTree.show()
      action = input(actionResponse)
    elif action == 'lss':
      print("\n已选模块：")
      addFileTree.show()
      action = input(actionResponse)
    elif action == 'lsa':
      print("\n所有模块：")
      pathTree.show()
      print("\n已选模块：")
      addFileTree.show()
      action = input(actionResponse)
    elif action == 'done':
      print('=> 选择完毕，开始打包\n')
      break
    elif action == 'exit':
      print('=> 您已取消打包并退出\n')
      break
    elif action == 'help':
      print(actionTip)
      action = input(actionResponse)
    else:
      print("无效指令，请重新操作\n")
      print(actionTip)
      action = input(actionResponse)

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
        print('已选模块\n')
        print(addedFilesArray)

    elif os.path.isdir(child) and len(os.listdir(child)) > 0:
      if(str(dir).lower() == str(fileName).lower()):
        if allowFile:
          if action == 'add':
            addedFilesArray.append(dir)
          elif action == 'rm':
            addedFilesArray.remove(dir)

          filesTree(filePath)
          print('已选模块\n')
          print(addedFilesArray)

        else:
          print('level not 1 rm')
          if action == 'add':
            addedFilesArray.append(dir)
          elif action == 'rm':
            addedFilesArray.remove(dir)

          filesTree(filePath)
          print('已选模块\n')
          print(addedFilesArray)

      else:
        handleActionFile(child, action, fileName, False)

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

  # # 查看模块  
  # filesTree(filePath)
  handlePathFile(filePath)
  print("+----------------------+\n| 欢迎使用模块打包工具 |\n+----------------------+\n")
  print("所有模块")
  pathTree.show()

  # 处理模块
  action = input(actionTip + "\n" + actionResponse)
  handleAction(filePath, action)


