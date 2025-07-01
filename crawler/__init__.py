"""
爬虫包
提供网页爬取、SPA处理、文件保存等功能
"""

from .core import WebCrawler
from .spa_handler import SPAHandler
from .file_saver import FileSaver

__all__ = ['WebCrawler', 'SPAHandler', 'FileSaver']