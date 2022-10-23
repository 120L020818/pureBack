import logging
import sys


def log(name):
    # 1 - 配置日志记录器名称
    logger = logging.getLogger(name)

    # 2-配置日志级别
    logger.setLevel(logging.DEBUG)

    # 3-配置日志格式（可以分别设置，也可以统一设置）
    format = logging.Formatter('%(name)s-%(asctime)s-%(message)s')

    # 4 - 创建并添加handler - 控制台
    sh = logging.StreamHandler()
    sh.setFormatter(format)
    logger.addHandler(sh)

    # 5 - 创建并添加handler - 文件
    fh = logging.FileHandler(name + '.log')
    fh.setFormatter(format)
    logger.addHandler(fh)

    # 6 - 提供对外获取logger
    return logger


logger = log('user')
logger2 = log('operate')

if __name__ == '__main__':
    logger.info('使用函数定义的log方法')
