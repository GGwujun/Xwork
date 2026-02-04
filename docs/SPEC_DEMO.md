 Web版计算器模块实现方案

 项目概述

 在Winning Web Portal系统中实现一个功能完整的web版计算器模块，支持基础四则运算、科学计算、历史记录和内存功能， 
 作为独立的功能页面提供服务。

 技术栈和约束

 - 框架: Vue 3 + Composition API + TypeScript
 - 构建工具: Spark Framework v2.0.0+
 - UI组件: WinDesign组件库（w-*前缀）
 - 样式: Tailwind CSS + SCSS + BEM命名规范
 - 状态管理: Pinia
 - 存储: localStorage本地存储
 - 文件权限: 只能修改src/pages/、src/components/等指定目录

 整体架构设计

 目录结构

 src/pages/calculator/
 ├── index.vue                    # 主页面入口
 ├── api/
 │   └── storage.ts              # 本地存储API封装
 ├── components/
 │   ├── CalculatorDisplay.vue   # 显示屏组件
 │   ├── BasicKeypad.vue         # 基础按键盘
 │   ├── ScientificKeypad.vue    # 科学计算按键盘
 │   ├── HistoryPanel.vue        # 历史记录面板
 │   ├── MemoryPanel.vue         # 内存功能面板
 │   └── CalculatorButton.vue    # 通用按钮组件
 ├── composables/
 │   ├── useCalculator.ts        # 计算器核心逻辑
 │   ├── useHistory.ts           # 历史记录管理
 │   └── useMemory.ts            # 内存功能管理
 ├── utils/
 │   ├── calculator-engine.ts    # 计算引擎
 │   ├── formatter.ts            # 数字格式化
 │   └── constants.ts            # 常量定义
 ├── types/
 │   └── calculator.ts           # TypeScript类型定义
 └── styles/
     └── calculator.scss         # 样式文件

 组件架构

 - 主容器: index.vue - 整体布局和模式切换
 - 显示组件: CalculatorDisplay.vue - 数字显示和表达式展示
 - 输入组件: BasicKeypad.vue / ScientificKeypad.vue - 按键输入
 - 功能面板: HistoryPanel.vue / MemoryPanel.vue - 辅助功能
 - 通用组件: CalculatorButton.vue - 可复用按钮

 核心功能实现

 1. 计算引擎设计

 // utils/calculator-engine.ts
 export class CalculatorEngine {
   // 基础运算
   static basicOperations = {
     '+': (a: number, b: number) => a + b,
     '-': (a: number, b: number) => a - b,
     '*': (a: number, b: number) => a * b,
     '/': (a: number, b: number) => a / b,
     '%': (a: number, b: number) => a % b
   }

   // 科学计算
   static scientificOperations = {
     'sin': Math.sin,
     'cos': Math.cos,
     'tan': Math.tan,
     'log': Math.log10,
     'ln': Math.log,
     'sqrt': Math.sqrt,
     'pow': Math.pow,
     'factorial': (n: number) => { /* 阶乘实现 */ }
   }

   // 表达式求值
   static evaluate(expression: string): number
   static validateExpression(expression: string): boolean
 }

 2. 状态管理（Pinia Store）

 // stores/calculator.ts
 export const useCalculatorStore = defineStore('calculator', () => {
   // 计算状态
   const display = ref('0')
   const expression = ref('')
   const lastResult = ref(0)
   const mode = ref<'basic' | 'scientific'>('basic')

   // 历史记录
   const history = ref<CalculationRecord[]>([])

   // 内存功能
   const memory = ref<number[]>([])

   // 操作方法
   const inputNumber = (num: string) => { /* 数字输入逻辑 */ }
   const inputOperator = (op: string) => { /* 运算符输入逻辑 */ }
   const calculate = () => { /* 计算逻辑 */ }
   const clear = () => { /* 清除逻辑 */ }

   return {
     display, expression, lastResult, mode,
     history, memory,
     inputNumber, inputOperator, calculate, clear
   }
 })

 3. 本地存储管理

 // api/storage.ts
 export class CalculatorStorage {
   private static readonly KEYS = {
     HISTORY: 'calculator_history',
     MEMORY: 'calculator_memory',
     SETTINGS: 'calculator_settings'
   }

   static saveHistory(history: CalculationRecord[]): void
   static loadHistory(): CalculationRecord[]
   static saveMemory(memory: number[]): void
   static loadMemory(): number[]
   static clearAll(): void
 }

 4. 类型定义

 // types/calculator.ts
 export interface CalculationRecord {
   id: string
   expression: string
   result: number
   timestamp: Date
   mode: 'basic' | 'scientific'
 }

 export interface CalculatorState {
   display: string
   expression: string
   lastResult: number
   mode: 'basic' | 'scientific'
   isNewCalculation: boolean
 }

 export type OperatorType = '+' | '-' | '*' | '/' | '%' | '=' | 'C' | 'CE'
 export type ScientificFunction = 'sin' | 'cos' | 'tan' | 'log' | 'ln' | 'sqrt' | 'pow'

 UI界面设计

 布局方案

 采用卡片式布局，分为以下区域：
 - 显示区域: 当前数值和表达式显示
 - 模式切换: 基础/科学计算模式切换
 - 按键区域: 根据模式显示不同按键布局
 - 功能面板: 历史记录和内存功能（可折叠）

 响应式设计

 // styles/calculator.scss
 .calculator {
   max-width: 800px;
   margin: 0 auto;

   &__display {
     background: var(--w-color-bg-1);
     border: 1px solid var(--w-border-color);
     border-radius: 8px;
     padding: 20px;
     margin-bottom: 16px;
   }

   &__keypad {
     display: grid;
     gap: 8px;

     &--basic {
       grid-template-columns: repeat(4, 1fr);
     }

     &--scientific {
       grid-template-columns: repeat(6, 1fr);
     }
   }

   &__panels {
     display: flex;
     gap: 16px;
     margin-top: 16px;

     @media (max-width: 768px) {
       flex-direction: column;
     }
   }
 }

 WinDesign组件使用

 - w-card: 主容器和功能面板
 - w-button: 计算器按键
 - w-input: 显示屏（只读）
 - w-tabs: 模式切换
 - w-collapse: 历史记录折叠面板
 - w-tag: 内存数值标签
 - w-tooltip: 按键功能提示

 路由和菜单集成

 路由配置

 // 在 src/router/routes.ts 中添加
 {
   path: '/calculator',
   name: 'Calculator',
   component: () => import('@/pages/calculator/index.vue'),
   meta: {
     title: '计算器',
     requiresAuth: true
   }
 }

 菜单配置

 在系统菜单配置中添加计算器入口，建议放在"工具"或"实用工具"分类下。

 开发实施计划

 第一阶段：基础框架搭建

 1. 创建目录结构和基础文件
 2. 设置TypeScript类型定义
 3. 实现基础的Pinia Store
 4. 创建主页面布局

 第二阶段：核心计算功能

 1. 实现计算引擎（基础四则运算）
 2. 开发显示组件和基础按键盘
 3. 实现数字输入和基础运算逻辑
 4. 添加错误处理和边界情况处理

 第三阶段：科学计算功能

 1. 扩展计算引擎（科学函数）
 2. 开发科学计算按键盘
 3. 实现三角函数、对数、指数等功能
 4. 添加角度/弧度模式切换

 第四阶段：辅助功能

 1. 实现历史记录功能
 2. 开发内存功能（M+, M-, MR, MC）
 3. 实现本地存储
 4. 添加设置和偏好功能

 第五阶段：UI优化和测试

 1. 完善响应式设计
 2. 添加键盘快捷键支持
 3. 性能优化
 4. 编写单元测试和集成测试

 质量保证

 测试策略

 - 单元测试: 计算引擎、工具函数
 - 组件测试: 各个Vue组件
 - 集成测试: 完整的计算流程
 - E2E测试: 用户操作场景

 代码质量检查

 - TypeScript类型检查
 - ESLint代码规范检查
 - Prettier代码格式化
 - 构建验证

 性能考虑

 - 大数运算精度处理
 - 历史记录数量限制
 - 组件懒加载
 - 计算结果缓存

 关键文件清单

 核心文件

 - src/pages/calculator/index.vue - 主页面
 - src/pages/calculator/composables/useCalculator.ts - 核心逻辑
 - src/pages/calculator/utils/calculator-engine.ts - 计算引擎
 - src/pages/calculator/stores/calculator.ts - 状态管理

 组件文件

 - src/pages/calculator/components/CalculatorDisplay.vue - 显示屏
 - src/pages/calculator/components/BasicKeypad.vue - 基础按键
 - src/pages/calculator/components/ScientificKeypad.vue - 科学按键
 - src/pages/calculator/components/HistoryPanel.vue - 历史记录
 - src/pages/calculator/components/MemoryPanel.vue - 内存功能

 配置文件

 - src/router/routes.ts - 路由配置（需要修改）
 - 系统菜单配置 - 添加计算器入口

 预期成果

 完成后将提供一个功能完整的web版计算器，具备：
 - ✅ 完整的基础和科学计算功能
 - ✅ 直观易用的用户界面
 - ✅ 历史记录和内存功能
 - ✅ 响应式设计，支持各种屏幕尺寸
 - ✅ 本地数据持久化
 - ✅ 符合项目代码规范和质量标准
 - ✅ 完整的测试覆盖

 该模块将作为系统的实用工具，提升用户体验和系统的完整性。