"""
ArkTS规则提取器模块
从华为开发者文档中提取arkts-no-*规则并格式化为cursor rules
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from crawler import WebCrawler
from config import ConfigManager
from gemini_api import GeminiAPI


class ArkTSRulesExtractor:
    """ArkTS规则提取器"""

    def __init__(self, web_crawler: WebCrawler, gemini_api: GeminiAPI, output_dir: Path = None):
        """
        初始化规则提取器

        Args:
            web_crawler: 网页爬虫实例
            gemini_api: Gemini API实例
            output_dir: 输出目录路径，默认为None时使用默认路径
        """
        self.web_crawler = web_crawler
        self.gemini_api = gemini_api

        # 设置输出目录
        if output_dir is None:
            self.output_dir = Path("harmony_cursor_rules/final_cursor_rules")
        else:
            self.output_dir = output_dir / "final_cursor_rules"

        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def extract_arkts_rules_from_url(
        self,
        url: str = "https://developer.huawei.com/consumer/en/doc/harmonyos-guides-V14/typescript-to-arkts-migration-guide-V14"
    ) -> Dict[str, Any]:
        """
        从指定URL提取ArkTS规则

        Args:
            url: 目标URL

        Returns:
            Dict: 提取结果
        """
        print("🚀 开始提取ArkTS Lint规则")
        print("=" * 50)
        print(f"📄 目标页面: {url}")

        # 爬取页面
        crawl_result = await self.web_crawler.crawl_single_page(
            url=url,
            module_name="arkts_migration_guide",
            use_spa_mode=True,
            extract_best_practices=False
        )

        if not crawl_result.get('success', False):
            error_msg = crawl_result.get('error', '未知错误')
            print(f"❌ 页面爬取失败: {error_msg}")
            return {
                "success": False,
                "error": f"页面爬取失败: {error_msg}",
                "rules_count": 0
            }

        print("✅ 页面爬取成功")

        # 从爬取结果中获取HTML内容
        html_content = self._get_html_content_from_crawl_result(crawl_result)

        if not html_content:
            print("❌ 无法获取HTML内容")
            return {
                "success": False,
                "error": "无法获取HTML内容",
                "rules_count": 0
            }

        # 提取规则 - 使用AI智能提取
        rules_result = self._extract_arkts_rules_with_ai(html_content)

        if not rules_result.get("success", False):
            error_msg = rules_result.get("error", "AI提取失败")
            print(f"⚠️ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "rules_count": 0
            }

        rules = rules_result.get("rules", [])

        if not rules:
            print("⚠️ 未找到任何arkts-no-*规则")
            return {
                "success": False,
                "error": "未找到任何arkts-no-*规则",
                "rules_count": 0
            }

        print(f"📋 找到 {len(rules)} 个ArkTS规则")

        # 生成cursor rules文件
        markdown_content = self._generate_cursor_rules_markdown(rules)

        # 保存文件
        output_file = self.output_dir / "arkts-lint-rules.md"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            print(f"✅ 规则文件已保存: {output_file}")
            return {
                "success": True,
                "output_file": str(output_file),
                "rules_count": len(rules),
                "rules": rules
            }

        except Exception as e:
            print(f"❌ 文件保存失败: {e}")
            return {
                "success": False,
                "error": f"文件保存失败: {e}",
                "rules_count": len(rules)
            }

    def _get_html_content_from_crawl_result(self, crawl_result: Dict[str, Any]) -> Optional[str]:
        """
        从爬取结果中获取HTML内容

        Args:
            crawl_result: 爬取结果

        Returns:
            Optional[str]: HTML内容
        """
        # 优先从爬取结果中直接获取HTML内容
        html_content = crawl_result.get('html_content')
        if html_content:
            return html_content


        return None

    def _extract_arkts_rules_with_ai(self, html_content: str) -> Dict[str, Any]:
        """
        使用AI从HTML内容中提取arkts-no-*规则

        Args:
            html_content: HTML内容

        Returns:
            Dict: 提取结果，包含success和rules字段
        """
        try:
            # 使用BeautifulSoup清理HTML，提取纯文本
            soup = BeautifulSoup(html_content, 'html.parser')

            # 移除script和style标签
            for script in soup(["script", "style"]):
                script.decompose()

            # 获取纯文本内容
            text_content = soup.get_text()

            print(f"📝 准备AI提取，文本长度: {len(text_content)} 字符")

            # 构建AI提示词
            extraction_prompt = self._build_arkts_extraction_prompt(text_content)

            # 直接使用Gemini API提取规则
            ai_response = self.gemini_api.generate_text(extraction_prompt)

            if not ai_response:
                return {
                    "success": False,
                    "error": "AI未返回任何内容"
                }

            # 解析AI返回的规则
            rules = self._parse_ai_response_text(ai_response)

            if not rules:
                return {
                    "success": False,
                    "error": "AI未能提取到有效的arkts-no-*规则"
                }

            print(f"🤖 AI成功提取 {len(rules)} 个规则")

            return {
                "success": True,
                "rules": rules,
                "rules_count": len(rules)
            }

        except Exception as e:
            print(f"❌ AI提取过程发生错误: {e}")
            return {
                "success": False,
                "error": f"AI提取过程错误: {str(e)}"
            }

    def _build_arkts_extraction_prompt(self, content: str) -> str:
        """
        构建ArkTS规则提取的AI提示词

        Args:
            content: 页面文本内容

        Returns:
            str: AI提示词
        """
        prompt = f"""
