from multiprocessing import Queue
import signal
import time
from watchdog.observers import Observer
from watchdog.events import *
import os, sys

from log import getLogger

logger = getLogger(name='watch', rotating=True, stream=True)
ob = Observer()

class FileEventHandler(FileSystemEventHandler):

    def __init__(self, srcPath, destPath: str, q: Queue):
        super().__init__()
        self.srcPath = srcPath
        self.destPath = destPath
        self.q = q
    
    def getRealPath(self, path):
        # 返回目标位置路径
        newPath: str = path.lstrip(self.srcPath)
        if newPath.startswith(os.sep):
            newPath.lstrip(os.sep)
        if newPath.startswith("wnloads"):
            newPath = "do{0}".format(newPath)
        return newPath

    def on_any_event(self, event):
        return True

    def on_moved(self, event):
        logger.info("移动: {0} => {1}".format(event.src_path, event.dest_path))
        return True
    
    def on_deleted(self, event):
        logger.info("删除: {0}".format(event.src_path))
        return True

    def on_modified(self, event):
        return True

    def on_created(self, event):
        filePath = self.getRealPath(event.src_path)
        if filePath.startswith('downloads'):
            return True
        if event.is_directory:
            realPath = os.path.join(self.destPath, filePath)
            if not os.path.exists(realPath):
                os.makedirs(realPath)
                logger.info("创建目录: {0}".format(realPath))
        else:
            filename, ext = os.path.splitext(filePath)
            if ext == ".mp":
                filePath = filename
            self.q.put(filePath)
            logger.info("新增文件: {0} => {1}".format(filePath, event.src_path))

def StartWatch(srcPath: str, destPath: str, q: Queue):
    global ob
    def stop(sig, frame):
        ob.unschedule_all()
        ob.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    eventHandler = FileEventHandler(srcPath, destPath, q)
    ob.schedule(eventHandler, srcPath, recursive=True) # 指定监控路径/触发对应的监控事件类
    isStart = False
    while(True):
        try:
            if isStart is False:
                ob.start()
                isStart = True
                logger.info("已启动监控任务")
            #logger.info('已启动所有监控任务，开始10s一次检测任务执行状态')
            time.sleep(10)
        except Exception as e:
            logger.error("监控任务停止: {1}".format(e))
            break
