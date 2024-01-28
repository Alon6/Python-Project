import os

def file_read(file):
    for row in open(file,"r"):
        yield row

def file_print(file):
    if os.path.isfile(file):
        for row in file_read(file):
            print(row)
    else:
        print("error " + file + " does not exist")
if __name__ == "__main__":
    file = "../test/file4.txt"
    file_print(file)