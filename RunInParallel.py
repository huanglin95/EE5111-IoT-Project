
import os
import threading

def fun1():
    os.system("python FD001.py")
def fun2():
    os.system("python FD002.py")

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()
    
run_threaded(fun1)
run_threaded(fun2)