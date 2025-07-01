# ArkTS Lint Rules - Cursor Rules

## 概述
ArkTS（TypeScript的子集）的Lint规则，用于确保代码符合HarmonyOS开发规范。

## 规则统计
- 总规则数量: 67
- 严重程度: error
- 适用范围: ArkTS/TypeScript代码

## 规则列表

### JSON格式
```json
[
  {
    "name": "arkts-no-aliases-by-index",
    "severity": "error",
    "description": "ArkTS不支持索引访问类型。",
    "suggestion": "请改用类型名称。"
  },
  {
    "name": "arkts-no-ambient-decls",
    "severity": "error",
    "description": "ArkTS不支持环境模块声明，因为它有自己的与JavaScript互操作的机制。",
    "suggestion": "请从原始模块中导入所需的内容。"
  },
  {
    "name": "arkts-no-any-unknown",
    "severity": "error",
    "description": "ArkTS不支持any和unknown类型。",
    "suggestion": "请显式指定类型。"
  },
  {
    "name": "arkts-no-as-const",
    "severity": "error",
    "description": "ArkTS不支持as const断言，因为在标准TypeScript中，as const用于使用相应的字面量类型标注字面量，而ArkTS不支持字面量类型。",
    "suggestion": "请避免使用as const断言。请改用字面量的显式类型标注。"
  },
  {
    "name": "arkts-no-call-signatures",
    "severity": "error",
    "description": "ArkTS不支持对象类型中的调用签名。",
    "suggestion": "请改用class（类）来实现。"
  },
  {
    "name": "arkts-no-class-literals",
    "severity": "error",
    "description": "ArkTS不支持类字面量。",
    "suggestion": "请显式引入新的命名类类型。"
  },
  {
    "name": "arkts-no-classes-as-obj",
    "severity": "error",
    "description": "ArkTS不支持将类用作对象（将其赋值给变量等）。这是因为在ArkTS中，类声明引入的是一种新类型，而不是一个值。",
    "suggestion": "请勿将类用作对象；类声明引入的是一种新类型，而不是一个值。"
  },
  {
    "name": "arkts-no-comma-outside-loops",
    "severity": "error",
    "description": "ArkTS仅在for循环中支持逗号运算符。在其他情况下，逗号运算符是无用的，因为它会使执行顺序更难理解。",
    "suggestion": "在for循环之外，请使用显式执行顺序而不是逗号运算符。"
  },
  {
    "name": "arkts-no-conditional-types",
    "severity": "error",
    "description": "ArkTS不支持条件类型别名。",
    "suggestion": "请显式引入带约束的新类型，或使用Object重写逻辑。不支持infer关键字。"
  },
  {
    "name": "arkts-no-ctor-prop-decls",
    "severity": "error",
    "description": "ArkTS不支持在构造函数中声明类字段。",
    "suggestion": "请在类声明内部声明类字段。"
  },
  {
    "name": "arkts-no-ctor-signatures-funcs",
    "severity": "error",
    "description": "ArkTS不支持使用构造函数类型。",
    "suggestion": "请改用lambdas（匿名函数）。"
  },
  {
    "name": "arkts-no-ctor-signatures-iface",
    "severity": "error",
    "description": "ArkTS不支持接口中的构造函数签名。",
    "suggestion": "请改用方法（methods）。"
  },
  {
    "name": "arkts-no-ctor-signatures-type",
    "severity": "error",
    "description": "ArkTS不支持对象类型中的构造函数签名。",
    "suggestion": "请改用class（类）来实现。"
  },
  {
    "name": "arkts-no-decl-merging",
    "severity": "error",
    "description": "ArkTS不支持声明合并。",
    "suggestion": "请保持代码库中所有类和接口的定义紧凑。"
  },
  {
    "name": "arkts-no-definite-assignment",
    "severity": "error",
    "description": "ArkTS不支持确定性赋值断言let v!: T，因为它们被认为是过度的编译器提示。使用确定性赋值断言运算符（!）需要运行时类型检查，导致额外的运行时开销并生成此警告。",
    "suggestion": "请改用带初始化的声明。如果使用了!，请确保实例属性在使用前已赋值，并注意运行时开销和警告。"
  },
  {
    "name": "arkts-no-delete",
    "severity": "error",
    "description": "ArkTS假定对象布局在编译时已知且运行时不可更改。因此，删除属性的操作没有意义。",
    "suggestion": "为了模拟原始语义，您可以声明一个可空类型并赋值为null以标记值的缺失。"
  },
  {
    "name": "arkts-no-destruct-assignment",
    "severity": "error",
    "description": "ArkTS不支持解构赋值。",
    "suggestion": "请改用其他惯用法（例如，在适用情况下使用临时变量）代替。"
  },
  {
    "name": "arkts-no-destruct-decls",
    "severity": "error",
    "description": "ArkTS不支持解构变量声明。这是一个依赖于结构兼容性的动态特性。",
    "suggestion": "创建中间对象并逐字段操作，不受名称限制。"
  },
  {
    "name": "arkts-no-destruct-params",
    "severity": "error",
    "description": "ArkTS要求参数直接传递给函数，并手动分配局部名称。",
    "suggestion": "请将参数直接传递给函数，并手动分配局部名称，而不是使用解构参数声明。"
  },
  {
    "name": "arkts-no-enum-merging",
    "severity": "error",
    "description": "ArkTS不支持枚举的声明合并。",
    "suggestion": "请保持代码库中每个枚举的声明紧凑。"
  },
  {
    "name": "arkts-no-enum-mixed-types",
    "severity": "error",
    "description": "ArkTS不支持使用在程序运行时评估的表达式初始化枚举成员。此外，所有显式设置的初始化器必须是相同类型。",
    "suggestion": "请仅使用相同类型的编译时表达式初始化枚举成员。"
  },
  {
    "name": "arkts-no-export-assignment",
    "severity": "error",
    "description": "ArkTS不支持export = ...语法。",
    "suggestion": "请改用普通的export和import语法。"
  },
  {
    "name": "arkts-no-extend-same-prop",
    "severity": "error",
    "description": "ArkTS不允许接口包含两个具有不可区分签名的方法（例如，参数列表相同但返回类型不同）。",
    "suggestion": "请避免接口扩展具有相同方法签名的其他接口。重构方法名称或返回类型。"
  },
  {
    "name": "arkts-no-for-in",
    "severity": "error",
    "description": "ArkTS不支持通过for .. in循环遍历对象内容。对于对象，运行时遍历属性被认为是冗余的，因为对象布局在编译时已知且运行时不可更改。",
    "suggestion": "对于数组，请使用常规的for循环进行迭代。"
  },
  {
    "name": "arkts-no-func-apply-call",
    "severity": "error",
    "description": "ArkTS不支持Function.apply或Function.call。这些API在标准库中用于显式设置被调用函数的this参数。在ArkTS中，this的语义被限制为传统的OOP风格，并且禁止在独立函数中使用this。",
    "suggestion": "请避免使用Function.apply和Function.call。请遵循传统的OOP风格来处理this的语义。"
  },
  {
    "name": "arkts-no-func-bind",
    "severity": "error",
    "description": "ArkTS不支持Function.bind。这些API在标准库中用于显式设置被调用函数的this参数。在ArkTS中，this的语义被限制为传统的OOP风格，并且禁止在独立函数中使用this。",
    "suggestion": "请避免使用Function.bind。请遵循传统的OOP风格来处理this的语义。"
  },
  {
    "name": "arkts-no-func-expressions",
    "severity": "error",
    "description": "ArkTS不支持函数表达式。",
    "suggestion": "请改用箭头函数来显式指定。"
  },
  {
    "name": "arkts-no-func-props",
    "severity": "error",
    "description": "ArkTS不支持在函数上声明属性，因为不支持具有动态更改布局的对象。函数对象遵循此规则，其布局在运行时不可更改。",
    "suggestion": "请勿直接在函数上声明属性，因为它们的布局在运行时不可更改。"
  },
  {
    "name": "arkts-no-generators",
    "severity": "error",
    "description": "ArkTS当前不支持生成器函数。",
    "suggestion": "请使用async/await机制进行多任务处理。"
  },
  {
    "name": "arkts-no-globalthis",
    "severity": "error",
    "description": "ArkTS不支持全局作用域和globalThis，因为不支持具有动态更改布局的无类型对象。",
    "suggestion": "请使用显式模块导出和导入来在文件之间共享数据，而不是依赖全局作用域。"
  },
  {
    "name": "arkts-no-implicit-return-types",
    "severity": "error",
    "description": "ArkTS支持函数返回类型推断，但此功能目前受到限制。特别是，当return语句中的表达式是对返回类型被省略的函数或方法的调用时，会发生编译时错误。",
    "suggestion": "当返回类型被省略时，请显式指定函数的返回类型。"
  },
  {
    "name": "arkts-no-import-assertions",
    "severity": "error",
    "description": "ArkTS不支持导入断言，因为导入在ArkTS中是编译时特性，而不是运行时特性。因此，对于静态类型语言来说，在运行时断言导入API的正确性没有意义。",
    "suggestion": "请改用普通的import语法；导入的正确性将在编译时检查。"
  },
  {
    "name": "arkts-no-in",
    "severity": "error",
    "description": "ArkTS不支持in运算符。此运算符意义不大，因为对象布局在编译时已知且运行时不可更改。",
    "suggestion": "如果您想检查是否存在某些类成员，请使用instanceof作为替代方案。"
  },
  {
    "name": "arkts-no-indexed-signatures",
    "severity": "error",
    "description": "ArkTS不允许索引签名。",
    "suggestion": "请改用数组（arrays）。"
  },
  {
    "name": "arkts-no-inferred-generic-params",
    "severity": "error",
    "description": "ArkTS允许在函数调用时省略泛型类型参数（如果可以从传递给函数的参数中推断出具体类型），否则会发生编译时错误。特别地，仅基于函数返回类型推断泛型类型参数是被禁止的。",
    "suggestion": "当推断受限时（特别是仅基于函数返回类型时），请显式指定返回类型。"
  },
  {
    "name": "arkts-no-intersection-types",
    "severity": "error",
    "description": "ArkTS当前不支持交叉类型。",
    "suggestion": "请使用继承（inheritance）作为替代方案。"
  },
  {
    "name": "arkts-no-is",
    "severity": "error",
    "description": "ArkTS不支持is运算符，必须将其替换为instanceof运算符。请注意，在使用对象字段之前，必须使用as运算符将其转换为适当的类型。",
    "suggestion": "请将is运算符替换为instanceof。在使用对象字段之前，请使用as运算符将其转换为适当的类型。"
  },
  {
    "name": "arkts-no-jsx",
    "severity": "error",
    "description": "ArkTS不支持JSX表达式。",
    "suggestion": "请勿使用JSX，因为没有提供替代方案来重写它。"
  },
  {
    "name": "arkts-no-mapped-types",
    "severity": "error",
    "description": "ArkTS不支持映射类型。",
    "suggestion": "请使用其他语言惯用法和常规类来实现相同的行为。"
  },
  {
    "name": "arkts-no-method-reassignment",
    "severity": "error",
    "description": "ArkTS不支持重新分配对象方法。在静态类型语言中，对象的布局是固定的，同一对象的所有实例必须共享每个方法的相同代码。",
    "suggestion": "如果需要为特定对象添加特定行为，可以创建单独的包装函数或使用继承。"
  },
  {
    "name": "arkts-no-misplaced-imports",
    "severity": "error",
    "description": "在ArkTS中，所有import语句都应该在程序中的所有其他语句之前。",
    "suggestion": "请将所有import语句放在程序的开头，在任何其他语句之前。"
  },
  {
    "name": "arkts-no-module-wildcards",
    "severity": "error",
    "description": "ArkTS不支持模块名称中的通配符，因为import在ArkTS中是编译时特性，而不是运行时特性。",
    "suggestion": "请改用普通的export语法。"
  },
  {
    "name": "arkts-no-multiple-static-blocks",
    "severity": "error",
    "description": "ArkTS不允许类初始化存在多个静态代码块。",
    "suggestion": "将所有静态代码块语句合并到一个静态代码块中。"
  },
  {
    "name": "arkts-no-nested-funcs",
    "severity": "error",
    "description": "ArkTS不支持嵌套函数。",
    "suggestion": "请改用lambdas（匿名函数）。"
  },
  {
    "name": "arkts-no-new-target",
    "severity": "error",
    "description": "ArkTS不支持new.target，因为语言中没有运行时原型继承的概念。此功能被认为不适用于静态类型。",
    "suggestion": "此功能不适用于静态类型和运行时原型继承，因此不受支持。没有提供直接的替代方案，因为它是一个根本性的差异。"
  },
  {
    "name": "arkts-no-noninferrable-arr-literals",
    "severity": "error",
    "description": "如果数组字面量中至少有一个元素具有不可推断的类型（例如，无类型对象字面量），则会发生编译时错误。",
    "suggestion": "请确保数组字面量中的所有元素都具有可推断的类型，或将元素显式转换为已定义的类型。"
  },
  {
    "name": "arkts-no-ns-as-obj",
    "severity": "error",
    "description": "ArkTS不支持将命名空间用作对象。",
    "suggestion": "请将类或模块解释为命名空间的类似物。"
  },
  {
    "name": "arkts-no-ns-statements",
    "severity": "error",
    "description": "ArkTS不支持命名空间中的语句。",
    "suggestion": "请使用函数来执行语句。"
  },
  {
    "name": "arkts-no-obj-literals-as-types",
    "severity": "error",
    "description": "ArkTS不支持将对象字面量直接用作类型声明。",
    "suggestion": "请显式声明类和接口。"
  },
  {
    "name": "arkts-no-polymorphic-unops",
    "severity": "error",
    "description": "ArkTS只允许一元运算符+、-和~作用于数字类型。如果这些运算符应用于非数字类型，则会发生编译时错误。与TypeScript不同，此上下文中不支持字符串的隐式类型转换，必须显式进行类型转换。",
    "suggestion": "请确保一元运算符+、-和~仅应用于数字类型。如有必要，请执行显式类型转换。"
  },
  {
    "name": "arkts-no-private-identifiers",
    "severity": "error",
    "description": "ArkTS不支持以#符号开头的私有标识符。",
    "suggestion": "请改用private关键字。"
  },
  {
    "name": "arkts-no-props-by-index",
    "severity": "error",
    "description": "ArkTS不支持动态字段声明和访问，也不支持通过索引访问对象字段（obj[\"field\"]）。",
    "suggestion": "请在类中立即声明所有对象字段，并使用obj.field语法访问字段。标准库中的所有类型化数组（如Int32Array）是例外，它们支持通过container[index]语法访问元素。"
  },
  {
    "name": "arkts-no-prototype-assignment",
    "severity": "error",
    "description": "ArkTS不支持原型赋值，因为语言中没有运行时原型继承的概念。此功能被认为不适用于静态类型。",
    "suggestion": "请改用类和/或接口来静态地将方法与数据“组合”在一起。"
  },
  {
    "name": "arkts-no-require",
    "severity": "error",
    "description": "ArkTS不支持通过require导入。它也不支持import赋值。",
    "suggestion": "请改用常规的import语法。"
  },
  {
    "name": "arkts-no-spread",
    "severity": "error",
    "description": "展开运算符唯一支持的场景是将数组或派生自数组的类展开到rest参数或数组字面量中。否则，必要时手动从数组和对象中“解包”数据。",
    "suggestion": "展开运算符仅用于将数组或派生自数组的类展开到rest参数或数组字面量中。对于其他情况，请手动从数组和对象中解包数据。"
  },
  {
    "name": "arkts-no-standalone-this",
    "severity": "error",
    "description": "ArkTS不支持在独立函数和静态方法中使用this。",
    "suggestion": "this只能在实例方法中使用。"
  },
  {
    "name": "arkts-no-structural-typing",
    "severity": "error",
    "description": "ArkTS当前不支持结构化类型。这意味着编译器无法比较两种类型的公共API并判断它们是否相同。",
    "suggestion": "请改用其他机制（继承、接口或类型别名）。"
  },
  {
    "name": "arkts-no-symbol",
    "severity": "error",
    "description": "ArkTS不支持Symbol() API，因为其最常见的用例在静态类型环境中没有意义，对象的布局在编译时定义且运行时不可更改。",
    "suggestion": "除Symbol.iterator外，避免使用Symbol() API。"
  },
  {
    "name": "arkts-no-ts-deps",
    "severity": "error",
    "description": "目前，用标准TypeScript语言实现的 codebase 不得通过导入 ArkTS codebase 来依赖 ArkTS。",
    "suggestion": "请避免TypeScript代码库依赖ArkTS代码库。反向导入（ArkTS导入TS）是支持的。"
  },
  {
    "name": "arkts-no-type-query",
    "severity": "error",
    "description": "ArkTS仅在表达式上下文中支持typeof运算符。不支持使用typeof指定类型标注。",
    "suggestion": "请改用显式类型声明而不是typeof进行类型标注。"
  },
  {
    "name": "arkts-no-types-in-catch",
    "severity": "error",
    "description": "在TypeScript中，catch子句变量类型标注必须是any或unknown（如果指定）。由于ArkTS不支持这些类型，因此请省略类型标注。",
    "suggestion": "请省略catch子句中的类型标注。"
  },
  {
    "name": "arkts-no-typing-with-this",
    "severity": "error",
    "description": "ArkTS不支持使用this关键字进行类型标注。",
    "suggestion": "请改用显式类型。"
  },
  {
    "name": "arkts-no-umd",
    "severity": "error",
    "description": "ArkTS不支持通用模块定义（UMD），因为它没有“脚本”的概念（与“模块”相对）。此外，import在ArkTS中是编译时特性，而不是运行时特性。",
    "suggestion": "请改用普通的export和import语法。"
  },
  {
    "name": "arkts-no-untyped-obj-literals",
    "severity": "error",
    "description": "ArkTS支持对象字面量，前提是编译器可以推断出这些字面量所对应的类或接口。否则，会发生编译时错误。在以下上下文中，不支持使用字面量初始化类和接口：初始化any、Object或object类型；初始化带有方法的类或接口；初始化声明带参数构造函数的类；初始化带有readonly字段的类。",
    "suggestion": "请确保对象字面量对应于显式声明的类或接口。避免将它们用于any、Object、object类型，或用于初始化带有方法、参数化构造函数或只读字段的类。"
  },
  {
    "name": "arkts-no-utility-types",
    "severity": "error",
    "description": "ArkTS目前不支持TypeScript扩展标准库中的实用类型。Partial、Required、Readonly和Record是例外。对于Record<K, V>类型，索引表达式rec[index]的类型为V | undefined。",
    "suggestion": "请避免使用不支持的TypeScript实用类型。Partial、Required、Readonly和Record可用于其特定目的。"
  },
  {
    "name": "arkts-no-var",
    "severity": "error",
    "description": "ArkTS不支持var关键字。",
    "suggestion": "请改用let关键字。"
  },
  {
    "name": "arkts-no-with",
    "severity": "error",
    "description": "ArkTS不支持with语句。",
    "suggestion": "请使用其他语言惯用法来实现相同的行为。"
  }
]
```

## 使用说明

### 在Cursor中使用
1. 将此文件保存为 `.cursorrules` 文件
2. 配置TypeScript/ArkTS项目的ESLint规则
3. 确保IDE能够识别这些规则

### 规则应用
这些规则主要用于：
- TypeScript到ArkTS的迁移
- HarmonyOS应用开发
- 确保代码符合ArkTS规范

## 参考资源
- [HarmonyOS ArkTS开发指南](https://developer.huawei.com/consumer/en/doc/harmonyos-guides-V14/typescript-to-arkts-migration-guide-V14)
- 生成时间: 2025-07-01 20:04:00

---
*此文件由ArkTS规则提取器自动生成*
