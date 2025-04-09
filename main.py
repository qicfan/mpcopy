# 1. 启动主进程
# 2. 启动监控进程（将新增文件写入队列）
# 3. 启动消费进程（复制文件）

import argparse
import signal, sys, os
from multiprocessing import Process, Queue
import time

from copyJob import StartCopy
from watch import StartWatch


def Start(srcPath: str, destPath: str):
    watchProcess: Process | None = None
    consumerProcess: Process | None = None
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
    if (srcPath == "" or srcPath is None):
        print("源目录为空")
        stop()
    if (destPath == "" or srcPath is None):
        print("目标目录为空")
        stop()

    watchProcess = Process(target=StartWatch, args=(srcPath, destPath, q))
    print("已启动源目录监控进程")
    watchProcess.start()
    consumerProcess = Process(target=StartCopy, args=(srcPath, destPath, q))
    print("已启动消费进程")
    consumerProcess.start()
    while(True):
        try:
            time.sleep(2)
        except:
            break
    stop()


if __name__ == '__main__':
    key: str = ''
    parser = argparse.ArgumentParser(prog='mpcopy', description='监控目录变化，同步复制文件到网盘', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-s', '--src_path', help='源目录')
    parser.add_argument('-d', '--dest_path', help='目标目录')
    srcPath = '/src'
    destPath = '/dest'
    args, unknown = parser.parse_known_args()
    print("参数：", args)
    if args.src_path != None:
        srcPath = args.src_path
    if args.dest_path != None:
        destPath = args.dest_path
    print("源目录：", srcPath)
    print("目标目录：", destPath)
    Start(srcPath, destPath)