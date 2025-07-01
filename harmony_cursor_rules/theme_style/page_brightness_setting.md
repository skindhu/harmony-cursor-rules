作为一名资深的HarmonyOS界面开发专家，我将基于您提供的华为官方文档HTML内容，为您分析并整理出页面亮度设置领域的最佳实践。

# 页面亮度设置 - 最佳实践

## 📋 概述
本模块聚焦于HarmonyOS应用中页面亮度的精细化管理。它旨在解决在特定场景（如视频播放、付款码展示）下，应用需要动态调整屏幕亮度、支持用户自定义亮度，并在页面跳转时自动恢复系统或预设亮度的需求。核心功能包括视频播放页面的亮度调节、视频播放时的屏幕常亮设置以及付款码页面的高亮显示。

## 🎯 最佳实践

### 1. 页面级亮度动态管理与恢复
- **实践要点**：针对不同的应用页面（尤其是功能性页面如视频播放页、付款码页），应能够设置其专属的屏幕亮度。用户在特定页面调整的亮度应在该页面生效，并在离开该页面后自动恢复到系统默认亮度或进入前页面的亮度。再次进入该页面时，应恢复其上次保存的亮度设置。
- **实现方式**：
    *   **维护亮度映射表**：使用 `Map<string, number>` 结构维护页面路径（`navDestination`）与对应亮度的映射关系。例如：`brightnessMap.set(Constants.NAV_DESTINATION_ITEM_PAY_CODE, this.MAX_BRIGHTNESS)`。
    *   **监听页面跳转**：利用 `uiObserver.on('navDestinationUpdate')` API 监听页面的进入和离开事件。
    *   **动态设置亮度**：在页面进入时，根据映射表获取并应用对应的亮度值；在页面离开时，恢复系统默认亮度或上一个页面的亮度。
    *   **核心API**：`window.setWindowBrightness(brightness: number, callback: AsyncCallback<void>)`。
- **注意事项**：
    *   亮度设置仅在当前应用内生效，退出应用后系统亮度会自动恢复。
    *   确保页面路径（`navDestination`）的唯一性和准确性，以便正确匹配亮度。

### 2. 屏幕常亮智能控制
- **实践要点**：在用户进行沉浸式操作（如观看视频）时，应自动保持屏幕常亮，避免因超时熄屏打断用户体验。在操作结束后，应及时取消常亮状态，以节省电量。
- **实现方式**：
    *   **绑定组件生命周期**：将屏幕常亮设置与相关组件（如 `Video` 播放器）的生命周期事件（如 `onStart`、`onPause`）绑定。
    *   **开启常亮**：在视频播放开始时（`onStart`），调用 `window.setWindowKeepScreenOn(true)`。
    *   **关闭常亮**：在视频播放暂停或结束时（`onPause`），调用 `window.setWindowKeepScreenOn(false)`。
    *   **核心API**：`window.setWindowKeepScreenOn(isKeepScreenOn: boolean, callback: AsyncCallback<void>)`。
- **注意事项**：
    *   务必在不需要常亮时及时关闭，避免不必要的电量消耗和设备发热。
    *   考虑用户在播放过程中手动调整常亮设置的可能性，并确保应用行为与用户意图一致。

### 3. 用户可调节亮度UI集成
- **实践要点**：对于需要用户手动调节亮度的场景（如视频播放页），应提供直观、易用的UI组件，让用户能够便捷地进行调节。
- **实现方式**：
    *   **使用Slider组件**：在视频播放器等页面叠加 `Slider` 组件，用于调节亮度。
    *   **绑定亮度值**：将 `Slider` 的 `value` 属性绑定到当前页面的亮度状态变量。
    *   **设置调节范围**：将 `Slider` 的 `min` 和 `max` 值设置为 `0` 到 `1`（或0.01到1.00），`step` 设置为合适的粒度（如 `0.01`）。
    *   **触发亮度更新**：在 `Slider` 的 `onChange` 事件中调用 `window.setWindowBrightness()` 更新屏幕亮度。
    *   **示例配置**：
        ```arkts
        Slider({
            value: this.currentBrightness,
            min: 0,
            max: 1,
            step: 0.01,
            style: SliderStyle.InSet,
            direction: Axis.Vertical, // 垂直方向调节
            reverse: true // 反向，符合亮度调节习惯
        })
        .trackColor('#66A0A0A4') // 滑轨颜色
        .blockColor(Color.Transparent) // 滑块颜色
        .selectedColor(Color.White) // 选中部分颜色
        // .onChange(...) // 在此处理亮度值变化，调用setWindowBrightness
        ```
- **注意事项**：
    *   `Slider` 的样式和布局应与整体UI风格保持一致，并确保不会遮挡视频内容。
    *   考虑到不同设备的屏幕亮度差异，`0-1`的范围可以覆盖所有设备。

