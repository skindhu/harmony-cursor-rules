# HarmonyOS 手势与导航 - Cursor Rules

你正在为HarmonyOS应用开发相关功能。以下是你需要遵循的开发规则。

## 核心原则

*   理解HarmonyOS触摸事件的分发机制和事件响应链的构建过程，是解决手势冲突的基础。
*   优先使用HarmonyOS提供的标准UI组件（如`Tabs`）构建导航，确保一致、高效的用户体验。
*   利用HMRouter简化页面路由管理，提升开发效率和代码可维护性，避免手动管理页面栈。

## 推荐做法

### 代码结构
*   使用`@Builder`装饰器封装可复用的UI模块，例如自定义底部页签的图标和文字组合 (`TabItemBuilder`)。
*   通过`@HMRouter`注解为目标页面注册唯一的`pageUrl`，实现声明式路由配置。

### 最佳实践
*   **手势事件冲突解决**：
    *   通过`hitTestBehavior`属性精确控制组件的触摸测试行为：
        *   `HitTestMode.Transparent`: 组件自身响应，但允许事件继续向下或向上透传。
        *   `HitTestMode.Block`: 组件命中后独占事件，阻塞事件向兄弟节点和父组件传递。
    *   在触摸或手势回调函数中，适时调用`event.stopPropagation()`，立即停止事件向上冒泡。
*   **底部页签导航**：
    *   使用`Tabs`组件作为底部导航容器，并设置`barPosition: BarPosition.End`。
    *   为每个`TabContent`组件通过`tabBar`属性定义其对应的页签外观（包括选中和未选中状态的图标及文字）。
    *   对于固定数量的页签，设置`Tabs`的`barMode: Fixed`以平均分配页签宽度。
*   **页面跳转与返回**：
    *   使用`HMRouterMgr.push()`或`HMRouterMgr.replace()`方法进行页面跳转，并可通过`param`参数传递数据。
    *   在目标页面（被跳转页）的`aboutToAppear`生命周期中，通过`HMRouterMgr.getCurrentParam()`获取跳转参数。
    *   在`push/replace`方法的`onResult`回调中接收从其他页面返回的数据，并通过`popInfo.srcPageInfo.name`判断返回源页面。

## 禁止做法

*   **过度阻塞手势事件**：未经深思熟虑地滥用`HitTestMode.Block`或`event.stopPropagation()`，可能导致用户交互失效或应用行为异常。
*   **手动管理页面栈**：避免直接操作底层的`Navigation`能力进行页面跳转和栈管理，应优先使用HMRouter提供的统一接口。

## 代码示例

### 推荐写法
```arkts
// 手势冲突处理: 独占区域手势，不向上冒泡
Column() {
  Text('点击我，事件在此终止')
}
.width('100%').height(100)
.backgroundColor(Color.Blue)
.hitTestBehavior(HitTestMode.Block) // 独占所有触摸事件
.onClick(() => {
  console.log('Column clicked, event stopped here.');
})

// 底部页签导航 (简化示例)
Tabs({ barPosition: BarPosition.End }) {
  TabContent() { Text('消息页面').fontSize(24) }
    .tabBar(this.TabItemBuilder('消息', $r('app.media.message_icon'))) // 自定义页签样式
  TabContent() { Text('我的页面').fontSize(24) }
    .tabBar(this.TabItemBuilder('我的', $r('app.media.profile_icon')))
}

@Builder TabItemBuilder(text: string, icon: Resource) {
  Column() {
    Image(icon).width(24).height(24)
    Text(text).fontSize(12)
  }
}

// 页面跳转与参数传递，并接收返回结果
HMRouterMgr.push({
  pageUrl: 'pages/DetailPage', // 目标页面路由
  param: { id: 123, name: 'Product A' }, // 传递参数
  onResult: (popInfo) => { // 接收返回结果
    if (popInfo.srcPageInfo.name === 'pages/DetailPage') {
      console.log('Returned from DetailPage with result:', popInfo.result);
    }
  }
});
```

### 避免写法
```arkts
// 避免不加区分地在父子组件上都使用onTouch，且不控制事件冒泡，这会增加手势冲突的风险。
// 避免在存在多个HMNavigation组件时，不指定HMRouterMgr跳转的navigationId，可能导致页面跳转到错误的栈。
```

## 注意事项

*   在使用`hitTestBehavior`和`event.stopPropagation()`时，务必充分测试，确保用户交互的连贯性和预期性。
*   在应用中存在多个`HMNavigation`组件（如多窗口、多页面栈）时，务必为`HMRouterMgr.push/replace`方法明确指定正确的`navigationId`，以确保页面跳转到正确的导航栈。
*   为底部导航的页签提供清晰的图标（区分选中和未选中态）和简洁的文字标签，以提升用户识别度和整体用户体验。