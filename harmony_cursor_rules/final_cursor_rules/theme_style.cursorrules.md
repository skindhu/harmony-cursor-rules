# HarmonyOS 主题与样式 - Cursor Rules

你正在为HarmonyOS应用开发相关功能。以下是你需要遵循的开发规则。

## 核心原则

- **响应用户/系统偏好**: UI应自动适配深浅色模式及用户自定义亮度。
- **保持视觉一致性**: 在不同模式和页面间，保持UI元素的统一性和协调性。
- **优化资源与性能**: 合理管理资源，避免不必要的电量消耗和性能开销。
- **提供流畅用户体验**: 确保用户在不同场景下（如视频播放、付款码）获得无缝且舒适的体验。

## 推荐做法

### 代码结构
- **资源目录管理**: 利用HarmonyOS的资源目录机制 (`src/main/resources/base` 用于浅色模式，`src/main/resources/dark` 用于深色模式) 管理深浅色资源。
- **同名资源定义**: 在 `base` 和 `dark` 目录下，为同一种UI元素（如颜色、图片）定义**同名**的资源文件和资源项，实现自动切换。

### 最佳实践
- **深浅色模式适配**:
    - **颜色资源**: 自定义颜色应定义在 `base/element/color.json` 和 `dark/element/color.json` 中，并通过 `$('app.color.your_color_name')` 引用。优先使用系统级颜色资源。
    - **媒体资源**:
        - SVG图标: 利用 `fillColor()` 属性，使其颜色跟随当前主题变化。
        - 非SVG图片: 在 `base/media` 和 `dark/media` 目录下放置同名图片资源。
    - **状态栏**: 确保状态栏背景和内容字体颜色与应用深浅模式保持一致。
    - **Web页面**: 配合前端开发，使应用内嵌Web内容支持深色模式（利用CSS媒体查询 `prefers-color-scheme`）。
    - **模式切换**: 提供应用跟随系统模式切换 (`applicationContext.setColorMode(ColorMode.COLOR_MODE_NOT_SET)`) 或用户手动切换的选项。
- **页面亮度与常亮控制**:
    - **页面级亮度**: 使用 `window.setWindowBrightness()` 实现页面专属亮度。利用 `uiObserver.on('navDestinationUpdate')` 监听页面跳转，并在页面进入时应用亮度，离开时恢复系统默认或前一页面的亮度。
    - **屏幕常亮**: 在沉浸式场景（如视频播放）中，通过 `window.setWindowKeepScreenOn(true)` 保持屏幕常亮。务必将其与组件生命周期绑定（如 `onStart` 开启，`onPause`/`onDestroy` 关闭）。
    - **用户UI**: 为需要用户调节亮度的场景（如视频播放器）提供 `Slider` 等UI组件，方便用户调节。

## 禁止做法

- **硬编码颜色值**: 避免直接在代码中写入十六进制或RGB颜色值，应统一通过资源引用。
- **不及时关闭屏幕常亮**: 在不需要常亮时（如视频暂停、页面退出）不调用 `setWindowKeepScreenOn(false)`，导致不必要的电量消耗和设备发热。
- **深浅色资源命名不一致**: 在 `base` 和 `dark` 目录下为同一元素定义不同的资源名称，导致深浅色模式切换失败。

## 代码示例

### 推荐写法
```arkts
// 1. 深浅色模式下引用颜色资源
Text('Hello HarmonyOS')
  .fontColor($r('app.color.text_primary')) // text_primary 在base和dark下定义不同颜色

// 2. 页面亮度动态设置与屏幕常亮
// 假设在视频播放页面的某个组件内
@State currentBrightness: number = 0.5; // 当前页面亮度

aboutToAppear() {
  // 进入页面时设置亮度，并保持屏幕常亮
  window.setWindowBrightness(this.currentBrightness);
  window.setWindowKeepScreenOn(true);
}

aboutToDisappear() {
  // 离开页面时恢复系统亮度，并关闭屏幕常亮
  window.setWindowBrightness(-1); // -1 表示恢复系统默认亮度
  window.setWindowKeepScreenOn(false);
}

// 用户通过Slider调节亮度
Slider({ value: this.currentBrightness, min: 0.01, max: 1.0, step: 0.01 })
  .onChange((value: number) => {
    this.currentBrightness = value;
    window.setWindowBrightness(value);
  })
```

### 避免写法
```arkts
// 1. 硬编码颜色值
Text('Avoid this')
  .fontColor('#FF0000') // 硬编码红色，在深色模式下可能不协调

// 2. 随意开启屏幕常亮，不及时关闭
// 假设某个地方开启了常亮，但没有对应的关闭逻辑
window.setWindowKeepScreenOn(true); // 容易造成电量浪费
```

## 注意事项

- **资源自动切换**: HarmonyOS会自动根据系统颜色模式加载对应资源目录下的同名资源，无需额外代码判断。
- **页面亮度作用域**: `window.setWindowBrightness()` 仅在当前应用内生效，退出应用后系统亮度会自动恢复。
- **Web组件适配**: Web内容的深色模式适配通常需要前端开发人员配合完成，确保Web内容自身支持 `prefers-color-scheme`。
- **权限**: 某些亮度或窗口操作可能需要特定权限，请查阅官方文档。