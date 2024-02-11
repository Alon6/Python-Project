import threading
import time
def writeLog(lock):
    with lock:
        file = open("log.txt","a")
        file.write("Thread " + threading.current_thread().name + " writes to log at " + str(time.time()) + ".\n")
        file.close()

if __name__ == "__main__":
    lock = threading.Lock()
    t1 = threading.Thread(target=writeLog,args=(lock,), name='t1')
    t2 = threading.Thread(target=writeLog,args=(lock,), name='t2')
    t3 = threading.Thread(target=writeLog,args=(lock,), name='t3')
    t4 = threading.Thread(target=writeLog,args=(lock,), name='t4')
    t5 = threading.Thread(target=writeLog,args=(lock,), name='t5')
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()