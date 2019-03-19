import os
from treelib import Node, Tree

pathTree = Tree()
pathTree.create_node("/", "id")
 
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        dir_indent = "|   " * (level-1) + "|-- "
        file_indent = "|   " * level + "|-- "
        if not level:
            print('.')
        else:
            print('{}{}{}{}'.format(dir_indent, os.path.basename(root), ' ', level))
        for f in files:
            print('{}{}{}{}'.format(file_indent, f, ' ', level + 1))

if __name__ == "__main__":
    # list_files('D:\\dev\\github\\antd-admin\\src\\components')  # refer root dir
    pathTree.create_node("a", "id11", "id")
    pathTree.show()

    pathTree.remove_node('id11')
    pathTree.show()
