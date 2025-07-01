"""
核心爬虫模块
提供主要的网页爬取功能，整合SPA处理和文件保存
"""

import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from crawl4ai import AsyncWebCrawler
from config import ConfigManager
from ai import ContentProcessor
from utils import URLHelper
from .spa_handler import SPAHandler
from .file_saver import FileSaver


class WebCrawler:
    """核心网页爬虫类"""

    def __init__(self, config_manager: ConfigManager, content_processor: ContentProcessor):
        """
        初始化网页爬虫

        Args:
            config_manager: 配置管理器
            content_processor: AI内容处理器
        """
        self.config_manager = config_manager
        self.content_processor = content_processor

        # 初始化组件
        self.spa_handler = SPAHandler()
        self.file_saver = FileSaver(debug_mode=config_manager.is_debug_mode())

        # 获取配置
        self.output_dir = config_manager.get_output_directory()
        self.debug_mode = config_manager.is_debug_mode()

    async def crawl_single_page(
        self,
        url: str,
        module_name: Optional[str] = None,
        use_spa_mode: bool = True,
        extract_best_practices: bool = True
    ) -> Dict[str, Any]:
        """
        爬取单个页面

        Args:
            url: 目标URL
            module_name: 模块名称，如果为None则从URL提取
            use_spa_mode: 是否使用SPA模式
            extract_best_practices: 是否使用AI提取最佳实践，默认为True

        Returns:
            Dict: 爬取结果，包含html_content字段
        """
        # 生成模块名
        if not module_name:
            module_name = URLHelper.get_module_name_from_url(url)

        # 选择爬虫配置
        if use_spa_mode:
            run_config = self.spa_handler.create_spa_crawler_config()
        else:
            run_config = self.config_manager.get_crawler_run_config()

        try:
            async with AsyncWebCrawler(config=self.config_manager.get_browser_config()) as crawler:
                result = await crawler.arun(url=url, config=run_config)

                if not result.success:
                    return {
                        "success": False,
                        "error": f"页面访问失败: {result.error_message}",
                        "url": url,
                        "module_name": module_name
                    }

                # 获取页面内容
                page_content = result.cleaned_html or result.html

                # 验证内容有效性
                if use_spa_mode and not self.spa_handler.validate_spa_content(page_content):
                    return {
                        "success": False,
                        "error": "SPA页面内容验证失败或内容过少",
                        "url": url,
                        "module_name": module_name
                    }
                elif not use_spa_mode and len(page_content) < 1000:
                    return {
                        "success": False,
                        "error": "页面内容获取失败或内容过少",
                        "url": url,
                        "module_name": module_name
                    }

                # 提取元数据
                if use_spa_mode:
                    metadata = self.spa_handler.extract_spa_metadata(result)
                else:
                    metadata = {
                        'title': result.metadata.get('title', '未知标题') if result.metadata else '未知标题',
                        'url': url,
                        'content_type': 'standard'
                    }

                # 根据开关决定是否使用AI处理器提取最佳实践
                markdown_content = ""
                if extract_best_practices and self.content_processor.is_api_available():
                    markdown_content = self.content_processor.extract_best_practices(
                        html_content=page_content,
                        module_name=module_name,
                        title=metadata['title'],
                        url=url
                    )

                # 保存文件
                save_result = self.file_saver.save_crawl_result(
                    target_dir=self.output_dir,
                    module_name=module_name,
                    sub_module_name=metadata['title'],
                    html_content=page_content,
                    markdown_content=markdown_content,
                    metadata=metadata
                )

                # 在返回结果中添加原始HTML内容
                save_result['html_content'] = page_content
                save_result['url'] = url
                save_result['module_name'] = module_name

                return save_result

        except Exception as e:
            return {
                "success": False,
                "error": f"爬取过程发生异常: {str(e)}",
                "url": url,
                "module_name": module_name
            }

    async def crawl_with_directory_structure(
        self,
        target_dir: Path,
        url: str,
        module_name: str,
        sub_module_name: str
    ) -> Dict[str, Any]:
        """
        按目录结构爬取并保存文件

        Args:
            target_dir: 目标目录
            url: 目标URL
            module_name: 模块名称（用于文件命名）
            sub_module_name: 子模块中文名称

        Returns:
            Dict: 爬取结果
        """
        # 检查文件是否已存在
        existing_result = self.file_saver.check_existing_files(
            target_dir, module_name, sub_module_name
        )
        if existing_result:
            existing_result["url"] = url  # 补充URL信息
            return existing_result

        # 获取SPA爬虫配置
        run_config = self.spa_handler.create_spa_crawler_config()

        try:
            async with AsyncWebCrawler(config=self.config_manager.get_browser_config()) as crawler:
                result = await crawler.arun(url=url, config=run_config)

                if not result.success:
                    return {
                        "success": False,
                        "error": f"页面访问失败: {result.error_message}",
                        "url": url,
                        "module_name": module_name,
                        "sub_module_name": sub_module_name
                    }

                # 获取页面内容
                page_content = result.cleaned_html or result.html

                # 验证SPA页面内容
                if not self.spa_handler.validate_spa_content(page_content):
                    return {
                        "success": False,
                        "error": "SPA页面内容验证失败或内容过少",
                        "url": url,
                        "module_name": module_name,
                        "sub_module_name": sub_module_name
                    }

                # 提取元数据
                metadata = self.spa_handler.extract_spa_metadata(result)
                metadata['url'] = url

                # 使用AI内容处理器提取最佳实践
                markdown_content = ""
                if self.content_processor.is_api_available():
                    markdown_content = self.content_processor.extract_best_practices(
                        html_content=page_content,
                        module_name=sub_module_name,  # 使用中文名称
                        title=metadata['title'],
                        url=url
                    )

                # 创建临时文件保存器（使用目标目录）
                temp_file_saver = FileSaver(debug_mode=self.debug_mode)
                save_result = temp_file_saver.save_crawl_result(
                    target_dir=target_dir,
                    module_name=module_name,
                    sub_module_name=sub_module_name,
                    html_content=page_content,
                    markdown_content=markdown_content,
                    metadata=metadata
                )

                return save_result

        except Exception as e:
            return {
                "success": False,
                "error": f"爬取过程发生异常: {str(e)}",
                "url": url,
                "module_name": module_name,
                "sub_module_name": sub_module_name
            }

    async def crawl_spa_page_legacy(
        self,
        url: str,
        module_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        爬取SPA页面的遗留接口（保持向后兼容）

        Args:
            url: 目标URL
            module_name: 模块名称，用于文件命名

        Returns:
            Dict: 爬取结果
        """
        return await self.crawl_single_page(
            url=url,
            module_name=module_name,
            use_spa_mode=True
        )

    def get_crawler_stats(self) -> Dict[str, Any]:
        """
        获取爬虫统计信息

        Returns:
            Dict: 统计信息
        """
        return {
            'config_manager_ready': self.config_manager is not None,
            'content_processor_ready': self.content_processor is not None,
            'ai_available': self.content_processor.is_api_available() if self.content_processor else False,
            'spa_handler_ready': self.spa_handler is not None,
            'file_saver_ready': self.file_saver is not None,
            'debug_mode': self.debug_mode,
            'output_directory': str(self.output_dir)
        }

    async def batch_crawl_urls(
        self,
        urls: list,
        use_spa_mode: bool = True,
        delay_between_requests: float = 3.0
    ) -> list:
        """
        批量爬取URL列表

        Args:
            urls: URL列表
            use_spa_mode: 是否使用SPA模式
            delay_between_requests: 请求间延迟时间（秒）

        Returns:
            list: 爬取结果列表
        """
        results = []

        for i, url in enumerate(urls):
            print(f"爬取进度: {i+1}/{len(urls)} - {url}")

            result = await self.crawl_single_page(
                url=url,
                use_spa_mode=use_spa_mode
            )
            results.append(result)

            # 添加延迟避免频繁请求
            if i < len(urls) - 1:
                await asyncio.sleep(delay_between_requests)

        return results

    def validate_crawl_environment(self) -> Dict[str, bool]:
        """
        验证爬虫运行环境

        Returns:
            Dict: 验证结果
        """
        validations = {
            'config_manager_valid': self.config_manager is not None,
            'content_processor_valid': self.content_processor is not None,
            'output_directory_exists': self.output_dir.exists(),
            'browser_config_valid': True,  # 假设配置总是有效的
            'spa_handler_valid': self.spa_handler is not None,
            'file_saver_valid': self.file_saver is not None
        }

        # 检查浏览器配置
        try:
            browser_config = self.config_manager.get_browser_config()
            validations['browser_config_valid'] = browser_config is not None
        except Exception:
            validations['browser_config_valid'] = False

        # 检查AI功能
        if self.content_processor:
            validations['ai_processor_available'] = self.content_processor.is_api_available()
        else:
            validations['ai_processor_available'] = False

        return validations