### 4. 特定场景高亮显示
- **实践要点**：对于付款码、二维码等需要确保清晰可见的场景，应将页面亮度自动设置为最高，以便于扫描或展示。
- **实现方式**：
    *   在进入付款码页面时，直接将该页面的亮度设置为最大值（`1.0` 或 `MAX_BRIGHTNESS`）。这可以通过在页面初始化时从亮度映射表中读取并设置。
    *   离开该页面时，确保亮度自动恢复。
- **注意事项**：
    *   高亮设置通常是固定值，不提供用户调节选项。
    *   仅在确实需要高亮显示的页面应用，避免滥用。

## 💡 代码示例

```arkts
// BrightnessUtil.ets (示例辅助类，用于管理页面亮度映射)
// 维护页面与亮度的映射关系
private static brightnessMap: Map<string, number> =
    new Map([[Constants.NAV_DESTINATION_DEFAULT, this.DEFAULT_BRIGHTNESS],
    [Constants.NAV_DESTINATION_ITEM_PAY_CODE, this.MAX_BRIGHTNESS]]);

// 视频播放页面集成 Slider 和常亮控制
// 假设在一个VideoPlayerComponent中
build() {
  Stack({ alignContent: Alignment.Start }) {
    Video({
      src: $rawfile('video1.mp4'),
      previewUri: $r('app.media.img_preview'),
    })
    .loop(true)
    .width(Constants.FULL_PERCENT)
    .height(Constants.FULL_PERCENT)
    .onStart(() => {
      // 视频开始播放时设置屏幕常亮
      this.brightnessViewModel.setWindowKeepScreenState(true);
    })
    .onPause(() => {
      // 视频暂停时取消屏幕常亮
      this.brightnessViewModel.setWindowKeepScreenState(false);
    })

    // 亮度调节Slider
    Slider({
      value: this.currentBrightness, // 绑定当前亮度值
      min: 0,
      max: 1,
      step: 0.01,
      style: SliderStyle.InSet,
      direction: Axis.Vertical,
      reverse: true
    })
    .trackColor('#66A0A0A4')
    .blockColor(Color.Transparent)
    .selectedColor(Color.White)
    .height('80%')
    // .onChange((value: number) => {
    //   // 用户拖动Slider时，更新亮度
    //   this.currentBrightness = value;
    //   window.setWindowBrightness(value, (err) => {
    //     if (err) {
    //       console.error(`Failed to set window brightness: ${err.message}`);
    //     }
    //   });
    //   // 同时更新Map中的亮度，以便下次进入时恢复
    //   this.brightnessMap.set(currentPagePath, value);
    // })
  }
}

// 假设在某个页面管理类或ViewModel中，处理页面跳转和亮度设置
// 监听页面跳转事件
// uiObserver.on('navDestinationUpdate', (data: NavDestinationInfo) => {
//     const currentPath = data.navDestination;
//     // 根据currentPath从brightnessMap中获取亮度，并调用window.setWindowBrightness
//     // 离开页面时，恢复默认亮度或上一个页面的亮度
// });

// 设置窗口亮度的方法（示例，具体实现可能在ViewModel中）
// function setWindowBrightness(brightness: number) {
//   window.setWindowBrightness(brightness, (err) => {
//     if (err) {
//       console.error(`Failed to set window brightness: ${err.message}`);
//     }
//   });
// }

// 设置屏幕常亮的方法（示例，具体实现可能在ViewModel中）
// function setWindowKeepScreenOn(isKeepScreenOn: boolean) {
//   window.setWindowKeepScreenOn(isKeepScreenOn, (err) => {
//     if (err) {
//       console.error(`Failed to set window keep screen on: ${err.message}`);
//     }
//   });
// }
```

## ⚠️ 常见陷阱

### 避免的做法
- **全局性亮度设置**：避免在应用启动时一次性设置全局亮度，而不考虑不同页面的特定需求，导致所有页面亮度一致，影响用户体验。
- **未及时恢复亮度**：在离开特定亮度设置页面（如视频播放页、付款码页）时，未能通过监听机制及时恢复到系统默认亮度或前一个页面的亮度，导致用户在其他页面体验异常。
- **屏幕常亮滥用**：在非必要场景（如非视频播放、非关键信息展示）下长时间保持屏幕常亮，导致设备电量快速消耗和不必要的发热。
- **未提供用户调节选项**：对于可能需要用户自定义亮度的场景（如阅读器、视频播放器），未提供相应的UI调节组件，剥夺了用户的控制权。

### 推荐的做法
- **利用官方API和机制**：充分利用 `uiObserver.on('navDestinationUpdate')` 监听页面变化，结合 `window.setWindowBrightness()` 和 `window.setWindowKeepScreenOn()` 实现精准的页面级亮度控制。
- **状态管理**：使用 `Map` 或类似的数据结构来管理不同页面的亮度状态，确保页面亮度的持久化和恢复。
- **用户体验为中心**：在设计亮度调节功能时，始终以用户体验为核心，提供直观的UI，并在合适时机自动调整和恢复亮度。
- **资源优化**：严格控制屏幕常亮的状态，仅在用户有明确需求时开启，并在需求结束后立即关闭。

## 🔗 相关资源
- 原文档：https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-page-brightness-settings