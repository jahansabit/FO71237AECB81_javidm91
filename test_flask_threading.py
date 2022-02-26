from multiprocessing import Process
from flask_server import *
import time

server = Process(target=start_server)
server.start()
for i in range(10):
    time.sleep(2)
    print(i)
server.terminate()
server.join()