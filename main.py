# 1. 启动主进程
# 2. 启动监控进程（将新增文件写入队列）
# 3. 启动消费进程（复制文件）

import signal, sys, os
from multiprocessing import Process, Queue

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
    
    def startWatch():
        StartWatch(srcPath, q)

    def startConsumer():
        StartCopy(srcPath, destPath, q)

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

    watchProcess = Process(target=startWatch)
    consumerProcess = Process(target=startConsumer)

if __name__ == '__main__':
    Start()