请从以下华为HarmonyOS ArkTS迁移指南内容中，提取所有的ArkTS Lint规则（以"arkts-no-"开头的规则）。

任务要求：
1. 找出所有以"arkts-no-"开头的规则名称
2. 为每个规则提取对应的描述信息
3. 规则名称统一转换为小写
4. 按照指定的JSON格式返回

请仔细阅读以下内容并提取规则：

{content}

请以以下JSON格式返回提取的规则：
```json
[
  {{
    "name": "arkts-no-xxx",
    "severity": "error",
    "description": "规则的详细描述",
    "suggestion": "建议的替代实践方式"
  }},
  {{
    "name": "arkts-no-yyy",
    "severity": "error",
    "description": "规则的详细描述",
    "suggestion": "建议的替代实践方式"
  }}
]
```

注意事项：
- 只提取以"arkts-no-"开头的规则
- 确保每个规则都有清晰的描述和建议
- 规则名称必须完整且准确
- 描述要简洁明了，说明该规则的作用
- suggestion字段要提供具体的替代方案或最佳实践
- 如果同一个规则出现多次，只保留一次
- 严重程度统一设置为"error"
"""
        return prompt

    def _parse_ai_response_text(self, ai_response: str) -> List[Dict[str, str]]:
        """
        解析AI返回的文本，提取ArkTS规则

        Args:
            ai_response: AI返回的原始文本

        Returns:
            List[Dict]: 解析后的规则列表
        """
        rules = []

        try:
            # 首先尝试从JSON格式中提取
            rules.extend(self._extract_rules_from_json_text(ai_response))

            # 如果没有JSON，尝试从纯文本中提取
            if not rules:
                rules.extend(self._extract_rules_from_plain_text(ai_response))

            # 去重和排序
            unique_rules = self._deduplicate_rules(rules)

            return unique_rules

        except Exception as e:
            print(f"⚠️ 解析AI结果时发生错误: {e}")
            return []

    def _extract_rules_from_json_text(self, text: str) -> List[Dict[str, str]]:
        """
        从文本中提取JSON格式的规则

        Args:
            text: 包含JSON的文本

        Returns:
            List[Dict]: 规则列表
        """
        rules = []

        try:
            # 查找JSON代码块
            json_pattern = r'```json\s*(.*?)\s*```'
            json_matches = re.findall(json_pattern, text, re.DOTALL)

            for json_text in json_matches:
                try:
                    parsed_rules = json.loads(json_text)
                    if isinstance(parsed_rules, list):
                        for rule in parsed_rules:
                            if self._is_valid_arkts_rule(rule):
                                rules.append(rule)
                except json.JSONDecodeError:
                    continue

            # 如果没找到代码块，尝试直接解析整个文本
            if not rules:
                try:
                    parsed_rules = json.loads(text)
                    if isinstance(parsed_rules, list):
                        for rule in parsed_rules:
                            if self._is_valid_arkts_rule(rule):
                                rules.append(rule)
                except json.JSONDecodeError:
                    pass

        except Exception as e:
            print(f"⚠️ JSON解析错误: {e}")

        return rules

    def _extract_rules_from_plain_text(self, text: str) -> List[Dict[str, str]]:
        """
        从纯文本中提取规则（备用方法）

        Args:
            text: 纯文本内容

        Returns:
            List[Dict]: 规则列表
        """
        rules = []

        # 使用正则表达式查找arkts-no-*规则
        pattern = r'(arkts-no-[\w-]+)[:\s]*([^\n\r]+)'
        matches = re.findall(pattern, text, re.IGNORECASE)

        for rule_name, description in matches:
            rule_name = rule_name.lower()
            description = description.strip()

            if len(description) > 10:  # 过滤太短的描述
                # 从描述中尝试提取建议（如果有）
                suggestion = "Use ArkTS-compatible alternatives as specified in the documentation."
                if "Use " in description or "use " in description:
                    # 如果描述中包含建议，提取后半部分作为suggestion
                    parts = description.split("Use ", 1)
                    if len(parts) > 1:
                        suggestion = "Use " + parts[1]
                        description = parts[0].rstrip(" .;,")

                rules.append({
                    "name": rule_name,
                    "severity": "error",
                    "description": description,
                    "suggestion": suggestion
                })

        return rules

    def _is_valid_arkts_rule(self, rule: Dict[str, Any]) -> bool:
        """
        验证规则是否有效

        Args:
            rule: 规则字典

        Returns:
            bool: 是否有效
        """
        if not isinstance(rule, dict):
            return False

        name = rule.get("name", "")
        description = rule.get("description", "")
        suggestion = rule.get("suggestion", "")

        return (
            isinstance(name, str) and
            name.lower().startswith("arkts-no-") and
            isinstance(description, str) and
            len(description.strip()) > 5 and
            isinstance(suggestion, str) and
            len(suggestion.strip()) > 5
        )

    def _deduplicate_rules(self, rules: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        去重规则

        Args:
            rules: 规则列表

        Returns:
            List[Dict]: 去重后的规则列表
        """
        seen_names = set()
        unique_rules = []

        for rule in rules:
            name = rule["name"]
            if name not in seen_names:
                seen_names.add(name)
                unique_rules.append(rule)

        # 按名称排序
        unique_rules.sort(key=lambda x: x["name"])

        return unique_rules

    def _generate_cursor_rules_markdown(self, rules: List[Dict[str, str]]) -> str:
        """
        生成cursor rules格式的markdown内容

        Args:
            rules: 规则列表

        Returns:
            str: markdown内容
        """
        # 将规则转换为JSON格式
        rules_json = json.dumps(rules, indent=2, ensure_ascii=False)

        markdown_content = f"""# ArkTS Lint Rules - Cursor Rules

## 概述
ArkTS（TypeScript的子集）的Lint规则，用于确保代码符合HarmonyOS开发规范。

## 规则统计
- 总规则数量: {len(rules)}
- 严重程度: error
- 适用范围: ArkTS/TypeScript代码

## 规则列表

### JSON格式
```json
{rules_json}
```

## 使用说明

### 在Cursor中使用
1. 将此文件保存为 `.cursorrules` 文件
2. 配置TypeScript/ArkTS项目的ESLint规则
3. 确保IDE能够识别这些规则

### 规则应用
这些规则主要用于：
- TypeScript到ArkTS的迁移
- HarmonyOS应用开发
- 确保代码符合ArkTS规范

## 参考资源
- [HarmonyOS ArkTS开发指南](https://developer.huawei.com/consumer/en/doc/harmonyos-guides-V14/typescript-to-arkts-migration-guide-V14)
- 生成时间: {self._get_current_time()}

---
*此文件由ArkTS规则提取器自动生成*
"""

        return markdown_content

    def _get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_extractor_stats(self) -> Dict[str, Any]:
        """
        获取提取器统计信息

        Returns:
            Dict: 统计信息
        """
        return {
            'web_crawler_ready': self.web_crawler is not None,
            'ai_processor_ready': self.gemini_api is not None,
            'output_directory': str(self.output_dir),
            'output_directory_exists': self.output_dir.exists(),
            'extraction_method': 'AI-powered (Gemini)'
        }
