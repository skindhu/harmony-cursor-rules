"""
批量处理模块
专门处理批量爬取任务，包括进度管理、统计汇总、结果整理等
"""

import asyncio
import time
from pathlib import Path
from typing import Dict, Any, List
from crawler import WebCrawler
from module_manager import HarmonyModuleManager
from utils import DisplayHelper, StatisticsHelper
from ai import ContentProcessor


class BatchProcessor:
    """批量处理器类"""

    def __init__(self, web_crawler: WebCrawler, output_dir: Path):
        """
        初始化批量处理器

        Args:
            web_crawler: 网页爬虫实例
            output_dir: 输出目录
        """
        self.web_crawler = web_crawler
        self.output_dir = output_dir
        self.content_processor = web_crawler.content_processor

    async def process_harmony_modules(
        self,
        config_file: str = "harmony_modules_config.json"
    ) -> List[Dict[str, Any]]:
        """
        批量处理HarmonyOS模块

        Args:
            config_file: 配置文件路径

        Returns:
            List: 处理结果列表
        """
        print("🚀 开始HarmonyOS模块完整爬取")
        print("=" * 80)

        # 初始化模块管理器
        module_manager = HarmonyModuleManager(config_file)

        # 验证配置文件
        is_valid, errors = module_manager.validate_config()
        if not is_valid:
            print("❌ 配置文件验证失败:")
            for error in errors:
                print(f"  - {error}")
            return []

        # 创建目录结构
        module_manager.create_directory_structure(self.output_dir)

        # 获取所有模块信息
        grouped_modules = module_manager.get_modules_by_category()
        total_modules = module_manager.get_total_module_count()

        print(f"📊 总共需要爬取 {total_modules} 个模块")
        print("=" * 80)

        all_results = []
        current_index = 0

        # 遍历所有一级模块
        for category_name, modules_in_category in grouped_modules.items():
            print(f"\n📂 开始处理一级模块: {category_name}")
            print(f"📁 目录: {modules_in_category[0]['category_directory']}")
            print("-" * 60)

            category_dir = self.output_dir / modules_in_category[0]['category_directory']
            category_results = []

            # 遍历该一级模块下的所有二级模块
            for module_info in modules_in_category:
                current_index += 1
                print(f"\n  🔄 [{current_index}/{total_modules}] {module_info['sub_module_name']}")

                result = await self.web_crawler.crawl_with_directory_structure(
                    target_dir=category_dir,
                    url=module_info["url"],
                    module_name=module_info["module_name"],
                    sub_module_name=module_info["sub_module_name"]
                )

                result["category_name"] = category_name
                result["category_dir"] = module_info["category_directory"]
                category_results.append(result)
                all_results.append(result)

                # 简化结果显示
                display_text = DisplayHelper.format_result_display(result)
                print(f"    {display_text}")

                # 添加延迟避免频繁请求
                if current_index < total_modules:
                    await asyncio.sleep(3)

            # 输出当前一级模块汇总
            self._display_category_summary(category_name, category_results)

        # 输出最终汇总
        self._display_final_summary(all_results, grouped_modules)

        return all_results

    def _display_category_summary(self, category_name: str, category_results: List[Dict[str, Any]]):
        """
        显示一级模块汇总信息

        Args:
            category_name: 分类名称
            category_results: 分类结果列表
        """
        successful_in_category, failed_in_category, skipped_in_category, new_in_category = \
            StatisticsHelper.categorize_results(category_results)

        summary_text = DisplayHelper.format_category_summary(
            category_name, len(successful_in_category), len(category_results),
            len(new_in_category), len(skipped_in_category)
        )
        print(f"\n{summary_text}")

        if failed_in_category:
            print(f"❌ 失败模块:")
            for result in failed_in_category:
                print(f"  - {result.get('sub_module_name', '未知')}: {result.get('error', '未知错误')}")

    def _display_final_summary(self, all_results: List[Dict[str, Any]], grouped_modules: Dict):
        """
        显示最终汇总信息

        Args:
            all_results: 所有结果列表
            grouped_modules: 分组模块信息
        """
        print("\n" + "=" * 50)
        print("🎉 HarmonyOS模块完整爬取完成！")
        print("=" * 50)

        # 使用统计工具生成最终统计
        final_stats = StatisticsHelper.generate_final_statistics(all_results)

        print(f"📊 最终统计:")
        print(f"✅ 总成功: {final_stats['successful']} 个")
        print(f"  🆕 新爬取: {final_stats['new']} 个")
        print(f"  ⏭️ 已跳过: {final_stats['skipped']} 个")
        print(f"❌ 总失败: {final_stats['failed']} 个")
        print(f"📈 成功率: {final_stats['success_rate']:.1f}%")

        # 按一级模块汇总
        print(f"\n📁 按一级模块汇总:")
        grouped_results = StatisticsHelper.group_results_by_category(all_results)
        for category_name in grouped_modules.keys():
            if category_name in grouped_results:
                category_results = grouped_results[category_name]
                successful, failed, skipped, new = StatisticsHelper.categorize_results(category_results)
                print(f"  - {category_name}: {len(successful)}/{len(category_results)} 成功 (新:{len(new)}, 跳过:{len(skipped)})")

        print(f"\n📁 文件保存位置: {self.output_dir}")
        if self.web_crawler.debug_mode:
            print(f"🔧 调试模式: HTML文件已保存")
        print("=" * 50)

    async def integrate_all_best_practices(
        self,
        config_file: str = "harmony_modules_config.json"
    ) -> List[Dict[str, Any]]:
        """
        整合所有最佳实践为Cursor Rules格式

        Args:
            config_file: 配置文件路径

        Returns:
            List: 整合结果列表
        """
        print("\n" + "=" * 50)
        print("🔄 开始整合最佳实践为Cursor Rules")
        print("=" * 50)

        # 初始化模块管理器
        module_manager = HarmonyModuleManager(config_file)

        # 验证配置文件
        is_valid, errors = module_manager.validate_config()
        if not is_valid:
            print("❌ 配置文件验证失败:")
            for error in errors:
                print(f"  - {error}")
            return []

        # 创建最终输出目录
        final_output_dir = Path("harmony_cursor_rules/final_cursor_rules")
        final_output_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 最终输出目录: {final_output_dir}")

        # 获取所有一级模块信息
        grouped_modules = module_manager.get_modules_by_category()
        integration_results = []

        # 遍历每个一级模块
        for category_name, modules_in_category in grouped_modules.items():
            print(f"\n📂 整合一级模块: {category_name}")

            # 获取该一级模块的目录和directory名称
            category_dir = self.output_dir / modules_in_category[0]['category_directory']
            directory_name = modules_in_category[0]['category_directory']  # 使用directory名称

            if not category_dir.exists():
                print(f"⚠️ 目录不存在: {category_dir}")
                continue

            # 查找所有.md文件
            md_files = list(category_dir.glob("*.md"))

            if not md_files:
                print(f"⚠️ 未找到任何.md文件")
                integration_results.append({
                    "category_name": category_name,
                    "directory_name": directory_name,
                    "success": False,
                    "error": "未找到任何.md文件"
                })
                continue

            print(f"📄 找到 {len(md_files)} 个最佳实践文件")

            # 读取所有最佳实践内容
            all_practices = []
            for md_file in md_files:
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():
                            all_practices.append({
                                "filename": md_file.name,
                                "content": content
                            })
                except Exception as e:
                    print(f"⚠️ 读取文件失败 {md_file.name}: {e}")

            if not all_practices:
                print(f"⚠️ 没有有效的最佳实践内容")
                integration_results.append({
                    "category_name": category_name,
                    "directory_name": directory_name,
                    "success": False,
                    "error": "没有有效的最佳实践内容"
                })
                continue

            # 使用AI内容处理器整合最佳实践
            if self.content_processor.is_api_available():
                integrated_content = self.content_processor.integrate_practices(
                    module_name=category_name,
                    practices=all_practices
                )

                if integrated_content:
                    # 使用directory名称作为文件名，保存到final_cursor_rules目录
                    output_file = final_output_dir / f"{directory_name}.cursorrules.md"
                    try:
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(integrated_content)

                        print(f"✅ 整合成功: {output_file.name} -> {final_output_dir}")
                        integration_results.append({
                            "category_name": category_name,
                            "directory_name": directory_name,
                            "success": True,
                            "output_file": str(output_file),
                            "practices_count": len(all_practices)
                        })
                    except Exception as e:
                        print(f"❌ 文件保存失败: {e}")
                        integration_results.append({
                            "category_name": category_name,
                            "directory_name": directory_name,
                            "success": False,
                            "error": f"文件保存失败: {e}"
                        })
                else:
                    print(f"❌ AI整合失败")
                    integration_results.append({
                        "category_name": category_name,
                        "directory_name": directory_name,
                        "success": False,
                        "error": "AI整合失败"
                    })
            else:
                print(f"⚠️ AI功能不可用，跳过整合")
                integration_results.append({
                    "category_name": category_name,
                    "directory_name": directory_name,
                    "success": False,
                    "error": "AI功能不可用"
                })

        # 输出整合汇总
        self._display_integration_summary(integration_results, final_output_dir)

        return integration_results

    def _display_integration_summary(self, integration_results: List[Dict[str, Any]], final_output_dir: Path):
        """
        显示整合汇总信息

        Args:
            integration_results: 整合结果列表
            final_output_dir: 最终输出目录
        """
        print("\n" + "=" * 50)
        print("🎉 最佳实践整合完成！")
        print("=" * 50)

        successful = [r for r in integration_results if r.get('success', False)]
        failed = [r for r in integration_results if not r.get('success', False)]

        print(f"📊 整合统计:")
        print(f"✅ 成功: {len(successful)} 个")
        print(f"❌ 失败: {len(failed)} 个")
        print(f"📈 成功率: {len(successful)/len(integration_results)*100:.1f}%")

        if successful:
            print(f"\n✅ 成功整合的模块:")
            for result in successful:
                practices_count = result.get('practices_count', 0)
                directory_name = result.get('directory_name', result['category_name'])
                print(f"  - {directory_name}.cursorrules.md: {practices_count} 个最佳实践")

        if failed:
            print(f"\n❌ 失败的模块:")
            for result in failed:
                error = result.get('error', '未知错误')
                directory_name = result.get('directory_name', result['category_name'])
                print(f"  - {directory_name}: {error}")

        print(f"\n📁 最终文件保存位置: {final_output_dir}")
        print("=" * 50)

    async def process_url_list(
        self,
        urls: List[str],
        delay_between_requests: float = 3.0,
        use_spa_mode: bool = True
    ) -> List[Dict[str, Any]]:
        """
        批量处理URL列表

        Args:
            urls: URL列表
            delay_between_requests: 请求间延迟
            use_spa_mode: 是否使用SPA模式

        Returns:
            List: 处理结果列表
        """
        print(f"🚀 开始批量处理 {len(urls)} 个URL")
        print("=" * 50)

        results = []

        for i, url in enumerate(urls):
            print(f"\n🔄 [{i+1}/{len(urls)}] 处理URL: {url}")

            result = await self.web_crawler.crawl_single_page(
                url=url,
                use_spa_mode=use_spa_mode
            )
            results.append(result)

            # 显示结果
            if result.get('success', False):
                print(f"✅ 成功: {result.get('module_name', '未知')}")
            else:
                print(f"❌ 失败: {result.get('error', '未知错误')}")

            # 添加延迟
            if i < len(urls) - 1:
                await asyncio.sleep(delay_between_requests)

        # 输出汇总
        successful = [r for r in results if r.get('success', False)]
        failed = [r for r in results if not r.get('success', False)]

        print(f"\n📊 批量处理完成:")
        print(f"✅ 成功: {len(successful)} 个")
        print(f"❌ 失败: {len(failed)} 个")
        print(f"📈 成功率: {len(successful)/len(results)*100:.1f}%")

        return results

    def get_processing_stats(self) -> Dict[str, Any]:
        """
        获取批量处理统计信息

        Returns:
            Dict: 统计信息
        """
        return {
            'web_crawler_ready': self.web_crawler is not None,
            'output_directory': str(self.output_dir),
            'output_directory_exists': self.output_dir.exists(),
            'ai_available': self.content_processor.is_api_available() if self.content_processor else False,
            'debug_mode': self.web_crawler.debug_mode if self.web_crawler else False
        }