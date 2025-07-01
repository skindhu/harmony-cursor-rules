"""
配置管理模块
提供应用程序配置、浏览器配置和爬虫配置的管理功能
"""

import sys
from typing import Dict, Any, Optional
from pathlib import Path
from crawl4ai import BrowserConfig, CrawlerRunConfig, CacheMode


class CrawlerConfig:
    """爬虫配置类"""

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.output_dir = "harmony_cursor_rules"
        self.config_file = "harmony_modules_config.json"

    @property
    def browser_config(self) -> BrowserConfig:
        """
        获取浏览器配置

        Returns:
            BrowserConfig: 浏览器配置对象
        """
        return BrowserConfig(
            verbose=False,  # 关闭详细输出
            headless=True,
            browser_type="chromium",
        )

    @property
    def crawler_run_config(self) -> CrawlerRunConfig:
        """
        获取爬虫运行配置

        Returns:
            CrawlerRunConfig: 爬虫运行配置对象
        """
        return CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            wait_for="body",
            delay_before_return_html=15.0,
            page_timeout=60000,
            js_code=self._get_spa_js_code()
        )

    def _get_spa_js_code(self) -> str:
        """
        获取SPA页面专用的JavaScript代码

        Returns:
            str: JavaScript代码字符串
        """
        return """
        await new Promise(resolve => setTimeout(resolve, 3000));
        window.scrollTo(0, document.body.scrollHeight);
        await new Promise(resolve => setTimeout(resolve, 3000));
        window.scrollTo(0, document.body.scrollHeight / 2);
        await new Promise(resolve => setTimeout(resolve, 2000));
        window.scrollTo(0, 0);
        await new Promise(resolve => setTimeout(resolve, 2000));

        const expandButtons = document.querySelectorAll('[class*="expand"], [class*="more"], [class*="show"]');
        for (let button of expandButtons) {
            if (button.click) button.click();
        }
        await new Promise(resolve => setTimeout(resolve, 1000));
        """


class ConfigManager:
    """配置管理器"""

    def __init__(self):
        self._config: Optional[CrawlerConfig] = None

    @classmethod
    def from_command_line(cls) -> 'ConfigManager':
        """
        从命令行参数创建配置管理器

        Returns:
            ConfigManager: 配置管理器实例
        """
        manager = cls()
        debug_mode = "--debug" in sys.argv
        manager._config = CrawlerConfig(debug=debug_mode)
        return manager

    @classmethod
    def from_settings(cls, debug: bool = False, output_dir: str = "harmony_cursor_rules",
                     config_file: str = "harmony_modules_config.json") -> 'ConfigManager':
        """
        从设置参数创建配置管理器

        Args:
            debug: 是否启用调试模式
            output_dir: 输出目录
            config_file: 配置文件路径

        Returns:
            ConfigManager: 配置管理器实例
        """
        manager = cls()
        config = CrawlerConfig(debug=debug)
        config.output_dir = output_dir
        config.config_file = config_file
        manager._config = config
        return manager

    @property
    def config(self) -> CrawlerConfig:
        """
        获取当前配置

        Returns:
            CrawlerConfig: 当前配置对象
        """
        if self._config is None:
            self._config = CrawlerConfig()
        return self._config

    def get_output_directory(self) -> Path:
        """
        获取输出目录路径

        Returns:
            Path: 输出目录路径对象
        """
        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(exist_ok=True)
        return output_dir

    def is_debug_mode(self) -> bool:
        """
        检查是否为调试模式

        Returns:
            bool: 是否为调试模式
        """
        return self.config.debug

    def get_config_file_path(self) -> str:
        """
        获取配置文件路径

        Returns:
            str: 配置文件路径
        """
        return self.config.config_file

    def should_save_html(self) -> bool:
        """
        检查是否应该保存HTML文件

        Returns:
            bool: 是否保存HTML文件
        """
        return self.config.debug

    def get_browser_config(self) -> BrowserConfig:
        """
        获取浏览器配置

        Returns:
            BrowserConfig: 浏览器配置对象
        """
        return self.config.browser_config

    def get_crawler_run_config(self) -> CrawlerRunConfig:
        """
        获取爬虫运行配置

        Returns:
            CrawlerRunConfig: 爬虫运行配置对象
        """
        return self.config.crawler_run_config

    def print_startup_info(self) -> None:
        """打印启动信息"""
        print("🚀 开始HarmonyOS界面开发最佳实践完整爬取")
        if self.is_debug_mode():
            print("🔧 调试模式已启用")
        print("=" * 80)

    def get_settings_summary(self) -> Dict[str, Any]:
        """
        获取配置摘要信息

        Returns:
            Dict: 配置摘要字典
        """
        return {
            'debug_mode': self.is_debug_mode(),
            'output_directory': str(self.get_output_directory()),
            'config_file': self.get_config_file_path(),
            'save_html': self.should_save_html()
        }