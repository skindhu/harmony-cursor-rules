# HarmonyOS 动画与转场 - Cursor Rules

你正在为HarmonyOS应用开发相关功能。以下是你需要遵循的开发规则。

## 核心原则

-   **用户体验至上**: 动画旨在提升交互流畅感，引导用户，而非纯粹的视觉炫技。
-   **性能优先**: 确保动画运行流畅，不造成卡顿或资源浪费。
-   **系统能力优先**: 优先使用HarmonyOS提供的原生动画API和高级模板。
-   **设计意图匹配**: 深入理解UX设计，选择最符合场景的动效类型和实现方式。

## 推荐做法

### 代码结构
-   **声明式动画与状态驱动**: 优先使用HarmonyOS的声明式UI和 `@State` 驱动动画，通过改变状态变量触发动画。
-   **组件化封装**: 将复杂的动画逻辑封装到自定义组件中，提高复用性和可维护性。

### 最佳实践
-   **动效选择与场景匹配**:
    *   **页面路由转场**: 大部分页面切换推荐使用**左右位移遮罩动效**。
    *   **共享元素转场**: 图片展开、图标（搜索框、头像）展开，推荐使用**一镜到底动效**或`geometryTransition`接口。将关键元素作为持续存在的共享元素。
    *   **共享容器转场**: 卡片/视频展开、列表项展开，推荐使用`Navigation`自定义动画或`geometryTransition`结合显示动画。
    *   **通用动画**: 元素显隐、状态变化等，使用属性动画（`animateTo`）或显式动画。
-   **动画运行流畅度优化**:
    *   **优先使用系统动画API**: 系统提供的API经过底层优化，性能更佳。
    *   **动画属性选择**: 优先改变不影响布局的图形变换属性，如 `transform` (位移、旋转、缩放) 和 `opacity` (不透明度)。这些属性通常在GPU上合成，性能最高。
    *   **`animateTo` 复用**: 多个动画参数相同时，尽量在同一个 `animateTo` 块中更新状态，减少开销。
    *   **`renderGroup` 应用**: 对于包含复杂子组件的动画，将其设置为 `renderGroup(true)`，减少渲染批次。
-   **用户手势反馈**: 对于点击、滑动等手势，提供即时且连贯的动画反馈。

## 禁止做法

-   **频繁修改布局属性**: 严禁在动画过程中频繁改变组件的 `width`、`height`、`padding`、`margin` 等布局属性，这会导致UI树重绘，严重影响性能。
-   **滥用动画**: 避免不必要的、过于复杂的动画，以免分散用户注意力或增加视觉负担。
-   **缺乏用户反馈**: 禁止用户操作后界面无任何视觉反馈，特别是在点击、加载等关键交互点。

## 代码示例

### 推荐写法
```arkts
// 推荐：通过状态变化驱动动画，并优先改变图形变换属性
@Entry
@Component
struct GoodAnimationExample {
  @State isScaled: boolean = false;

  build() {
    Column() {
      Button('缩放')
        .width(100).height(100)
        .backgroundColor(Color.Blue)
        .scale(this.isScaled ? 1.5 : 1.0) // 改变scale属性
        .opacity(this.isScaled ? 0.5 : 1.0) // 改变opacity属性
        .onClick(() => {
          // 使用animateTo进行动画过渡
          animateTo({ duration: 300, curve: Curve.EaseOut }, () => {
            this.isScaled = !this.isScaled;
          });
        })
    }
    .width('100%').height('100%')
    .justifyContent(FlexAlign.Center)
  }
}

// 推荐：使用共享元素转场
// PageA.ets
@Entry
@Component
struct PageA {
  build() {
    Column() {
      Image('placeholder.png')
        .width(100).height(100)
        .sharedTransition('heroImage') // 定义共享元素ID
        .onClick(() => {
          Router.pushUrl({ url: 'pages/PageB' });
        })
    }
  }
}

// PageB.ets
@Entry
@Component
struct PageB {
  build() {
    Column() {
      Image('placeholder.png')
        .width(300).height(300)
        .sharedTransition('heroImage') // 相同ID，自动匹配
    }
  }
}
```

### 避免写法
```arkts
// 避免：在动画中直接修改布局属性
@Entry
@Component
struct BadAnimationExample {
  @State currentWidth: number = 100;
  @State currentHeight: number = 100;

  build() {
    Column() {
      Button('改变大小')
        .width(this.currentWidth) // 避免在动画中直接改变width/height
        .height(this.currentHeight) // 避免在动画中直接改变width/height
        .backgroundColor(Color.Red)
        .onClick(() => {
          // 这种方式会导致UI树的重新布局和重绘，性能较差
          animateTo({ duration: 300 }, () => {
            this.currentWidth = 200;
            this.currentHeight = 200;
          });
        })
    }
    .width('100%').height('100%')
    .justifyContent(FlexAlign.Center)
  }
}
```

## 注意事项

-   **转场曲线**: 页面转场曲线优先使用**弹簧曲线 (Curve.Spring)**，以提供更自然的动效。
-   **内存管理**: 注意及时释放不再需要的动画资源，防止内存泄漏。
-   **跨应用转场**: 对于跨应用转场，应遵循系统规范，确保体验一致性。
-   **调试**: 利用DevEco Studio的性能分析工具（如CPU Profiler, UI Latency）对动画进行性能监控和调试。