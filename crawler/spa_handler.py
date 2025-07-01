"""
SPA页面处理器模块
专门处理Single Page Application的爬取需求
"""

import asyncio
from typing import Dict, Any, Optional
from crawl4ai import CrawlerRunConfig, CacheMode


class SPAHandler:
    """SPA页面处理器"""

    def __init__(self):
        """初始化SPA处理器"""
        self.default_wait_time = 15.0
        self.page_timeout = 60000
        self.scroll_delay = 3000  # 滚动延迟毫秒
        self.interaction_delay = 2000  # 交互延迟毫秒

    def get_spa_javascript_code(self) -> str:
        """
        获取SPA页面专用的JavaScript代码

        Returns:
            str: JavaScript代码字符串
        """
        return f"""
        // 等待页面基础加载完成
        await new Promise(resolve => setTimeout(resolve, {self.scroll_delay}));

        // 滚动到页面底部触发懒加载
        window.scrollTo(0, document.body.scrollHeight);
        await new Promise(resolve => setTimeout(resolve, {self.scroll_delay}));

        // 滚动到页面中部
        window.scrollTo(0, document.body.scrollHeight / 2);
        await new Promise(resolve => setTimeout(resolve, {self.interaction_delay}));

        // 滚回顶部
        window.scrollTo(0, 0);
        await new Promise(resolve => setTimeout(resolve, {self.interaction_delay}));

        // 尝试点击可能的展开按钮
        const expandButtons = document.querySelectorAll('[class*="expand"], [class*="more"], [class*="show"]');
        for (let button of expandButtons) {{
            if (button.click) button.click();
        }}
        await new Promise(resolve => setTimeout(resolve, 1000));
        """

    def create_spa_crawler_config(
        self,
        custom_js_code: Optional[str] = None,
        wait_time: Optional[float] = None,
        timeout: Optional[int] = None
    ) -> CrawlerRunConfig:
        """
        创建SPA页面专用的爬虫配置

        Args:
            custom_js_code: 自定义JavaScript代码
            wait_time: 等待时间（秒）
            timeout: 页面超时时间（毫秒）

        Returns:
            CrawlerRunConfig: 爬虫运行配置
        """
        js_code = custom_js_code or self.get_spa_javascript_code()
        wait_time = wait_time or self.default_wait_time
        timeout = timeout or self.page_timeout

        return CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            wait_for="body",
            delay_before_return_html=wait_time,
            page_timeout=timeout,
            js_code=js_code
        )

    def validate_spa_content(self, content: str, min_length: int = 1000) -> bool:
        """
        验证SPA页面内容是否有效

        Args:
            content: 页面内容
            min_length: 最小内容长度

        Returns:
            bool: 内容是否有效
        """
        if not content:
            return False

        if len(content) < min_length:
            return False

        # 检查是否包含常见的SPA加载指示器
        loading_indicators = [
            'loading...', 'please wait', '正在加载', '请稍候',
            'spinner', 'loader', 'loading-'
        ]

        content_lower = content.lower()
        for indicator in loading_indicators:
            if indicator in content_lower:
                # 如果内容主要是加载指示器，认为无效
                if len(content.strip()) < min_length * 2:
                    return False

        return True

    def extract_spa_metadata(self, crawler_result) -> Dict[str, Any]:
        """
        从爬取结果中提取SPA页面元数据

        Args:
            crawler_result: crawl4ai的爬取结果

        Returns:
            Dict: 元数据字典
        """
        metadata = {
            'title': '未知标题',
            'url': '',
            'content_type': 'spa',
            'success': crawler_result.success if crawler_result else False
        }

        if not crawler_result or not crawler_result.success:
            return metadata

        # 提取标题
        if hasattr(crawler_result, 'metadata') and crawler_result.metadata:
            metadata['title'] = crawler_result.metadata.get('title', '未知标题')

        # 提取URL
        if hasattr(crawler_result, 'url'):
            metadata['url'] = crawler_result.url

        # 添加其他有用的元数据
        if hasattr(crawler_result, 'response_headers'):
            metadata['response_headers'] = crawler_result.response_headers

        if hasattr(crawler_result, 'status_code'):
            metadata['status_code'] = crawler_result.status_code

        return metadata

    def get_spa_processing_stats(self, content: str) -> Dict[str, Any]:
        """
        获取SPA页面处理统计信息

        Args:
            content: 页面内容

        Returns:
            Dict: 统计信息
        """
        return {
            'content_length': len(content),
            'content_valid': self.validate_spa_content(content),
            'estimated_load_time': self.default_wait_time,
            'processing_type': 'spa',
            'javascript_executed': True,
            'scroll_interactions': 3,  # 滚动操作次数
        }

    def create_enhanced_spa_config(
        self,
        wait_for_selectors: Optional[list] = None,
        custom_interactions: Optional[str] = None
    ) -> CrawlerRunConfig:
        """
        创建增强的SPA配置，支持更复杂的交互

        Args:
            wait_for_selectors: 等待特定选择器出现
            custom_interactions: 自定义交互代码

        Returns:
            CrawlerRunConfig: 增强的爬虫配置
        """
        # 构建基础JavaScript代码
        js_parts = [
            "// SPA页面增强处理",
            "await new Promise(resolve => setTimeout(resolve, 3000));"
        ]

        # 添加选择器等待逻辑
        if wait_for_selectors:
            for selector in wait_for_selectors:
                js_parts.append(f"""
                // 等待选择器: {selector}
                let retries = 0;
                while (retries < 10 && !document.querySelector('{selector}')) {{
                    await new Promise(resolve => setTimeout(resolve, 500));
                    retries++;
                }}
                """)

        # 添加标准滚动交互
        js_parts.extend([
            "// 标准滚动交互",
            "window.scrollTo(0, document.body.scrollHeight);",
            "await new Promise(resolve => setTimeout(resolve, 3000));",
            "window.scrollTo(0, document.body.scrollHeight / 2);",
            "await new Promise(resolve => setTimeout(resolve, 2000));",
            "window.scrollTo(0, 0);",
            "await new Promise(resolve => setTimeout(resolve, 2000));"
        ])

        # 添加自定义交互
        if custom_interactions:
            js_parts.append("// 自定义交互")
            js_parts.append(custom_interactions)

        # 添加通用展开按钮点击
        js_parts.extend([
            "// 通用展开按钮处理",
            """
            const expandButtons = document.querySelectorAll('[class*="expand"], [class*="more"], [class*="show"]');
            for (let button of expandButtons) {
                if (button.click) button.click();
            }
            await new Promise(resolve => setTimeout(resolve, 1000));
            """
        ])

        combined_js = "\n".join(js_parts)

        return CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            wait_for="body",
            delay_before_return_html=self.default_wait_time,
            page_timeout=self.page_timeout,
            js_code=combined_js
        )