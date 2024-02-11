import os
import re

def file_pass(dir,path,pattern):
    if re.match(pattern, dir):
        yield (dir,path)
    if os.path.isdir(path):
        for file in os.listdir(path):
            yield from file_pass(file,path + "/" + file,pattern)
def file_print(dir,pattern):
    if not os.path.isdir(dir):
        print("error " + dir + " does not exist")
        return
    for file in file_pass(dir,dir,pattern):
        if os.path.isfile(file[1]):
            print("file: " + file[0])
        elif os.path.isdir(file[1]):
            print("directory: " + file[0])
if __name__ == "__main__":
    dir = "../test"
    pattern = "file4.*"
    file_print(dir,pattern)