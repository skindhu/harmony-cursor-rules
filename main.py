#!/usr/bin/env python3
"""
HarmonyOS界面开发最佳实践爬虫
专门针对华为开发者官网的SPA页面进行优化

用法：
- 默认运行：python main.py
- 调试模式：python main.py --debug  (保存HTML文件)
"""

import asyncio
import os
import json
import time
from pathlib import Path
from typing import Dict, Any
from config import ConfigManager
from ai import ContentProcessor
from crawler import WebCrawler
from batch import BatchProcessor
from arkts_lint import ArkTSRulesExtractor


class SPACrawler:
    def __init__(self, config_manager: ConfigManager = None):
        # 使用配置管理器
        if config_manager is None:
            config_manager = ConfigManager.from_command_line()
        self.config_manager = config_manager

        # 从配置管理器获取配置
        self.output_dir = self.config_manager.get_output_directory()
        self.debug = self.config_manager.is_debug_mode()

        # 初始化AI内容处理器
        self.content_processor = ContentProcessor()
        if self.content_processor.is_api_available():
            print("✅ AI内容处理器初始化成功")
        else:
            print("⚠️ AI内容处理器初始化失败，将跳过AI处理功能")

        # 初始化核心爬虫
        self.web_crawler = WebCrawler(
            config_manager=self.config_manager,
            content_processor=self.content_processor
        )
        print("✅ 核心爬虫模块初始化成功")

        # 初始化批量处理器
        self.batch_processor = BatchProcessor(
            web_crawler=self.web_crawler,
            output_dir=self.output_dir
        )
        print("✅ 批量处理器初始化成功")

        # 初始化ArkTS规则提取器
        self.arkts_extractor = ArkTSRulesExtractor(
            web_crawler=self.web_crawler,
            gemini_api=self.content_processor.gemini_api,
            output_dir=self.output_dir
        )
        print("✅ ArkTS规则提取器初始化成功")





    async def crawl_with_directory_structure(self, target_dir: Path, url: str, module_name: str, sub_module_name: str) -> Dict[str, Any]:
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
        return await self.web_crawler.crawl_with_directory_structure(
            target_dir=target_dir,
            url=url,
            module_name=module_name,
            sub_module_name=sub_module_name
        )



    async def crawl_spa_page(self, url: str, module_name: str = None) -> Dict[str, Any]:
        """
        爬取SPA页面，直接保存原始HTML内容

        Args:
            url: 目标URL
            module_name: 模块名称，用于文件命名
        """
        return await self.web_crawler.crawl_spa_page_legacy(
            url=url,
            module_name=module_name
        )



    async def crawl_all_harmony_modules(self, config_file: str = "harmony_modules_config.json"):
        """
        根据配置文件爬取所有HarmonyOS模块

        Args:
            config_file: 配置文件路径
        """
        return await self.batch_processor.process_harmony_modules(config_file)

    async def integrate_best_practices(self, config_file: str = "harmony_modules_config.json"):
        """
        整合每个一级目录中的所有最佳实践，生成符合Cursor Rules格式的规范文件

        Args:
            config_file: 配置文件路径
        """
        return await self.batch_processor.integrate_all_best_practices(config_file)

    async def extract_arkts_rules(self) -> Dict[str, Any]:
        """
        提取ArkTS Lint规则

        Returns:
            Dict: 提取结果
        """
        # 检查文件是否已存在
        arkts_rules_file = self.output_dir / "final_cursor_rules" / "arkts-lint-rules.md"
        if arkts_rules_file.exists():
            print("📋 ArkTS规则文件已存在，跳过提取")
            return {
                "success": True,
                "message": "文件已存在，跳过提取",
                "output_file": str(arkts_rules_file),
                "skipped": True
            }

        print("\n" + "="*60)
        print("🎯 开始提取ArkTS Lint规则")
        print("="*60)

        # 执行提取
        result = await self.arkts_extractor.extract_arkts_rules_from_url()

        if result.get("success", False):
            print(f"✅ ArkTS规则提取成功！")
            print(f"📄 输出文件: {result.get('output_file', 'N/A')}")
            print(f"📊 提取规则数量: {result.get('rules_count', 0)}")
        else:
            print(f"❌ ArkTS规则提取失败")
            print(f"❌ 错误信息: {result.get('error', '未知错误')}")

        return result





async def main():
    """主函数"""
    # 创建配置管理器
    config_manager = ConfigManager.from_command_line()

    # 创建爬虫实例
    crawler = SPACrawler(config_manager)

    # 打印启动信息
    config_manager.print_startup_info()

    results = await crawler.crawl_all_harmony_modules()

    if results:
        successful_count = len([r for r in results if r.get("success")])
        total_count = len(results)

        print(f"\n🎊 爬取任务完成！")
        print(f"📊 成功率: {successful_count}/{total_count} ({successful_count/total_count*100:.1f}%)")
        print("\n✨ 所有HarmonyOS界面开发最佳实践已整理完成！")

        # 执行最佳实践整合，生成Cursor Rules
        if successful_count > 0:
            integration_results = await crawler.integrate_best_practices()
            if integration_results:
                successful_integrations = len([r for r in integration_results if r['success']])
                print(f"\n🎯 Cursor Rules生成完成！成功整合 {successful_integrations} 个一级模块")
            else:
                print(f"\n⚠️ Cursor Rules整合跳过或失败")

        # 提取ArkTS Lint规则
        arkts_result = await crawler.extract_arkts_rules()
        if arkts_result.get("success", False):
            if arkts_result.get("skipped", False):
                print(f"\n⏭️ ArkTS规则文件已存在，跳过提取")
            else:
                print(f"\n🎊 ArkTS规则提取完成！")
                print(f"📊 提取了 {arkts_result.get('rules_count', 0)} 个规则")
        else:
            print(f"\n⚠️ ArkTS规则提取失败: {arkts_result.get('error', '未知错误')}")
    else:
        print("\n❌ 爬取任务失败，请检查配置文件和网络连接")

    # 如果需要单独测试某个URL，可以使用以下代码：
    # test_url = "https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-ui-dynamic-operations"
    # result = await crawler.crawl_spa_page(test_url, "test_module")
    # print(f"单个测试结果: {result}")


if __name__ == "__main__":
    asyncio.run(main())