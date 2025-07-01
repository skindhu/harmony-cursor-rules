作为一位资深的HarmonyOS界面开发专家，我将基于您提供的华为官方文档HTML内容，分析并整理出界面开发领域的最佳实践。

请注意，您提供的HTML内容中，关于“顶部导航”和“侧边导航”的具体实现细节（即 `app-document-text` 部分）并未完全展开，因此我将主要聚焦于HTML中已包含详细描述的“底部导航”部分。

---

# 常见导航样式案例 - 最佳实践

## 📋 概述
本模块核心功能是探讨HarmonyOS应用中常见的页签导航样式及其实现方案。不同的产品形态和用户体验需求会衍生出多样化的UI效果，文档旨在为开发者提供底部、顶部和侧边导航的实现指导，以帮助构建丰富多样的应用界面。

## 🎯 最佳实践

### 1. 底部导航 - 基础样式
- **实践要点**：适用于常规应用场景，通过图标和文字组合提供清晰的导航入口，用户可以方便地在不同核心功能模块间切换。
- **实现方式**：
    *   使用HarmonyOS的 `Tabs` 组件作为底部导航的主要容器。
    *   通过设置 `Tabs` 组件的 `barPosition` 属性为 `BarPosition.End`，确保导航条固定在屏幕底部。
    *   在 `Tabs` 组件内部，通过循环或单独调用自定义的 `@Builder` 方法（如 `tabContentBuilder`）来构建每个页签的内容和对应的导航栏项。
    *   自定义的 `@Builder` 方法内部应包含 `TabContent` 组件，用于承载每个页签的实际页面内容，并通过 `TabContent` 的 `tabBar` 属性定义页签的图标（选中态和非选中态）和文字。
    *   通过 `Tabs` 的 `barHeight` (导航栏高度)、`backgroundColor` (背景色) 和 `barMode` (导航栏模式，如 `Fixed` 固定模式) 等属性进行样式定制。
    *   利用 `onAnimationStart` 回调函数，可以在页签切换动画开始时获取当前和目标页签的索引，便于进行状态管理或数据更新。
- **注意事项**：
    *   确保为每个页签提供清晰的图标（区分选中和未选中状态）和简洁的文字标签，以增强用户识别度。
    *   合理设置 `barHeight`，使其在不同设备上都能提供良好的点击区域和视觉效果。
    *   `barMode` 设置为 `Fixed` 时，所有页签的宽度将平均分配，适用于页签数量较少（通常3-5个）的场景。
    *   注意通过 `Constants` 或其他方式管理页签索引，提高代码可读性和维护性。

## 💡 代码示例

```arkts
// 定义Tabs控制器，用于控制页签的切换
// @State tabsController: TabsController = new TabsController(); // 假设已在类中声明

// build方法中实现底部导航
build() {
  Tabs({
    barPosition: BarPosition.End, // 设置导航条在底部显示
    controller: this.tabsController // 绑定控制器
  }) {
    // 示例：第一个页签 - 消息
    this.tabContentBuilder(
      $r('app.string.message'), // 页签文字资源
      Constants.TAB_INDEX_ZERO, // 页签索引
      $r('app.media.activeMessage'), // 选中态图标资源
      $r('app.media.message') // 未选中态图标资源
    )
    // 示例：第二个页签 - 人脉
    this.tabContentBuilder(
      $r('app.string.people'),
      Constants.TAB_INDEX_ONE,
      $r('app.media.activePeople'),
      $r('app.media.people')
    )
    // 示例：第三个页签 - 活动
    this.tabContentBuilder(
      $r('app.string.activity'),
      Constants.TAB_INDEX_TWO,
      $r('app.media.activeStar'),
      $r('app.media.star')
    )
  }
  .width('100%') // 导航条宽度占满父容器
  .backgroundColor('#F3F4F5') // 导航条背景色
  .barHeight(52) // 导航条高度
  .barMode(BarMode.Fixed) // 导航条模式为固定，页签宽度平均分配
  .onAnimationStart((index: number, targetIndex: number) => {
    // 监听页签切换动画开始事件
    hilog.info(0x0000, 'index', index.toString()); // 打印当前页签索引
    this.currentIndex = targetIndex; // 更新当前选中页签的索引
  })
}

// @Builder 修饰器定义自定义组件，用于构建单个TabContent及其tabBar
@Builder
tabContentBuilder(text: Resource, index: number, selectedImg: Resource, normalImg: Resource) {
  TabContent() {
    // 这里放置当前页签的具体内容，例如一个Text或Column等
    // Text(`${text.toString()} Content`) // 示例内容
    // .fontSize(24)
    // .fontColor(Color.Black)
    // .width('100%')
    // .height('100%')
    // .backgroundColor(index === Constants.TAB_INDEX_ZERO ? Color.Red : index === Constants.TAB_INDEX_ONE ? Color.Green : Color.Blue)
  }
  .tabBar({ // 定义页签的导航栏部分
    builder: () => { // 使用builder自定义tabBar的UI
      Column() {
        Image(this.currentIndex === index ? selectedImg : normalImg) // 根据选中状态显示不同图标
          .size({ width: 24, height: 24 })
        Text(text) // 显示页签文字
          .fontSize(12)
          .fontColor(this.currentIndex === index ? Color.Blue : Color.Gray) // 根据选中状态显示不同文字颜色
      }
      .justifyContent(FlexAlign.Center)
      .width('100%')
      .height('100%')
    }
  })
}
```
*注：上述代码示例是根据HTML中提供的 `Tabs` 组件使用方式和链接到的Gitee仓库 `BottomTab.ets` 文件内容推断和补充的，以提供一个完整的、可运行的示例。实际文档中的HTML只包含 `build()` 方法的部分代码。*

## ⚠️ 常见陷阱

### 避免的做法
- **未区分选中/未选中状态的图标和文字颜色**：导致用户无法清晰识别当前所在的页签，降低可用性。
- **底部导航条高度设置过小**：可能导致点击区域不足，影响用户操作体验。
- **页签内容与导航条耦合过紧**：将页面内容直接写在 `Tabs` 内部，而不是通过 `TabContent` 和 `@Builder` 封装，导致代码复用性差，维护困难。
- **未处理页签切换时的状态更新**：例如，当页签切换时，相关数据或UI状态未及时更新。

### 推荐的做法
- **提供清晰的视觉反馈**：通过改变图标、文字颜色、背景高亮等方式，明确指示当前选中的页签。
- **使用自定义 `@Builder` 封装页签样式**：将 `tabBar` 的UI逻辑封装在独立的 `@Builder` 方法中，提高代码复用性和可维护性。
- **合理利用 `onAnimationStart` 或 `onChange` 等回调**：在页签切换时，进行必要的业务逻辑处理或数据加载。
- **遵循HarmonyOS设计规范**：确保导航样式与系统整体风格保持一致，提供统一的用户体验。

## 🔗 相关资源
- 原文档：https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-multi-tab-practice
- 相关代码示例（Gitee）：https://gitee.com/harmonyos_samples/multi-tab-navigation/blob/master/entry/src/main/ets/pages/BottomTab.ets#L95-L115