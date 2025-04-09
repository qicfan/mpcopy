import os
import shutil
from multiprocessing import Queue
import signal
import sys
import time
from log import getLogger

logger = getLogger(name='copy_job', rotating=True, stream=True)

def StartCopy(srcPath: str, destPath: str, q: Queue):
    """
    启动复制进程
    :param srcPath: 源目录
    :param destPath: 目标目录
    :param q: 队列
    """
    def stop(sig, frame):
        logger.info("复制进程停止")
        if not q.empty():
            while not q.empty():
                job = q.get()
                logger.info("队列中还有任务: {0}".format(job))
        else:
            logger.info("队列为空，退出复制进程")
        sys.exit(0)
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    while True:
        if not q.empty():
            path = q.get()
            srcRealPath = os.path.join(srcPath, path)
            destRealPath = os.path.join(destPath, path)
            # 复制文件
            if not os.path.exists(srcRealPath):
                logger.warning("源文件不存在: {0}".format(srcRealPath))
                continue
            if os.path.exists(destRealPath):
                logger.warning("目标文件已存在: {0}".format(destRealPath))
                continue
            try:
                dirname = os.path.dirname(destRealPath)
                # 如果目录不存在，先创建目录
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                shutil.copy(srcRealPath, destRealPath)
                logger.info("复制文件：{0} => {1}".format(srcRealPath, destRealPath))
            except Exception as e:
                logger.error("复制文件失败: {0} {1} => {2}".format(e, srcRealPath, destRealPath))
        else:
            # 队列为空，等待10秒
            #logger.info("队列为空，等待10秒")
            time.sleep(10)

