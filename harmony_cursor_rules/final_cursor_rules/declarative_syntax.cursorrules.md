# HarmonyOS 声明式语法 - Cursor Rules

你正在为HarmonyOS应用开发相关功能。以下是你需要遵循的开发规则。

## 核心原则

-   **UI是状态的函数**: 确保UI显示与应用状态始终一致，状态变更可预测。
-   **性能优先**: 优化UI刷新机制，避免不必要的组件渲染，提升应用性能。
-   **状态与UI解耦**: 将状态管理逻辑从UI组件中分离，提高组件复用性和代码可维护性。
-   **单向数据流**: 遵循明确的数据流向，简化状态管理复杂度。

## 推荐做法

### 代码结构
-   **集中共享状态**: 对于多组件共享的状态，推荐使用`StateStore`进行全局管理，将数据集中存储，实现状态与UI的解耦。
-   **观测数据定义**: 所有需要被`StateStore`管理且能触发UI更新的业务数据，必须使用`@Observed`或`@ObservedV2`装饰器修饰。
-   **纯函数Reducer**: 将所有的状态更新逻辑封装在独立的纯函数（Reducer）中，确保状态变更的单一职责和可预测性。

### 最佳实践
-   **理解刷新机制**: 深入理解`@State`, `@Prop`, `@Link`等装饰器的工作原理，明确它们如何触发UI刷新。
-   **审慎使用`@Link`**: `Link`实现双向绑定。若仅需单向传递数据，优先考虑`@Prop`或普通参数，以减少不必要的子组件刷新范围。
-   **按需使用状态变量**: 仅当变量的改变需要触发UI更新时，才使用相应的状态装饰器对其进行标记。
-   **事件驱动状态更新**: 状态的改变应发生在用户交互（如`onClick`）、生命周期回调（如`onAppear`）、数据请求回调等明确的事件中。

## 禁止做法

-   **`build`方法副作用**: 绝对避免在组件的`build`方法或其直接调用的计算属性/函数中修改非状态变量或执行其他副作用操作。
-   **冗余状态变量**: 禁止将未关联任何UI组件、或仅被读取但从未被修改的变量定义为状态变量（例如，未在`build`方法中使用的`@State`变量）。
-   **不必要的`@Link`**: 避免在仅需单向数据流的场景下使用`@Link`，这会增加不必要的双向依赖和刷新风险。

## 代码示例

### 推荐写法
```arkts
@Component
struct MyCounter {
  @State count: number = 0; // 状态变量，UI依赖

  build() {
    Column() {
      Text(`当前计数: ${this.count}`)
        .fontSize(24)
      Button('增加')
        .onClick(() => {
          this.count++; // 状态在事件回调中修改，触发UI刷新
        })
    }
  }
}
```

### 避免写法
```arkts
// 避免写法1: 在build方法直接调用的函数中引入副作用
@Component
struct BadImageEffect {
  private currentOpacity: number = 0; // 非状态变量

  // 该函数在每次build时都会被调用，意外修改非状态变量
  private calculateOpacity(): number {
    this.currentOpacity = (this.currentOpacity + 0.1) % 1;
    return this.currentOpacity;
  }

  build() {
    Image('icon.png')
      .opacity(this.calculateOpacity()) // 每次UI刷新都累加opacity
  }
}

// 避免写法2: 冗余状态变量
@Entry
@Component
struct BadComponent {
  // 变量未关联任何UI组件，或仅被读取但未修改，不应定义为状态变量
  @State unusedData: string = 'some data';
  @State readonlyMessage: string = 'Hello';

  build() {
    Column() {
      // 仅读取readonlyMessage，未修改
      Text(this.readonlyMessage)
    }
  }
}
```

## 注意事项

-   **利用开发工具**: 使用HarmonyOS提供的诊断工具（如`hidumper`）来分析应用运行时状态变量的变化和UI组件的刷新情况，定位冗余刷新问题。
-   **代码静态检查**: 定期使用`Code Linter`工具进行代码检查，重点关注性能优化规则（如`@performance/hp-arkui-remove-redundant-state-var`），并根据扫描结果进行优化。