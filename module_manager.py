#!/usr/bin/env python3
"""
HarmonyOS模块管理器
负责配置文件加载、目录结构创建和模块信息管理
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple


class HarmonyModuleManager:
    """HarmonyOS模块配置管理器"""

    def __init__(self, config_file: str = "harmony_modules_config.json"):
        self.config_file = config_file
        self.config = {}
        self.load_config()

    def load_config(self) -> bool:
        """
        加载模块配置文件

        Returns:
            bool: 是否加载成功
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"✅ 成功加载配置文件: {self.config_file}")
            return True
        except FileNotFoundError:
            print(f"❌ 配置文件未找到: {self.config_file}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ 配置文件格式错误: {e}")
            return False

    def get_all_modules(self) -> List[Dict[str, Any]]:
        """
        获取所有模块的完整信息列表

        Returns:
            List[Dict]: 包含所有模块信息的列表
        """
        modules = []

        if "modules" not in self.config:
            return modules

        for category_name, category_info in self.config["modules"].items():
            for sub_module_name, sub_module_info in category_info["sub_modules"].items():
                module_info = {
                    "category_name": category_name,
                    "category_directory": category_info["directory"],
                    "sub_module_name": sub_module_name,
                    "module_name": sub_module_info["module_name"],
                    "url": sub_module_info["url"]
                }
                modules.append(module_info)

        return modules

    def get_category_info(self, category_name: str) -> Dict[str, Any]:
        """
        获取指定一级模块的信息

        Args:
            category_name: 一级模块名称

        Returns:
            Dict: 模块信息
        """
        if "modules" not in self.config:
            return {}

        return self.config["modules"].get(category_name, {})

    def get_total_module_count(self) -> int:
        """
        获取模块总数

        Returns:
            int: 模块总数
        """
        total = 0
        if "modules" in self.config:
            for category_info in self.config["modules"].values():
                total += len(category_info["sub_modules"])
        return total

    def create_directory_structure(self, base_dir: Path) -> List[Path]:
        """
        根据配置创建目录结构

        Args:
            base_dir: 基础目录路径

        Returns:
            List[Path]: 创建的目录路径列表
        """
        created_dirs = []

        if "modules" not in self.config:
            print("❌ 配置文件中未找到modules字段")
            return created_dirs

        base_dir.mkdir(exist_ok=True)
        print(f"📁 确保基础目录存在: {base_dir}")

        for category_name, category_info in self.config["modules"].items():
            category_dir = base_dir / category_info["directory"]
            category_dir.mkdir(exist_ok=True)
            created_dirs.append(category_dir)
            print(f"📁 创建目录: {category_dir} (一级模块: {category_name})")

        return created_dirs

    def get_modules_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        按一级模块分组获取所有模块信息

        Returns:
            Dict: 按一级模块分组的模块信息
        """
        grouped_modules = {}

        if "modules" not in self.config:
            return grouped_modules

        for category_name, category_info in self.config["modules"].items():
            modules_in_category = []

            for sub_module_name, sub_module_info in category_info["sub_modules"].items():
                module_info = {
                    "sub_module_name": sub_module_name,
                    "module_name": sub_module_info["module_name"],
                    "url": sub_module_info["url"],
                    "category_directory": category_info["directory"]
                }
                modules_in_category.append(module_info)

            grouped_modules[category_name] = modules_in_category

        return grouped_modules

    def validate_config(self) -> Tuple[bool, List[str]]:
        """
        验证配置文件的完整性

        Returns:
            Tuple[bool, List[str]]: (是否有效, 错误信息列表)
        """
        errors = []

        if not self.config:
            errors.append("配置文件为空")
            return False, errors

        if "modules" not in self.config:
            errors.append("缺少modules字段")
            return False, errors

        for category_name, category_info in self.config["modules"].items():
            if "directory" not in category_info:
                errors.append(f"一级模块 '{category_name}' 缺少directory字段")

            if "sub_modules" not in category_info:
                errors.append(f"一级模块 '{category_name}' 缺少sub_modules字段")
                continue

            for sub_module_name, sub_module_info in category_info["sub_modules"].items():
                if "module_name" not in sub_module_info:
                    errors.append(f"二级模块 '{sub_module_name}' 缺少module_name字段")

                if "url" not in sub_module_info:
                    errors.append(f"二级模块 '{sub_module_name}' 缺少url字段")
                elif not sub_module_info["url"].startswith("http"):
                    errors.append(f"二级模块 '{sub_module_name}' 的URL格式无效")

        is_valid = len(errors) == 0
        return is_valid, errors

    def print_config_summary(self):
        """打印配置文件摘要信息"""
        if not self.config:
            print("❌ 没有配置信息")
            return

        print("📋 配置文件摘要:")
        print(f"📊 总模块数: {self.get_total_module_count()}")
        print(f"📂 一级模块数: {len(self.config.get('modules', {}))}")

        print("\n📁 一级模块列表:")
        for category_name, category_info in self.config.get("modules", {}).items():
            sub_module_count = len(category_info.get("sub_modules", {}))
            print(f"  - {category_name} ({category_info.get('directory', 'unknown')}) - {sub_module_count}个子模块")

    def get_module_by_name(self, module_name: str) -> Dict[str, Any]:
        """
        根据模块名称查找模块信息

        Args:
            module_name: 模块名称 (module_name字段)

        Returns:
            Dict: 模块信息，未找到返回空字典
        """
        for category_name, category_info in self.config.get("modules", {}).items():
            for sub_module_name, sub_module_info in category_info.get("sub_modules", {}).items():
                if sub_module_info.get("module_name") == module_name:
                    return {
                        "category_name": category_name,
                        "category_directory": category_info["directory"],
                        "sub_module_name": sub_module_name,
                        "module_name": sub_module_info["module_name"],
                        "url": sub_module_info["url"]
                    }
        return {}


# 使用示例和测试代码
if __name__ == "__main__":
    # 测试模块管理器
    manager = HarmonyModuleManager()

    # 验证配置
    is_valid, errors = manager.validate_config()
    if not is_valid:
        print("❌ 配置文件验证失败:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ 配置文件验证通过")

    # 打印摘要
    manager.print_config_summary()

    # 测试获取所有模块
    all_modules = manager.get_all_modules()
    print(f"\n📊 获取到 {len(all_modules)} 个模块")

    # 测试按分类获取模块
    grouped_modules = manager.get_modules_by_category()
    print(f"\n📂 按分类获取到 {len(grouped_modules)} 个一级模块")