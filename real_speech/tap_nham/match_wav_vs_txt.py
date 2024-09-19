import os
import argparse
from collections import defaultdict


def pairing(input_path, relative: bool = False):
    pairs = defaultdict(dict)
    stack = [input_path]
    while stack:
        node = stack.pop()
        if os.path.isdir(node):
            paths = sorted(os.listdir(node), reverse=True)
            for f in paths:
                stack.append(os.path.join(node, f))
        elif os.path.isfile(node):
            if relative is True:
                node = os.path.relpath(node, input_path)
            f_name, f_ext = os.path.splitext(node)
            if f_ext == ".txt":
                pairs[f_name]["text"] = node
            elif f_ext == ".wav" or f_ext == ".mp3":
                pairs[f_name]["audio"] = node
    # ret_pairs = {}
    # for k, v in pairs.items():
    #     if len(v) == 2 and "text" in v and "audio" in v:
    #         ret_pairs[k] = v
    # return ret_pairs


    return pairs