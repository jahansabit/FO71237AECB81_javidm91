import threading
import time

def sum_and_wait(id, x, y):
    print(x + y)
    for i in range(5):
        time.sleep(1)
        print("from_id", id, i)

for i in range(5):
    threading.Thread(target=sum_and_wait, args=(i, i, i)).start()