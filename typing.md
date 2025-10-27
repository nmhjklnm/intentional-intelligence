# typing 

> **说明**：本文档整理 `typing` 模块中的类型提示工具。

---

### **1. 泛型／类型变量／抽象基类辅助**

#### [x] **Any**
- 表示动态类型，可以是任何类型（与 object 不同，更灵活）。
- example: 

#### [x] **TypeVar**
- 定义一个类型变量（泛型参数）。
- example: 

#### [ ] **TypeVarTuple**
- （PEP 646）用于表示可变长度的类型参数元组。
- example: 

#### [ ] **ParamSpec**
- 用于表示可变参数列表（*args, **kwargs）在泛型函数中。
- example: 

#### [ ] **Generic**
- 用于定义泛型类（在旧语法里：class C(Generic[T])）。
- example: 

#### [ ] **GenericAlias**
- 泛型类型的实例化形式（如 list[int]、dict[str, int]）。
- example: 

#### [ ] **ClassVar**
- 标注类变量而非实例变量。
- example: 

#### [ ] **Final**
- 表示不可被重写／继承的变量或方法。
- example: 

#### [ ] **Literal**
- 表示"精确等于"某个字面值的类型。
- example: 

#### [ ] **Annotated**
- 用于在类型提示中附加元数据（如校验、框架标记）。
- example: 

#### [ ] **TypeAlias, TypeAliasType**
- 用于定义类型别名。
- example: 

#### [ ] **Self**
- （PEP 673）在类方法中表示"返回本类实例"的类型。
- example: 

#### [ ] **Never**
- 表示永远不会返回的类型（常用于报警或抛异常函数）。
- example: 

#### [ ] **Union, Optional**
- 虽然在新语法中 | 可以替代 Union，但仍存在于 typing 模块。
- example: 

#### [ ] **Required, NotRequired**
- 用于 TypedDict，标记必需/可选字段。
- example: 

#### [ ] **Unpack**
- 用于解包 TypeVarTuple 和 TypedDict（如 **kwargs: Unpack[Movie]）。
- example: 

#### [ ] **Type**
- 表示"一个类型"的类型（如 Type[int] 表示"类型是 int 的类型"）。
- example: 

#### [ ] **AnyStr**
- 预定义的 TypeVar，约束为 str 或 bytes。
- example: 

#### [ ] **NamedTuple**
- 创建具名元组类（类似 dataclass 但更轻量）。
- example:


### **2. 协议 (Protocol)／支持接口 (Supports…)**

#### [ ] **Protocol**
- 定义结构性类型（只要具备某些方法／属性即可，类似接口）。
- example: 

#### [ ] **runtime_checkable**
- 用作装饰器，使得一个 Protocol 在运行时可用 isinstance() 检查。
- example: 

#### [ ] **SupportsInt, SupportsFloat, SupportsComplex, SupportsIndex, SupportsBytes, SupportsAbs, SupportsRound, …**
- 这些 "SupportsX"用于表示某对象"支持 X 操作"（例如：可转为 int、可索引、可取绝对值等）。
- example: 

#### [ ] **TypedDict**
- （虽然不完全是 Protocol，但属于类型提示结构）表示字典具有固定键/值类型。
- example: 

#### [ ] **Protocol 的子类／组合形式**
- 用于更复杂接口定义。
- example:


### **3. 高阶类型形状／可调用／容器相关**

#### [ ] **Concatenate**
- 用于组合 Callable 参数列表（较高级用法）。
- example: 

#### [ ] **ParamSpecArgs, ParamSpecKwargs**
- 辅助 ParamSpec 表示参数列表中的 args／kwargs。
- example: 

#### [ ] **LiteralString**
- 表示字面量字符串类型（安全性相关）。
- example: 

#### [ ] **ReadOnly**
- 表示只读类型（用于 TypedDict 等）。
- example: 

#### [ ] **TypeGuard**
- 类型守卫，用于类型窄化（较宽松）。
- example: 

#### [ ] **TypeIs**
- 类型谓词，更精确的类型窄化（Python 3.13+，比 TypeGuard 更严格）。
- example: 

#### [ ] **NewType**
- 用于创建比原类型更"特定"的类型别名。
- example: 

#### [ ] **Overload**
- 表示重载函数签名。
- example: 

#### [ ] **get_origin(), get_args(), clear_overloads()**
- 虽是函数但用于类型提示元编程。
- example:


### **4. 类型检查器专用／运行时辅助／版本兼容**

#### [ ] **TYPE_CHECKING**
- 布尔常量，在类型检查器运行时为 True，而运行时代码可据此跳过某些导入。
- example: 

#### [ ] **cast()**
- 用于告诉类型检查器"把这个值当作某类型"。
- example: 

#### [ ] **assert_type()**
- 告诉类型检查器"我断言这个值类型"为某类型（Python 3.11+）。
- example: 

#### [ ] **assert_never()**
- 用于穷尽性检查，确认代码路径不可达（Python 3.11+）。
- example: 

#### [ ] **reveal_type()**
- 调试工具，显示类型检查器推断的类型（Python 3.11+）。
- example: 

#### [ ] **overload()**
- 装饰器，用于声明多个函数签名（静态分析用）。
- example: 

#### [ ] **get_origin(), get_args()**
- 提供类型提示元信息访问。
- example: 

#### [ ] **get_type_hints()**
- 获取对象的类型提示（重要的运行时函数）。
- example: 

#### [ ] **is_protocol()**
- 检查一个类型是否为 Protocol（Python 3.14）。
- example: 

#### [ ] **is_typeddict()**
- 检查一个类型是否为 TypedDict（Python 3.14）。
- example: 

#### [ ] **clear_overloads()**
- 清理已声明的 overload。
- example: 

#### [ ] **@override**
- （PEP 698）用于标记 "覆写父类方法" 的装饰器，帮助类型检查。
- example: 

#### [ ] **@dataclass_transform**
- （PEP 681）用于自定义装饰器的类型提示。
- example: 

#### [ ] **deprecated()**
- 标记已弃用的函数或类的装饰器。
- example: 

#### [ ] **typing_extensions**
- 为旧版本 Python 提供新特性的向后兼容模块。
- example:
