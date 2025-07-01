作为资深的HarmonyOS界面开发专家，我已仔细分析您提供的华为官方文档HTML内容，并整理出关于“组件封装”的界面开发最佳实践，具体如下：

# 组件封装 - 最佳实践

## 📋 概述
本模块专注于HarmonyOS应用开发中ArkUI组件的封装与复用。通过对组件进行合理的封装，可以提高代码的复用性、可维护性，并统一界面风格。文档主要介绍了以下三种典型的组件封装与复用场景：
1.  **公用组件封装**：对系统组件进行封装，形成公共组件库，统一UX规范。
2.  **弹窗组件封装**：封装自定义弹窗，并通过统一接口控制其显隐。
3.  **组件工厂类封装**：通过工厂模式统一管理和暴露组件，实现按需获取。

## 🎯 最佳实践

### 1. 公用组件封装
- **实践要点**：
    *   统一组件使用方式，使其与系统组件保持一致的链式调用风格。
    *   避免自定义组件的入参列表过长，简化组件调用。
    *   提高组件的可维护性，当系统组件属性变更时，减少自定义组件的适配成本。
- **实现方式**：
    *   **核心机制**：利用ArkTS为每个系统组件提供的 `attributeModifier` 属性方法。
    *   **原理**：`attributeModifier` 将组件属性设置分离到系统提供的 `AttributeModifier` 接口实现类实例中。通过自定义Class类实现 `AttributeModifier` 接口，对系统组件属性进行扩展。
    *   **两种推荐方案**：
        1.  **提供方对外提供封装好的自定义组件**：自定义组件内部包含系统组件，并支持外部传入 `attributeModifier` 属性，由外部控制系统组件的更多属性。
        2.  **提供方提供 `AttributeModifier` 接口实现类**：提供方将封装好的 `AttributeModifier` 接口实现类暴露给调用方，调用方直接通过系统组件的 `.attributeModifier()` 方法传入该实例。这种方式更接近系统组件的使用习惯。
- **注意事项**：
    *   `attributeModifier` 是解决传统封装方式缺点（使用方式不一致、入参过大、维护困难）的关键。
    *   通过 `AttributeModifier` 接口，可以在自定义组件中扩展系统组件的全部基础能力，并保持链式调用风格。

### 2. 弹窗组件封装
- **实践要点**：
    *   实现自定义弹窗的统一封装。
    *   提供清晰、集中的方式来控制弹窗的显示与隐藏。
- **实现方式**：
    *   推荐使用 `UIContext` 中获取到的 `PromptAction` 对象来实现自定义弹窗。
    *   调用方通过 `PromptAction` 对象的 `openCustomDialog` 方法显示弹窗，通过 `closeCustomDialog` 方法关闭弹窗。
- **注意事项**：
    *   `UIContext` 和 `PromptAction` 是HarmonyOS官方推荐的自定义弹窗管理方式，能够确保弹窗的正确生命周期管理和交互。

### 3. 组件工厂类封装
- **实践要点**：
    *   统一管理和对外暴露所有封装好的组件。
    *   调用方通过传入不同的参数，从工厂类中获取对应的组件实例。
- **实现方式**：
    *   创建一个组件工厂类，内部封装了各种组件的创建逻辑。
    *   工厂类对外提供统一的接口（如一个方法），根据传入的枚举值或配置参数，返回相应的组件实例。
- **注意事项**：
    *   适用于需要根据不同条件动态创建或获取多种类似组件的场景。
    *   提高了组件管理的集中性和灵活性，降低了调用方直接创建组件的复杂性。

## 💡 代码示例

### 传统公用组件封装 (应避免的做法)
这种方式导致入参过大且使用方式与系统组件不一致。
```arkts
// src/main/ets/view/CustomImageText.ets
@Component
struct MyButton {
 @Prop text: string = '';
 @Prop stateEffect: boolean = true; // 如果要支持Button所有属性，需要在此处穷举
 build() {
  Button(this.text)
   .fontSize(12)
   .fontColor($r('sys.color.comp_background_list_card'))
   .stateEffect(this.stateEffect)
 }
}

// 使用方式 (缺点：非链式调用，参数列表冗长)
@Component
struct Index {
 build() {
  MyButton({ text: 'Click with animation', stateEffect: true })
 }
}
```

### 使用 `attributeModifier` 进行公用组件封装 (推荐做法 - 方案一 Provider部分)
提供方封装自定义组件，支持传入 `attributeModifier`。
```arkts
//Provider customizes and exports components
@Component
export struct MyButton {
 @Prop attributeModifier: AttributeModifier<ButtonAttribute> = new ButtonAttribute(); // 接收外部传入的attributeModifier
 @Prop text: string = ''; // 仍可保留一些自定义属性

 build() {
  Button(this.text)
   .fontSize(12) // 默认公共样式
   .fontColor($r('sys.color.comp_background_list_card')) // 默认公共样式
   .attributeModifier(this.attributeModifier) // 应用外部传入的attributeModifier
 }
}
```
*(注：文档中未提供完整的 `AttributeModifier` 实现类和调用方使用示例，此处仅展示了文档中明确给出的 `MyButton` 定义部分。)*

## ⚠️ 常见陷阱

### 避免的做法
-   **自定义组件入参过大**：为了支持系统组件的全量属性，在自定义组件中以 `Prop` 形式穷举所有属性，导致组件的构造函数参数列表过于庞大。
-   **使用方式与系统组件不一致**：自定义组件通过参数列表设置属性，而系统组件通过链式调用设置属性，导致混合使用时代码风格不统一，降低可读性。
-   **不利于后期维护**：当所封装的系统组件的属性发生变更或新增时，自定义组件需要同步修改其 `Prop` 定义，维护成本高。

### 推荐的做法
-   **利用 `attributeModifier` 统一属性设置**：将系统组件属性的设置逻辑通过 `AttributeModifier` 接口实现类进行封装，并通过 `attributeModifier` 属性传入自定义组件，保持与系统组件一致的链式调用体验。
-   **使用 `UIContext.PromptAction` 管理弹窗**：对于自定义弹窗，遵循官方推荐，通过 `UIContext` 获取 `PromptAction` 对象来统一管理弹窗的生命周期和显隐。
-   **采用组件工厂模式**：对于需要动态生成或根据不同配置提供不同组件的场景，使用工厂类来统一创建和管理组件，提高代码的组织性和灵活性。

## 🔗 相关资源
- 原文档：https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-ui-component-encapsulation