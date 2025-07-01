"""
AI内容处理器模块
提供最佳实践提取和整合功能
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from gemini_api import GeminiAPI
from .prompts import PromptBuilder


class BestPracticesExtractor:
    """最佳实践提取器"""

    def __init__(self, gemini_api: GeminiAPI):
        """
        初始化提取器

        Args:
            gemini_api: Gemini API实例
        """
        self.gemini_api = gemini_api
        self.prompt_builder = PromptBuilder()

    def extract_from_html(
        self,
        html_content: str,
        module_name: str,
        title: str,
        url: str
    ) -> str:
        """
        从HTML内容中提取最佳实践

        Args:
            html_content: HTML页面内容
            module_name: 模块名称
            title: 页面标题
            url: 源URL

        Returns:
            str: 生成的最佳实践markdown内容
        """
        if not self.gemini_api:
            return self._get_no_api_fallback(module_name, url)

        try:
            # 构建提示词
            prompt = self.prompt_builder.build_extraction_prompt(
                title=title,
                module_name=module_name,
                url=url,
                html_content=html_content
            )

            # 调用Gemini API生成最佳实践
            best_practices = self.gemini_api.generate_text(prompt)
            return best_practices

        except Exception as e:
            return self.prompt_builder.build_error_fallback(
                module_name=module_name,
                error_message=str(e),
                context="最佳实践提取"
            )

    def _get_no_api_fallback(self, module_name: str, url: str) -> str:
        """
        API不可用时的回退内容

        Args:
            module_name: 模块名称
            url: 源URL

        Returns:
            str: 回退内容
        """
        return f"""# {module_name.replace('_', ' ').title()} - 最佳实践

## 📋 概述
无法自动提取最佳实践，Gemini API未初始化。

## 🔗 原始资源
- 源链接：{url}
- HTML文件：{module_name}.html

请手动查看HTML文件获取完整内容并提取最佳实践。
"""


class PracticesIntegrator:
    """实践整合器"""

    def __init__(self, gemini_api: GeminiAPI):
        """
        初始化整合器

        Args:
            gemini_api: Gemini API实例
        """
        self.gemini_api = gemini_api
        self.prompt_builder = PromptBuilder()

    def integrate_practices(
        self,
        module_name: str,
        practices: List[Dict[str, str]],
        max_content_per_practice: int = 2000
    ) -> str:
        """
        整合多个最佳实践为Cursor Rules格式

        Args:
            module_name: 一级模块名称
            practices: 最佳实践列表，每个元素包含filename和content
            max_content_per_practice: 每个实践的最大内容长度

        Returns:
            str: 整合后的Cursor Rules内容
        """
        if not self.gemini_api or not practices:
            return self._get_no_integration_fallback(module_name)

        try:
            # 构建所有实践内容的摘要
            practices_summary = self._build_practices_summary(
                practices, max_content_per_practice
            )

            # 构建整合提示词
            prompt = self.prompt_builder.build_integration_prompt(
                module_name=module_name,
                practices_content=practices_summary
            )

            # 调用Gemini API生成整合的Cursor Rules
            integrated_content = self.gemini_api.generate_text(prompt)
            return integrated_content

        except Exception as e:
            return self.prompt_builder.build_integration_error(
                module_name=module_name,
                error_message=str(e)
            )

    def _build_practices_summary(
        self,
        practices: List[Dict[str, str]],
        max_content_length: int
    ) -> str:
        """
        构建实践内容摘要

        Args:
            practices: 实践列表
            max_content_length: 每个实践的最大内容长度

        Returns:
            str: 实践摘要内容
        """
        practices_summary = []
        for practice in practices:
            # 提取每个实践的关键信息，限制长度避免超出token限制
            content_preview = practice['content'][:max_content_length]
            practices_summary.append(f"### {practice['filename']}\n{content_preview}\n")

        return "\n".join(practices_summary)

    def _get_no_integration_fallback(self, module_name: str) -> str:
        """
        无法整合时的回退内容

        Args:
            module_name: 模块名称

        Returns:
            str: 回退内容
        """
        return f"""# HarmonyOS {module_name} - Cursor Rules

## 说明
无法自动整合最佳实践，请手动处理。

## 原始资源
请查看该目录下的各个最佳实践文件获取详细内容。

## 手动整合建议
1. 提取各子模块的核心原则
2. 合并相似的最佳实践
3. 突出关键的代码模式
4. 列出明确的禁止事项
"""


class ContentProcessor:
    """内容处理器主类"""

    def __init__(self, gemini_api: Optional[GeminiAPI] = None):
        """
        初始化内容处理器

        Args:
            gemini_api: Gemini API实例，如果为None则自动初始化
        """
        if gemini_api is None:
            try:
                self.gemini_api = GeminiAPI()
                self.api_available = True
            except Exception as e:
                print(f"⚠️ Gemini API 初始化失败: {e}")
                self.gemini_api = None
                self.api_available = False
        else:
            self.gemini_api = gemini_api
            self.api_available = gemini_api is not None

        # 初始化子处理器
        self.extractor = BestPracticesExtractor(self.gemini_api)
        self.integrator = PracticesIntegrator(self.gemini_api)

    def is_api_available(self) -> bool:
        """
        检查API是否可用

        Returns:
            bool: API是否可用
        """
        return self.api_available

    def extract_best_practices(
        self,
        html_content: str,
        module_name: str,
        title: str,
        url: str
    ) -> str:
        """
        提取最佳实践

        Args:
            html_content: HTML内容
            module_name: 模块名称
            title: 页面标题
            url: 源URL

        Returns:
            str: 最佳实践内容
        """
        return self.extractor.extract_from_html(
            html_content=html_content,
            module_name=module_name,
            title=title,
            url=url
        )

    def integrate_practices(
        self,
        module_name: str,
        practices: List[Dict[str, str]]
    ) -> str:
        """
        整合实践为Cursor Rules

        Args:
            module_name: 模块名称
            practices: 实践列表

        Returns:
            str: 整合后的内容
        """
        return self.integrator.integrate_practices(
            module_name=module_name,
            practices=practices
        )

    def batch_extract_from_files(
        self,
        file_contents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        批量从文件内容中提取最佳实践

        Args:
            file_contents: 文件内容列表，每个元素包含必要的信息

        Returns:
            List: 提取结果列表
        """
        results = []

        for file_info in file_contents:
            try:
                extracted_content = self.extract_best_practices(
                    html_content=file_info.get('html_content', ''),
                    module_name=file_info.get('module_name', ''),
                    title=file_info.get('title', ''),
                    url=file_info.get('url', '')
                )

                results.append({
                    'success': True,
                    'module_name': file_info.get('module_name'),
                    'content': extracted_content,
                    'content_length': len(extracted_content)
                })

            except Exception as e:
                results.append({
                    'success': False,
                    'module_name': file_info.get('module_name'),
                    'error': str(e)
                })

        return results

    def get_processing_stats(self) -> Dict[str, Any]:
        """
        获取处理统计信息

        Returns:
            Dict: 统计信息
        """
        return {
            'api_available': self.api_available,
            'extractor_ready': self.extractor is not None,
            'integrator_ready': self.integrator is not None,
            'gemini_api_configured': self.gemini_api is not None
        }