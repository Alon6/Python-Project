import os


def file_pass(dir):
    if os.path.isfile(dir):
        print("file: " + dir)
        print("file's content:\n" + open(dir,"r").read())
    elif os.path.isdir(dir):
        print("directory: " + dir)
        for file in os.listdir(dir):
            file_pass(dir + "/" + file)
    else:
        print("error " + dir + " does not exist")
if __name__ == "__main__":
    dir = "../test"
    file_pass(dir)