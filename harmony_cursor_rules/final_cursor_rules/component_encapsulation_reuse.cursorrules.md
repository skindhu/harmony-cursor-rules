# HarmonyOS 组件封装与复用 - Cursor Rules

你正在为HarmonyOS应用开发相关功能。以下是你需要遵循的开发规则。

## 核心原则

-   **高效复用，减少开销：** 通过组件缓存和生命周期管理，避免频繁创建和销毁UI对象，提升渲染效率。
-   **统一封装，提升维护：** 采用标准化的封装模式，如`attributeModifier`，统一组件API风格，简化调用和维护。
-   **数据优化，避免冗余：** 选择高效的数据传递方式，减少不必要的深拷贝和重复更新。
-   **按需加载，动态渲染：** 利用动态UI能力实现组件的预创建和按需加载，优化页面响应速度。

## 推荐做法

### 推荐做法

-   **组件复用声明与生命周期：**
    -   使用`@Reusable`装饰器修饰自定义组件，使其具备复用能力。
    -   在`aboutToReuse()`生命周期回调中，根据新数据刷新组件UI，而非在构造函数中执行所有初始化逻辑。
    -   通过`reuseId`属性对不同结构或用途的可复用组件进行精细化分组，提高缓存匹配效率。
-   **数据传递与状态更新：**
    -   对于复杂对象或数组，优先使用`@Link`或`@ObjectLink`装饰器传递引用，避免深拷贝带来的性能开销。
    -   避免在`aboutToReuse()`中对会自动更新的状态变量（如`@Link`、`@ObjectLink`、`@Prop`）进行重复赋值。
-   **公用组件封装：**
    -   利用ArkTS提供的`attributeModifier`属性方法，对系统组件进行封装，实现链式调用风格，统一API。
    -   提供方可暴露`AttributeModifier`接口实现类，供调用方通过`.attributeModifier()`方法传入。
-   **弹窗组件封装：**
    -   使用`UIContext`中获取的`PromptAction`对象来管理自定义弹窗的显示与隐藏，确保生命周期正确。
-   **动态UI与性能优化：**
    -   对于需要频繁动态增删改查组件、或组件树深度和复杂度较高的场景，优先使用`FrameNode`配合`NodeController`进行组件的创建、管理和局部渲染，以获得更好的性能。
    -   利用`onIdle()`生命周期回调或其他空闲时间进行组件预创建和缓存，减少用户感知到的加载延迟。

## 禁止做法

-   **函数作为入参：** 避免将函数方法直接作为复用组件的入参，这可能导致组件无法有效复用或引起不必要的渲染更新。
-   **`@Prop`深拷贝复杂数据：** 避免使用`@Prop`传递大型或复杂的对象/数组，这会导致不必要的深拷贝，影响性能。
-   **传统冗余封装：** 避免采用导致自定义组件入参列表过长、使用方式与系统组件不一致的传统封装方式。
-   **过度依赖声明式`diff`：** 在需要频繁动态增删改查组件、或组件树深度和复杂度较高时，仅依赖声明式范式可能导致`diff`算法开销过大，影响性能。
-   **整体重绘操作局部：** 避免为了操作或移动局部子组件树而重新渲染整个父组件，导致不必要的性能浪费。

## 代码示例

### 推荐写法

```arkts
// 推荐：@Reusable 组件及 aboutToReuse 生命周期
@Reusable
@Component
struct ReusableListItem {
  private itemData: string = ''; // 初始化，但数据更新在aboutToReuse
  aboutToReuse(params: { data: string }) {
    this.itemData = params.data; // 从缓存取出时，更新数据
  }
  build() {
    Text(this.itemData)
      .fontSize(16)
      .fontColor(Color.Black);
  }
}

// 推荐：使用 attributeModifier 封装公用组件样式
class CommonButtonModifier implements AttributeModifier<ButtonAttribute> {
  applyNormalAttribute(instance: ButtonAttribute): void {
    instance.fontSize(18).fontColor(Color.White).backgroundColor(Color.Blue);
  }
}
// 使用方式
Button('提交').attributeModifier(new CommonButtonModifier());
```

### 避免写法

```arkts
// 避免：传统组件封装导致入参过多且非链式调用
@Component
struct MyLegacyButton {
  @Prop text: string = '';
  @Prop fontSize: number = 14;
  @Prop textColor: Color = Color.Black;
  @Prop bgColor: Color = Color.Gray;
  // ... 如果要支持所有Button属性，此处将非常冗长
  build() {
    Button(this.text)
      .fontSize(this.fontSize)
      .fontColor(this.textColor)
      .backgroundColor(this.bgColor);
  }
}
// 调用方式: <MyLegacyButton text="确认" fontSize={16} textColor={Color.Red} bgColor={Color.Green}/>
```

## 注意事项

-   **性能监控：** 在开发和测试阶段，务必关注应用的帧率、内存占用和CPU使用情况，尤其是在列表滑动、页面切换和复杂动画场景。
-   **`FrameNode`适用性：** `FrameNode`虽性能优越，但其使用场景相对特定，主要用于对性能有极高要求且需要直接操作UI树的动态布局，并非所有动态UI都需要采用。
-   **调试：** 利用HarmonyOS提供的DevEco Studio调试工具，特别是UI调试器，分析组件树结构和渲染性能。