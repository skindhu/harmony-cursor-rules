"""
文件保存处理器模块
处理HTML文件、markdown文件的保存逻辑
"""

import time
from pathlib import Path
from typing import Dict, Any, Optional
from utils import FileHelper


class FileSaver:
    """文件保存处理器"""

    def __init__(self, debug_mode: bool = False):
        """
        初始化文件保存器

        Args:
            debug_mode: 是否启用调试模式（保存HTML文件）
        """
        self.debug_mode = debug_mode

    def check_existing_files(
        self,
        target_dir: Path,
        module_name: str,
        sub_module_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        检查是否已存在相关文件

        Args:
            target_dir: 目标目录
            module_name: 模块名称
            sub_module_name: 子模块名称

        Returns:
            Dict: 如果文件已存在，返回文件信息；否则返回None
        """
        markdown_file = target_dir / f"{module_name}.md"

        if markdown_file.exists():
            # 读取文件信息
            file_info = FileHelper.get_file_info(markdown_file)
            html_file = target_dir / f"{module_name}.html" if self.debug_mode else None

            return {
                "success": True,
                "url": "",  # 这里没有URL信息，调用者需要填充
                "title": sub_module_name,
                "module_name": module_name,
                "sub_module_name": sub_module_name,
                "html_file": str(html_file) if (html_file and html_file.exists()) else None,
                "markdown_file": str(markdown_file),
                "content_length": file_info.get('content_length', 0),
                "has_best_practices": True,
                "skipped": True  # 标记为跳过
            }

        return None

    def save_html_file(
        self,
        target_dir: Path,
        module_name: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> Optional[Path]:
        """
        保存HTML文件（仅在调试模式下）

        Args:
            target_dir: 目标目录
            module_name: 模块名称
            content: HTML内容
            metadata: 元数据信息

        Returns:
            Path: 保存的文件路径，如果未保存则返回None
        """
        if not self.debug_mode:
            return None

        FileHelper.ensure_directory_exists(target_dir)
        html_file = target_dir / f"{module_name}.html"

        try:
            with open(html_file, 'w', encoding='utf-8') as f:
                # 添加元信息作为注释
                f.write("<!-- \n")
                f.write(f"页面标题: {metadata.get('title', '未知')}\n")
                f.write(f"源链接: {metadata.get('url', '未知')}\n")
                f.write(f"爬取时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"模块名称: {module_name}\n")
                if 'sub_module_name' in metadata:
                    f.write(f"子模块名称: {metadata['sub_module_name']}\n")
                f.write("-->\n\n")
                f.write(content)

            return html_file

        except Exception as e:
            print(f"⚠️ HTML文件保存失败: {e}")
            return None

    def save_markdown_file(
        self,
        target_dir: Path,
        module_name: str,
        content: str
    ) -> Optional[Path]:
        """
        保存markdown文件

        Args:
            target_dir: 目标目录
            module_name: 模块名称
            content: markdown内容

        Returns:
            Path: 保存的文件路径，如果保存失败则返回None
        """
        if not content:
            return None

        FileHelper.ensure_directory_exists(target_dir)
        markdown_file = target_dir / f"{module_name}.md"

        try:
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(content)

            return markdown_file

        except Exception as e:
            print(f"⚠️ Markdown文件保存失败: {e}")
            return None

    def save_crawl_result(
        self,
        target_dir: Path,
        module_name: str,
        sub_module_name: str,
        html_content: str,
        markdown_content: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        保存爬取结果（HTML + Markdown）

        Args:
            target_dir: 目标目录
            module_name: 模块名称
            sub_module_name: 子模块名称
            html_content: HTML内容
            markdown_content: Markdown内容
            metadata: 元数据

        Returns:
            Dict: 保存结果信息
        """
        # 保存HTML文件（如果启用调试模式）
        html_file = self.save_html_file(
            target_dir=target_dir,
            module_name=module_name,
            content=html_content,
            metadata={**metadata, 'sub_module_name': sub_module_name}
        )

        # 保存Markdown文件
        markdown_file = self.save_markdown_file(
            target_dir=target_dir,
            module_name=module_name,
            content=markdown_content
        )

        return {
            "success": True,
            "url": metadata.get('url', ''),
            "title": metadata.get('title', sub_module_name),
            "module_name": module_name,
            "sub_module_name": sub_module_name,
            "html_file": str(html_file) if html_file else None,
            "markdown_file": str(markdown_file) if markdown_file else None,
            "content_length": len(html_content),
            "has_best_practices": bool(markdown_content and markdown_file),
            "skipped": False  # 标记为新保存
        }

    def get_output_summary(self, target_dir: Path) -> Dict[str, Any]:
        """
        获取输出目录摘要信息

        Args:
            target_dir: 目标目录

        Returns:
            Dict: 摘要信息
        """
        if not target_dir.exists():
            return {
                'directory_exists': False,
                'html_files': 0,
                'markdown_files': 0,
                'total_files': 0
            }

        html_files = list(target_dir.glob("*.html"))
        markdown_files = list(target_dir.glob("*.md"))

        return {
            'directory_exists': True,
            'directory_path': str(target_dir),
            'html_files': len(html_files),
            'markdown_files': len(markdown_files),
            'total_files': len(html_files) + len(markdown_files),
            'debug_mode': self.debug_mode
        }