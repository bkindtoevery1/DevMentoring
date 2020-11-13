import threading, time
"""
def task(user_id):
    ret = 0
    for i in range(50000000):
        ret += i
    print('Hello World '+user_id + str(ret))

if __name__ == "__main__":
    thread1 = threading.Thread(target=task, args=('a'))
    thread2 = threading.Thread(target=task, args=('b'))
    thread3 = threading.Thread(target=task, args=('c'))
    thread1.start()
    thread1.join()
    thread2.start()
    thread2.join()
    thread3.start()
    thread3.join()
"""

class global_variable():
    def __init__(self):
        self.lock = threading.Lock()
        self.posts_count = 0
    
    def adding_post(self):
        self.lock.acquire()
        try:
            self.posts_count += 1
        finally:
            self.lock.release()
    
class multi_threading(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        global total_count

        for _ in range(1000000):
            total_count.adding_post()
        print("task complete")

if __name__ == '__main__':
    global total_count
    total_count = global_variable()

    for _ in range(4):
        thread_temp = multi_threading()
        thread_temp.start()
    main_thread = threading.current_thread()
    for thread in threading.enumerate():
        if thread is not main_thread:
            thread.join()
    print(total_count.posts_count)