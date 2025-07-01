# HarmonyOS 开发规则生成器

## 📖 项目背景

HarmonyOS作为新兴的移动操作系统，由于发展历史相对较短，主流AI模型在预训练阶段缺乏充足的HarmonyOS开发语料。这导致Cursor等AI开发工具在生成HarmonyOS相关代码时效果不佳，开发者难以获得准确的开发建议。

本项目旨在解决这一痛点，通过智能爬取华为官方HarmonyOS开发文档，自动提取最佳实践并生成符合Cursor IDE规范的开发规则文件，为开发者提供专业、准确的HarmonyOS开发指导。

## 🚀 核心功能

- **📋 智能文档爬取**: 自动爬取华为官方HarmonyOS最佳实践文档，支持SPA页面解析
- **📝 UI开发规范生成**: 基于Gemini AI智能提取界面开发最佳实践，生成结构化的开发规范
- **🔧 ArkTS迁移规则**: 自动提取TypeScript到ArkTS迁移过程中的Lint规则和语法约束

## 📁 harmony_cursor_rules 说明

项目运行后会生成 `harmony_cursor_rules` 目录，包含按模块分类的开发规范文件。具体涉及的模块配置可查看 `harmony_modules_config.json` 文件：

### 目录结构
```
harmony_cursor_rules/
├── component_encapsulation_reuse/    # 组件封装与复用
├── layout_dialog/                    # 布局与弹窗
├── animation_transition/             # 动画与转场
├── performance_optimization/         # 性能优化
├── ...                              # 其他模块
└── final_cursor_rules/              # 最终整合的规则文件
    ├── component_encapsulation_reuse.cursorrules.md
    ├── layout_dialog.cursorrules.md
    ├── arkts-lint-rules.md           # ArkTS迁移规则
    └── ...
```

> 💡 **快速使用**: 开发者只需将 `final_cursor_rules` 目录下的规则文件配置到Cursor IDE中即可获得专业的HarmonyOS开发提示。如果需要生成更多的规则文件，可在`harmony_modules_config.json`追加配置。

### 参考文档
生成的开发规则均基于华为官方权威文档：
- **界面开发最佳实践**: [HarmonyOS 最佳实践 - 界面开发](https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-ui-dynamic-operations)
- **ArkTS迁移指南**: [TypeScript到ArkTS迁移指南](https://developer.huawei.com/consumer/en/doc/harmonyos-guides-V14/typescript-to-arkts-migration-guide-V14)

## 🛠️ 使用方式

### 环境准备
1. **安装依赖**
```bash
pip install -r Requirements.txt
```

2. **配置API密钥**
```bash
# 设置Gemini API密钥
export GEMINI_API_KEY="your-gemini-api-key"
```

### 运行程序
```bash
# 标准运行
python main.py

# 调试模式（保存HTML文件）
python main.py --debug
```

### 使用生成的规则
1. 在你的HarmonyOS项目根目录创建 `.cursorrules` 文件
2. 将 `final_cursor_rules` 目录中相关 `.md` 文件的内容复制到 `.cursorrules` 文件中
3. 重启Cursor IDE，即可享受专业的HarmonyOS开发智能提示

## 📊 输出示例

生成的开发规则文件结构完整，包含：
- **核心原则**: HarmonyOS开发的基础设计理念和架构原则
- **推荐做法**: 经过验证的最佳实践和标准代码模式
- **禁止做法**: 需要避免的错误写法和反模式
- **代码示例**: 正确与错误写法的对比演示
- **注意事项**: 关键的开发要点和性能优化建议

---

*本项目基于AI技术自动化提取华为官方权威文档，为HarmonyOS开发者提供专业、标准的开发规范指导*