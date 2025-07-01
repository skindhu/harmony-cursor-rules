"""
工具函数模块
提供URL处理、显示格式化、统计计算等工具函数
"""

import time
from typing import List, Dict, Any, Tuple
from pathlib import Path


class URLHelper:
    """URL处理工具类"""

    @staticmethod
    def get_module_name_from_url(url: str) -> str:
        """
        从URL中提取模块名称

        Args:
            url: 目标URL

        Returns:
            str: 提取的模块名称
        """
        # 从URL中提取最后一部分作为模块名
        if "/best-practices/" in url:
            module_part = url.split("/best-practices/")[-1]
            # 移除可能的查询参数
            if "?" in module_part:
                module_part = module_part.split("?")[0]
            # 将连字符转换为下划线，便于文件命名
            return module_part.replace("-", "_")

        # 如果无法从URL提取，使用默认名称
        return f"harmony_module_{int(time.time())}"

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        验证URL格式是否正确

        Args:
            url: 待验证的URL

        Returns:
            bool: URL是否有效
        """
        return (url.startswith('http://') or url.startswith('https://')) and len(url) > 10


class DisplayHelper:
    """显示格式化工具类"""

    @staticmethod
    def format_progress_display(current: int, total: int, module_name: str) -> str:
        """
        格式化进度显示

        Args:
            current: 当前进度
            total: 总数
            module_name: 模块名称

        Returns:
            str: 格式化的进度字符串
        """
        return f"🔄 [{current}/{total}] {module_name}"

    @staticmethod
    def format_result_display(result: Dict[str, Any]) -> str:
        """
        格式化结果显示

        Args:
            result: 爬取结果字典

        Returns:
            str: 格式化的结果字符串
        """
        if not result.get("success"):
            return f"❌ 失败: {result.get('error', '未知错误')}"

        if result.get("skipped"):
            return f"⏭️ 跳过 | 已存在文件 | 内容:{result.get('content_length', 0)}字符"
        else:
            has_practices = '已生成' if result.get('has_best_practices') else '未生成'
            return f"✅ 完成 | 内容:{result.get('content_length', 0)}字符 | 最佳实践:{has_practices}"

    @staticmethod
    def format_category_summary(category_name: str, successful: int, total: int,
                              new_count: int, skipped_count: int) -> str:
        """
        格式化分类汇总显示

        Args:
            category_name: 分类名称
            successful: 成功数量
            total: 总数量
            new_count: 新增数量
            skipped_count: 跳过数量

        Returns:
            str: 格式化的汇总字符串
        """
        return f"📋 {category_name}: {successful}/{total} 成功 (新:{new_count}, 跳过:{skipped_count})"


class StatisticsHelper:
    """统计计算工具类"""

    @staticmethod
    def calculate_success_rate(results: List[Dict[str, Any]]) -> float:
        """
        计算成功率

        Args:
            results: 结果列表

        Returns:
            float: 成功率百分比
        """
        if not results:
            return 0.0

        successful_count = len([r for r in results if r.get("success")])
        return (successful_count / len(results)) * 100

    @staticmethod
    def categorize_results(results: List[Dict[str, Any]]) -> Tuple[List, List, List, List]:
        """
        对结果进行分类统计

        Args:
            results: 结果列表

        Returns:
            Tuple: (successful, failed, skipped, new) 四个列表
        """
        successful = [r for r in results if r.get("success")]
        failed = [r for r in results if not r.get("success")]
        skipped = [r for r in results if r.get("success") and r.get("skipped")]
        new = [r for r in results if r.get("success") and not r.get("skipped")]

        return successful, failed, skipped, new

    @staticmethod
    def group_results_by_category(results: List[Dict[str, Any]]) -> Dict[str, List]:
        """
        按分类对结果进行分组

        Args:
            results: 结果列表

        Returns:
            Dict: 按分类分组的结果字典
        """
        grouped = {}
        for result in results:
            category = result.get("category_name", "未知分类")
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(result)

        return grouped

    @staticmethod
    def generate_final_statistics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成最终统计信息

        Args:
            results: 结果列表

        Returns:
            Dict: 统计信息字典
        """
        successful, failed, skipped, new = StatisticsHelper.categorize_results(results)
        success_rate = StatisticsHelper.calculate_success_rate(results)

        return {
            'total': len(results),
            'successful': len(successful),
            'failed': len(failed),
            'skipped': len(skipped),
            'new': len(new),
            'success_rate': success_rate
        }


class FileHelper:
    """文件处理工具类"""

    @staticmethod
    def ensure_directory_exists(directory: Path) -> None:
        """
        确保目录存在，如果不存在则创建

        Args:
            directory: 目录路径
        """
        directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_file_info(file_path: Path) -> Dict[str, Any]:
        """
        获取文件信息

        Args:
            file_path: 文件路径

        Returns:
            Dict: 文件信息字典
        """
        if not file_path.exists():
            return {"exists": False}

        try:
            content = file_path.read_text(encoding='utf-8')
            return {
                "exists": True,
                "size": file_path.stat().st_size,
                "content_length": len(content),
                "modified_time": file_path.stat().st_mtime
            }
        except Exception as e:
            return {
                "exists": True,
                "error": str(e)
            }

    @staticmethod
    def collect_markdown_files(directory: Path, exclude_pattern: str = None) -> List[Path]:
        """
        收集目录下的markdown文件

        Args:
            directory: 目录路径
            exclude_pattern: 排除的文件名模式

        Returns:
            List[Path]: markdown文件列表
        """
        if not directory.exists():
            return []

        md_files = list(directory.glob("*.md"))

        if exclude_pattern:
            md_files = [f for f in md_files if exclude_pattern not in f.name]

        return md_files