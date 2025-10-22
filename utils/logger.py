"""
日志工具模块
提供统一的日志记录功能
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from config.settings import LOG_CONFIG, OUTPUT_CONFIG


class Logger:
    """日志记录器类"""
    
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化日志记录器"""
        if self._initialized:
            return
        
        self._initialized = True
        
        # 创建日志目录
        log_dir = LOG_CONFIG['log_dir']
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 日志文件路径
        log_file = os.path.join(log_dir, LOG_CONFIG['log_filename'])
        
        # 创建logger
        self.logger = logging.getLogger('Music163')
        self.logger.setLevel(getattr(logging, LOG_CONFIG['log_level']))
        
        # 避免重复添加handler
        if not self.logger.handlers:
            # 文件处理器 - 使用RotatingFileHandler实现日志轮转
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=LOG_CONFIG['max_bytes'],
                backupCount=LOG_CONFIG['backup_count'],
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # 格式化器
            formatter = logging.Formatter(
                LOG_CONFIG['log_format'],
                datefmt=LOG_CONFIG['date_format']
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # 添加处理器
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """获取日志记录器"""
        return self.logger
    
    def debug(self, message):
        """调试日志"""
        self.logger.debug(message)
    
    def info(self, message):
        """信息日志"""
        self.logger.info(message)
    
    def warning(self, message):
        """警告日志"""
        self.logger.warning(message)
    
    def error(self, message):
        """错误日志"""
        self.logger.error(message)
    
    def critical(self, message):
        """严重错误日志"""
        self.logger.critical(message)
    
    def exception(self, message):
        """异常日志(包含堆栈信息)"""
        self.logger.exception(message)


# 创建全局日志实例
logger = Logger()


def get_logger():
    """获取日志记录器实例"""
    return logger


if __name__ == '__main__':
    # 测试日志功能
    log = get_logger()
    log.debug("这是一条调试信息")
    log.info("这是一条普通信息")
    log.warning("这是一条警告信息")
    log.error("这是一条错误信息")
    log.critical("这是一条严重错误信息")

