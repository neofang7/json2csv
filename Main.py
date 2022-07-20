from re import split
import sys
import os
import types
from MemoryFootprint import MemoryFootprint
from Blogbench import Blogbench
from BootTimes import BootTimes
from NetworkIperf3 import NetworkIperf3
from MemoryFootprintInsideContainer import MemoryFootprintInsideContainer
from MemoryFootprintKsm import MemoryFootprintKsm
from Mlc import Mlc

def filename_to_classname(file_name, postfix):
    #remove .py
    #file_name = file_name[:-3]
    strs = file_name[:-len(postfix)].split('-')
    class_name = ""
    for s in strs:
        class_name += s.capitalize()
    return class_name


if __name__ == '__main__':
    # parse folder and get the generated json files.
    args = sys.argv[1:]

    for root, dirs, files in os.walk(args[0]):
        print(files)
        print(root)

        for f in files:
            #class_type = (globals()['BootTimes'])
            class_name = filename_to_classname(f, '.json')
            if class_name not in globals().keys():
                print('Unsupported class ', class_name)
                continue
            class_type = globals()[class_name]
            obj = class_type()
            obj.load_from_jsonfile(root+'/'+f)
            obj.to_csv('output/'+f[:-5]+'.csv')
