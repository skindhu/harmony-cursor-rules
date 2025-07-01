"""
AI提示词模板管理模块
包含各种场景下的提示词模板
"""

from typing import Dict, Any


class PromptTemplates:
    """提示词模板管理类"""

    @staticmethod
    def get_best_practices_extraction_prompt(
        title: str,
        module_name: str,
        url: str,
        html_content: str,
        max_content_length: int = 15000
    ) -> str:
        """
        获取最佳实践提取的提示词

        Args:
            title: 页面标题
            module_name: 模块名称
            url: 源URL
            html_content: HTML内容
            max_content_length: HTML内容最大长度

        Returns:
            str: 构建好的提示词
        """
        # 限制HTML内容长度以避免超出token限制
        limited_content = html_content[:max_content_length]

        return f"""
你是一位资深的HarmonyOS界面开发专家。请分析以下华为官方文档的HTML内容，提取并整理出界面开发领域的最佳实践。

**页面信息**：
- 标题：{title}
- 模块：{module_name}
- 链接：{url}

**HTML内容**：
{limited_content}

**请按以下格式输出最佳实践**：

# {module_name.replace('_', ' ').title()} - 最佳实践

## 📋 概述
[简要描述该模块的核心功能和用途]

## 🎯 最佳实践

### 1. [实践类别1]
- **实践要点**：[具体实践内容]
- **实现方式**：[如何实现]
- **注意事项**：[重要提醒]

### 2. [实践类别2]
- **实践要点**：[具体实践内容]
- **实现方式**：[如何实现]
- **注意事项**：[重要提醒]

## 💡 代码示例

```arkts
// 提取文档中的关键代码示例
```

## ⚠️ 常见陷阱

### 避免的做法
- [列出应该避免的做法]

### 推荐的做法
- [列出推荐的做法]

## 🔗 相关资源
- 原文档：{url}

**要求**：
1. 专注于界面开发的最佳实践
2. 提取具体可操作的建议
3. 包含代码示例（如果有）
4. 突出重要的注意事项
5. 使用清晰的markdown格式
6. 内容要实用且具体

请基于HTML内容提取真实有用的最佳实践，不要编造内容。
"""

    @staticmethod
    def get_practices_integration_prompt(
        module_name: str,
        practices_content: str,
        max_word_count: int = 800
    ) -> str:
        """
        获取实践整合的提示词

        Args:
            module_name: 模块名称
            practices_content: 实践内容汇总
            max_word_count: 最大字数限制

        Returns:
            str: 构建好的提示词
        """
        return f"""
你是一位资深的HarmonyOS界面开发专家。请将以下多个最佳实践文档整合成一个精简的Cursor Rules文件。

**模块名称**: {module_name}

**要整合的最佳实践内容**:
{practices_content}

**请严格按照以下Cursor Rules格式输出**:

```markdown
# HarmonyOS {module_name} - Cursor Rules

你正在为HarmonyOS应用开发相关功能。以下是你需要遵循的开发规则。

## 核心原则

- [列出3-5个核心开发原则，简洁明了]

## 推荐做法

### 代码结构
- [推荐的代码结构和组织方式]
- [关键的编程模式]

### 最佳实践
- [核心的最佳实践要点]
- [性能优化建议]

## 禁止做法

- [明确禁止的编程模式]
- [常见错误和陷阱]

## 代码示例

### 推荐写法
```arkts
// 提供1-2个简洁的正确示例
```

### 避免写法
```arkts
// 提供1-2个需要避免的错误示例
```

## 注意事项

- [重要的开发注意事项]
- [调试和性能监控建议]
```

**整合要求**:
1. 内容要精简，总长度控制在{max_word_count}字以内
2. 突出最重要和最实用的规则
3. 代码示例要简洁明了
4. 避免重复和冗余内容
5. 重点关注实际开发中的核心要点
6. 使用清晰的结构和格式

请基于提供的最佳实践内容进行整合，确保生成的Cursor Rules实用且易于理解。
"""

    @staticmethod
    def get_error_fallback_template(
        module_name: str,
        error_message: str,
        context: str = "最佳实践提取"
    ) -> str:
        """
        获取错误回退模板

        Args:
            module_name: 模块名称
            error_message: 错误信息
            context: 上下文描述

        Returns:
            str: 错误回退内容
        """
        return f"""# HarmonyOS {module_name.replace('_', ' ').title()} - {context}失败

## 错误信息
{context}时发生错误：{error_message}

## 原始资源
请查看相关源文件获取完整内容。

## 手动处理建议
1. 检查网络连接和API配置
2. 验证输入内容的格式和长度
3. 重试或手动提取关键信息
4. 查看日志获取更多错误详情
"""

    @staticmethod
    def get_integration_error_template(
        module_name: str,
        error_message: str
    ) -> str:
        """
        获取整合错误模板

        Args:
            module_name: 模块名称
            error_message: 错误信息

        Returns:
            str: 整合错误内容
        """
        return f"""# HarmonyOS {module_name} - Cursor Rules

## 错误信息
整合最佳实践时发生错误：{error_message}

## 原始资源
请查看该目录下的各个最佳实践文件获取详细内容。

## 手动整合建议
1. 提取各子模块的核心原则
2. 合并相似的最佳实践
3. 突出关键的代码模式
4. 列出明确的禁止事项
"""


class PromptBuilder:
    """提示词构建器类"""

    def __init__(self):
        self.templates = PromptTemplates()

    def build_extraction_prompt(self, **kwargs) -> str:
        """构建提取提示词"""
        return self.templates.get_best_practices_extraction_prompt(**kwargs)

    def build_integration_prompt(self, **kwargs) -> str:
        """构建整合提示词"""
        return self.templates.get_practices_integration_prompt(**kwargs)

    def build_error_fallback(self, **kwargs) -> str:
        """构建错误回退内容"""
        return self.templates.get_error_fallback_template(**kwargs)

    def build_integration_error(self, **kwargs) -> str:
        """构建整合错误内容"""
        return self.templates.get_integration_error_template(**kwargs)