# # we need a parent class to manage a tree of objects (component)
# # eed to be able to access both File and folder (as both have unique methods)
# class Component:
#     def __init__(self, name):
#         self.name = name
#     def move(self, new_path):
#         new_folder = get_path(new_path)
#         del self.parent.children[self.name]
#         new_folder.children[self.name] = self
#         self.parent = new_folder 
#     def delete(self):
#         del self.parent.children[self.name]
        
# class Folder(Component):
#     def __init__(self, name):
#         super().__init__(name)
#         self.children = {}
#     def add_child(self, child):
#         child.parent = self
#         self.children[child.name] = child
#     def copy(self, new_path):
#         pass
    
# class File(Component):
#     def __init__(self, name, contents):
#         super().__init__(name)
#         self.contents = contents
#     def copy(self, new_path):
#         pass


# root = Folder('')
# def get_path(path):
#     names = path.split('/')[1:]
#     node = root
#     for name in names:
#         node = node.children[name]
#     return node




# folder1 = Folder('folder1')
# folder2 = Folder('folder2')
# root.add_child(folder1)
# root.add_child(folder2)
# folder11 = Folder('folder11')
# folder1.add_child(folder11)
# file111 = File('file111', 'contents')
# folder11.add_child(file111)
# file21 = File('file21', 'other contents')
# folder2.add_child(file21)
# print(folder2.children)


# folder2.move('/folder1/folder11')
# print(folder11.children)


phone=("Phone", 256)
truck_toy=("TruckToy", 289)
plain_toy=("PlainToy", 587)
root_box=[truck_toy,plain_toy]
soldier_toy=("SoldierToy", 200)
child_box=[soldier_toy]
root_box.append(child_box)

print(root_box)
# dequy hoac try a[1] catch, hoac loc file co duoi .wav cua loi
print("tonggia")

# import os
# import argparse
# from collections import defaultdict


# def pairing(input_path, relative: bool = False):
#     pairs = defaultdict(dict)
#     stack = [input_path]
#     while stack:
#         node = stack.pop()
#         if os.path.isdir(node):
#             paths = sorted(os.listdir(node), reverse=True)
#             for f in paths:
#                 stack.append(os.path.join(node, f))
#         elif os.path.isfile(node):
#             if relative is True:
#                 node = os.path.relpath(node, input_path)
#             f_name, f_ext = os.path.splitext(node)
#             if f_ext == ".txt":
#                 pairs[f_name]["text"] = node
#             elif f_ext == ".wav" or f_ext == ".mp3":
#                 pairs[f_name]["audio"] = node
#     ret_pairs = {}
#     for k, v in pairs.items():
#         if len(v) == 2 and "text" in v and "audio" in v:
#             ret_pairs[k] = v
#     return ret_pairs
