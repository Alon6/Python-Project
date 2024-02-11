import multiprocessing
import queue
import os
from multiprocessing import Process

dir = "test"

def summFile(file_name,val):
    file = open(dir + "/" + file_name,"r")
    sum = 0
    for line in file:
        sum += int(line)
    val.append({"file name":file_name,"sum":sum})


if __name__ == "__main__":
    procs = queue.Queue()
    manager = multiprocessing.Manager()
    val = manager.list()
    for file in os.listdir(dir):
        proc = Process(target=summFile,args=(file,val,))
        procs.put(proc)
        proc.start()
    while not procs.empty():
        proc = procs.get()
        proc.join()
    print(val)