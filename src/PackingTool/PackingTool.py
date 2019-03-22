#!/usr/bin/env python 3.x
# encoding: utf-8

import os.path
import shutil
import re
from treelib import Node, Tree

import tkinter as tk
from tkinter import filedialog
import zipfile

'''
1、读取指定目录下的所有文件
2、匹配出需要的文件
3、复制到指定位置
'''

filePath = ''
pathTree = Tree()
pathTree.create_node("/", "id")

addFileTree = Tree()
addFileTree.create_node("/", "id")

actionTip = "\n+------------------------------------------------------------------------------------------------------------------------------------------------------------------------+\n| add: 添加 | rm: 移除 | addall: 添加所有 | rmall:移除所有 | lsm:查看所有模块 | lss:查看已选模块 | lsa: 查看所有模块及已选模块 | done: 完成 | exit:取消 | help: 查看指令 |\n+------------------------------------------------------------------------------------------------------------------------------------------------------------------------+"
actionResponse = "[请选择操作]$ "

# 遍历指定目录下所有文件，生成文件目录 pathTree
def handlePathFile(sourcePath, parentKey = 'id'):
  fileDir = os.listdir(sourcePath)
  hasDir = False
  # for item in fileDir:
  #   if os.path.isdir(os.path.join('%s\%s' % (sourcePath, item))):
  #     hasDir = True
  #     break

  for index, dir in enumerate(fileDir):
    child = os.path.join('%s\%s' % (sourcePath, dir))
    if os.path.isfile(child):
      print(len(os.listdir(sourcePath)))
      key = parentKey + (str(index) if index > 9 else '0' + str(index))
      pathTree.create_node(dir + '  ' + key, key, parentKey)

    if os.path.isdir(child) and len(os.listdir(child)) > 0:
      key = parentKey + (str(index) if index > 9 else '0' + str(index))
      pathTree.create_node(dir + '  ' + key, key, parentKey)

      handlePathFile(child, key)

def addAll(sourcePath, parentKey = 'id'):
  fileDir = os.listdir(sourcePath)
  hasDir = False
  # for item in fileDir:
  #   if os.path.isdir(os.path.join('%s\%s' % (sourcePath, item))):
  #     hasDir = True
  #     break

  for index, dir in enumerate(fileDir):
    child = os.path.join('%s\%s' % (sourcePath, dir))
    if os.path.isfile(child):
      key = parentKey + (str(index) if index > 9 else '0' + str(index))
      if not addFileTree.contains(key):
        addFileTree.create_node(dir + '  ' + key, key, parentKey)

    if os.path.isdir(child) and len(os.listdir(child)) > 0:
      key = parentKey + (str(index) if index > 9 else '0' + str(index))
      if not addFileTree.contains(key):
        addFileTree.create_node(dir + '  ' + key, key, parentKey)

      addAll(child, key)

def rmAll(sourcePath):
  fileDir = os.listdir(sourcePath)
  for index, dir in enumerate(fileDir):
    key = 'id' + (str(index) if index > 9 else '0' + str(index))
    if addFileTree.contains(key):
      addFileTree.remove_node(key)

# 添加树节点
def addNode(key):
  node = pathTree.get_node(key)
  print(Node.is_leaf(node))
  name = pathTree.get_node(key).tag
  if len(key) == 4:
    addFileTree.create_node(name, key, "id")
  else:
    treeDeep = int(len(key) / 2)
    keyArray = [key[0 : i * 2 + 4] for i in range(treeDeep - 1)]
    for key in keyArray:
      if not addFileTree.contains(key):
        addFileTree.create_node(pathTree.get_node(key).tag, key, key[:-2])

# 压缩指定文件夹
# param dirPath: 目标文件夹路径
# param outFullName: 压缩文件保存路径+xxxx.zip
# return: 无
def zipDir(dirPath, outFullName):
    zip = zipfile.ZipFile(outFullName,"w",zipfile.ZIP_DEFLATED)
    for path,dirnames,filenames in os.walk(dirPath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirPath,'')

        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
    zip.close()

# 选择打包存放路径
def pack():
  root = tk.Tk()
  root.withdraw()
  
  packPath = filedialog.askdirectory()
  print(packPath)
  print('打包中...')

  leafPathList = Tree.paths_to_leaves(addFileTree)

  for pathList in leafPathList:
    curLeafPath = filePath
    targetLeafPath = packPath
    for path  in pathList:
      if path != 'id':
        pathName = addFileTree.get_node(path).tag[:-(len(path) + 2)]
        curLeafPath = os.path.join(curLeafPath, pathName)
        targetLeafPath  = os.path.join(targetLeafPath, pathName)

    print(curLeafPath)
    print(targetLeafPath)
    targetLeafPath = targetLeafPath.replace('/', '\\')
    if curLeafPath.find('.') == -1:
      shutil.copytree(curLeafPath, targetLeafPath)
    else:
      targetLeafParent = os.path.split(targetLeafPath)[0]
      if os.path.exists(targetLeafParent):
        shutil.copy(curLeafPath, targetLeafPath)
      else:
        os.makedirs(targetLeafParent) 
        shutil.copy(curLeafPath, targetLeafPath)

  print('\n打包完成，开始压缩文件...')
  
  outZipPath = os.path.join(packPath, 'dist.zip')
  zipDir(packPath, outZipPath)
      
  print('\n打包完成，模块输出路径：' + packPath + '/ dist.zip')

# 根据指令处理文件
def handleAction(sourcePath, action):
  while True:
    if action == 'addall':
      rmAll(sourcePath)
      addAll(sourcePath, 'id')
      print("=> 所有模块添加成功\n")
      action = input(actionResponse)
    elif action == 'rmall':
      rmAll(sourcePath)
      print("=> 所有模块移除成功\n")
      action = input(actionResponse)
    elif str(action).startswith('add'):
      # add file
      key = str(action).replace('add ', '')

      if len(key) < 4 or not key.startswith('id') or not pathTree.contains(key):
        print("=> 该模块不存在\n")
      else:
        addNode(key)
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
      print('=> 选择模块完毕，请选择打包文件保存路径\n')
      pack()
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


