#!/usr/bin/env python 3.6
# encoding: utf-8

import os.path
import time
from subprocess import Popen

# 遍历指定目录下所有文件
def handlePathFile(sourcePath):
  fileDir = os.listdir(sourcePath)
  hasDir = False
  # for item in fileDir:
  #   if os.path.isdir(os.path.join('%s\%s' % (sourcePath, item))):
  #     hasDir = True
  #     break

  for index, dir in enumerate(fileDir):
    child = os.path.join('%s\%s' % (sourcePath, dir))
    print('sourcePath:' + sourcePath + 'child:' + child)
    if os.path.isfile(child) and child.endswith('index.js'):
      # os.system(filePath.split('\\')[0] + ' cd ' + sourcePath + 'uglifyjs index.js -m -o index.js')
      # time.sleep(1)

      # p = Popen([filePath.split('\\')[0] + ' cd ' + sourcePath + 'uglifyjs index.js -m -o index.js']) # something long running
      # # ... do other stuff while subprocess is running
      # p.terminate()
      command = filePath.split('\\')[0] + ' cd ' + sourcePath + ' uglifyjs index.js -m -o index.js'
      cmd = Popen(command)
      cmd.communicate()

    if os.path.isdir(child) and len(os.listdir(child)) > 0:
      handlePathFile(child)

if __name__ == "__main__":
  # filePath = 'D:\\dev\\github\\antd-admin\\src\\components'  # refer root dir
  # E:\\code\\github\\antd-admin\\src\\components
  # E:\\code\\work\\20190402_svms_daily\\30-web\\dist

  # 输入路径
  print("+----------------------+\n| 欢迎使用模块打包工具 |\n+----------------------+\n")
  filePath = 'E:\\code\\work\\20190402_svms_daily\\30-web\\dist'

  # filePath = input("请输入源文件路径：")

  # while True:
  #   if os.path.exists(filePath):
  #     break
  #   else:
  #     filePath = input("该目录不存在，请重新输入：")
  print('filePath.split' + filePath.split('\\')[0])
  

  # # 压缩文件  
  handlePathFile(filePath)