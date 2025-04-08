# 1. 启动主进程
# 2. 启动监控进程（将新增文件写入队列）
# 3. 启动消费进程（复制文件）

import signal, sys, os
from multiprocessing import Process, Queue
import time

from copyJob import StartCopy
from watch import StartWatch


def Start():
    watchProcess: Process | None = None
    consumerProcess: Process | None = None
    srcPath: str = ""
    destPath: str = ""
    q = Queue()

    def stop():
        try:
            if watchProcess is not None:
                watchProcess.terminate()
            if consumerProcess is not None:
                consumerProcess.terminate
        except:
            pass
        sys.exit(0)

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    srcPath = "/src"
    destPath = "/dest"
    if (srcPath == "" or srcPath is None):
        print("源目录为空")
        stop()
    if (destPath == "" or srcPath is None):
        print("目标目录为空")
        stop()

    watchProcess = Process(target=StartWatch, args=(srcPath, destPath, q))
    consumerProcess = Process(target=StartCopy, args=(srcPath, destPath, q))
    while(True):
        try:
            time.sleep(2)
        except:
            break
    stop()


if __name__ == '__main__':
    Start()