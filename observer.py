import time
import threading
from coordinate import *
from exception import *


class Observer(threading.Thread):
    def run(self):
        time.sleep(10)
        appWindow.eventQueue.put(SkipException())
