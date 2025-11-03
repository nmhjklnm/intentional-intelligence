# typing 

> **说明**：本文档整理 `typing` 模块中的类型提示工具。

---

### **1. 泛型／类型变量／抽象基类辅助**

#### [x] **Any**
- 表示动态类型，可以是任何类型（与 `object` 不同，更灵活）。语法：`Any`。
- 解释:

#### [x] **TypeVar**
- 定义一个类型变量（泛型参数）。语法：`T = TypeVar('T')`，可使用 `bound` 或约束集合。
- 解释:

#### [x] **TypeVarTuple**
- （PEP 646）用于表示可变长度的类型参数元组。语法：`Ts = TypeVarTuple('Ts')`。
- 解释:

#### [x] **ParamSpec**
- 用于表示可变参数列表（*args, **kwargs）在泛型函数中。语法：`P = ParamSpec('P')`。
- 解释:

#### [x] **Generic**
- 用于定义泛型类。语法：`class C(Generic[T])`（Python 3.12+ 可写 `class C[T]:`）。
- 解释:

#### [x] **GenericAlias**
- 泛型类型的实例化形式。语法：`list[int]`、`dict[str, int]`。
- 解释:

#### [x] **ClassVar**
- 标注类变量而非实例变量。语法：`x: ClassVar[int] = 0`。
- 解释: 标记一个变量为类变量（类变量这个类的所有实例都共享）

#### [x] **Final**
- 表示不可被重写／继承的变量或方法。语法：`NAME: Final[T] = ...`。
- 解释:

#### [x] **Literal**
- 表示"精确等于"某个字面值的类型。语法：`Literal[1, "x"]`。
- 解释:

#### [x] **Annotated**
- 用于在类型提示中附加元数据（如校验、框架标记）。语法：`Annotated[T, ...]`。
- 解释:

#### [x] **TypeAlias, TypeAliasType**
- 用于定义类型别名。语法：`type UserId = int`（Python 3.12+）。或 `UserId: TypeAlias = int`。
- 解释:类型别名就是给某个复杂的类型起个简洁的别名，让代码更易读。
    比如用 UserId 代替 int，让代码有更强的语义表达能力。
    - 比如
        ```
        UserId: TypeAlias = int # 3.12 之前  
        type UserId = int # 3.12 之后.
        ```
        TypeAliasType 是"真实对象"别名（Python 也能看见并操作.
        ```
        
        from typing import TypeAliasType
        UserId = TypeAliasType("UserId", int) # 语法：TypeAliasType("名字", 类型) 运行时可以检查
        print(UserId)  # typing.TypeAliasType[int]
        print(type(UserId))  # <class 'typing.TypeAliasType'>
        ```





#### [x] **Self**
- （PEP 673）在类方法中表示"返回本类实例"的类型。语法：`-> Self`。
- 解释:

#### [x] **Never**
- 表示永远不会返回的类型（常用于报警或抛异常函数）。语法：`-> Never`。
- 解释:

#### [x] **Union, Optional**
- 虽然在新语法中 `|` 可以替代 `Union`，但仍存在于 `typing` 模块。语法：`int | str`。`Optional[T]` 等同于 `T | None`。
- 解释:

#### [x] **Required, NotRequired**
- 用于 `TypedDict`，标记必需/可选字段。语法：在 `TypedDict` 字段上使用，如 `name: Required[str]`，`age: NotRequired[int]`。
- 解释:

#### [x] **Unpack**
- 用于解包 `TypeVarTuple` 和 `TypedDict`。语法：`Unpack[Ts]`。在 `**kwargs` 上可写 `**args: Unpack[TD]`。
- 解释:

#### [x] **Type**
- 表示"一个类型"的类型（如 `Type[int]` 表示"类型是 `int` 的类型"）。语法：`Type[T]`。
- 解释:

#### [x] **AnyStr**
- 预定义的 `TypeVar`，约束为 `str` 或 `bytes`。语法：`AnyStr`。
- 解释:

#### [x] **NamedTuple**
- 创建具名元组类（类似 `dataclass` 但更轻量）。语法：`Point = NamedTuple("Point", [("x", int), ("y", int)])`。
- 解释:
    - NamedTuple 是 Python 中一种创建具名元组类的工具，它让元组的每个位置都有一个名字。与普通元组相比，NamedTuple 的元素既可以通过索引访问（如 point[0]），也可以通过名字访问（如 point.x），让代码更具可读性。
    - 
        ```
        from typing import NamedTuple
        # 方式1：类定义风格（推荐，类似 pydantic 的 BaseModel）
        class Point(NamedTuple): 
            x: int
            y: int
        # 创建实例
        p = Point(10, 20)
        print(p.x)  # 10 - 通过名字访问
        print(p[0])  # 10 - 通过索引访问
        ```


### **2. 协议 (Protocol)／支持接口 (Supports…)**

#### [x] **Protocol**
- 定义结构性类型（只要具备某些方法／属性即可，类似接口）。语法：`class X(Protocol): ...`。
- 解释:
    - Protocol 的结构检查**不仅检查方法签名，也检查属性**（包括类型）。只要对象有对应的属性和方法，就满足 Protocol，无需显式继承（鸭子类型）。
    - 
        ```python
        from typing import Protocol
        
        class HasUserInfo(Protocol):
            user_id: int      # ✅ 可以定义属性
            username: str     # ✅ 可以定义属性
            def get_name(self) -> str: ...  # ✅ 可以定义方法
        
        # 实现时无需继承 Protocol
        class User:
            def __init__(self, uid: int, name: str):
                self.user_id = uid
                self.username = name
            def get_name(self) -> str:
                return self.username
        
        def print_user(u: HasUserInfo) -> None:
            print(f"{u.user_id}: {u.get_name()}")
        
        print_user(User(1, "Alice"))  # ✅ User 满足 Protocol
        ```

#### [x] **runtime_checkable**
- runtime_checkable 是一个装饰器，它让 Protocol 可以在运行时被 isinstance() 和 issubclass() 检查。
- 解释:

#### [x] **SupportsInt, SupportsFloat, SupportsComplex, SupportsIndex, SupportsBytes, SupportsAbs, SupportsRound, …**
- 这些 "SupportsX" 用于表示某对象支持相应操作（如可转为 `int`、可索引、可取绝对值等）。语法：直接使用对应类型，如 `SupportsInt`、`SupportsAbs`。
- 解释:
    - 相当于预定义的一些 Protocol
    - 协议类型	检查的魔法方法	含义
        SupportsInt	__int__()	可转换为 int
        SupportsFloat	__float__()	可转换为 float
        SupportsComplex	__complex__()	可转换为 complex
        SupportsBytes	__bytes__()	可转换为 bytes
        SupportsIndex	__index__()	可用作索引/切片
        SupportsAbs[T]	__abs__()	可求绝对值
        SupportsRound[T]	__round__()	可四舍五入 


#### [x] **TypedDict**
- （虽然不完全是 `Protocol`，但属于类型提示结构）表示字典具有固定键/值类型。语法：`class Movie(TypedDict): ...`。
- 解释:

#### [x] **Protocol 的子类／组合形式**
- 用于更复杂接口定义。语法：`class X(Protocol, Y): ...` 或组合多个 `Protocol`。
- 解释:


### **3. 高阶类型形状／可调用／容器相关**

#### [x] **Concatenate**
- 用于组合 `Callable` 参数列表（较高级用法）。语法：`Concatenate[Arg1, P, ArgN]`。
    解决的问题：假设你要写一个装饰器，它会给原函数额外添加一个参数（比如注入一个数据库连接）。使用普通的 Callable 类型提示时，无法精确表达"在原函数参数列表前面插入一个新参数"。
    本质：Concatenate 是一个类型级别的参数列表拼接器
- 解释:
  ```python
    from typing import Callable, Concatenate, ParamSpec, TypeVar
    P = ParamSpec('P')  # 代表"原函数的参数列表"
    T = TypeVar('T')    # 代表"原函数的返回值类型"
    # 装饰器：在原函数参数前添加一个 str 类型的 db 参数
    def add_db(
        func: Callable[P, T]  # 原函数：接受 P 参数，返回 T
    ) -> Callable[Concatenate[str, P], T]:  # 新函数：接受 str + P 参数，返回 T
        def wrapper(db: str, *args: P.args, **kwargs: P.kwargs) -> T:
            print(f"连接数据库: {db}")
            return func(*args, **kwargs)
        return wrapper
    # 使用装饰器
    @add_db
    def query_user(user_id: int, active: bool = True) -> str:
        return f"查询用户 {user_id}，活跃状态={active}"
    # 调用时必须传入 db 参数
    result = query_user("mysql://localhost", 42, active=False)  # ✅ 类型检查通过
    # result = query_user(42, active=False)  # ❌ mypy 报错：缺少 db 参数
    ```

#### [x] **ParamSpecArgs, ParamSpecKwargs**
- 辅助 `ParamSpec` 表示参数列表中的 `args`／`kwargs`。语法：`P.args`，`P.kwargs`。
- 解释: P.args 就是ParamSpecArgs 
       p.kwargs 同理。

        ParamSpec 是参数的"容器"
        ├── P.args 拆出位置参数
        ├── P.kwargs 拆出关键字参数
        └── Concatenate 在容器前面加新参数
  

#### [x] **LiteralString**
- 表示字面量字符串类型（安全性相关）。语法：`LiteralString`。
- 解释: LiteralString 的设计动机：让类型检查器能够区分哪些字符串是"写死在代码里的"（安全），哪些是"运行时来的"（不安全）。
    不接受外部输入或者动态生成的字符串。
    ```
    from typing import LiteralString
    `def execute_sql(sql: LiteralString) -> None:
        """只接受字面量字符串的函数"""
        print(f"执行 SQL: {sql}")    # ✅ 正确：直接写死的字符串
    execute_sql("SELECT * FROM users")
    table = "users"  # 字面量     # ✅ 正确：字面量拼接
    execute_sql(f"SELECT * FROM {table}")
    user_input = input("输入 SQL: ") # ❌ 错误：来自外部输入
    execute_sql(user_input)  # 类型检查器报错！
    dynamic = "SELECT" + " * FROM users" # ❌ 错误：动态生成
    execute_sql(dynamic)  # 类型检查器报错！
    ````

#### [x] **ReadOnly**
- 表示只读类型（用于 `TypedDict` 等）。语法：`ReadOnly[T]`。
- 解释:
   
    -  ReadOnly[T]：Python 3.13+ 的类型注解，标记 TypedDict 中的只读字段
        ```
        from typing import Final, TypedDict, ReadOnly
        from dataclasses import dataclass

        # Final：变量不能重新赋值
        API_KEY: Final[str] = "secret"
        # API_KEY = "new"  # mypy error

        # ReadOnly：TypedDict 这个字段的值创建之后就不能修改了
        class Config(TypedDict):
            key: ReadOnly[str]

        # frozen dataclass：运行时强制整个对象不可变
        @dataclass(frozen=True)
        class Point:
            x: int
            y: int
        ```

#### [x] **TypeGuard**
- 类型守卫，用于类型窄化。语法：`def is_str(x: object) -> TypeGuard[str]: ...`。
- 解释:

#### [x] **TypeIs**
- 类型谓词，更精确的类型窄化（Python 3.13+）。语法：`def is_str(x: object) -> TypeIs[str]: ...`。
- 解释:

#### [x] **NewType**
- 用于创建比原类型更"特定"的类型别名。语法：`UserId = NewType("UserId", int)`。
**NewType 只在类型检查时有效，运行时它就是一个简单的函数**
提高代码可读性：类型名称直接表达业务含义
- 解释:
    - NewType 是 typing 模块提供的一个工具，用于创建一个基于现有类型的新类型标识。它在类型检查层面创建了一个"独特"的类型，但在运行时仍然是原始类型。
简单说：NewType 让你可以给同一个底层类型（如 int）创建多个"语义上不同"的类型名称。 
        ```
        from typing import NewType

        # 创建新类型：语法是 NewType("类型名", 基础类型)
        UserId = NewType("UserId", int)
        OrderId = NewType("OrderId", int)

        # 使用新类型作为类型提示
        def get_user(user_id: UserId) -> str:
            return f"User {user_id}"

        def get_order(order_id: OrderId) -> str:
            return f"Order {order_id}"

        # 创建新类型的值：需要显式调用构造器
        user_id = UserId(12345)  # ✅ 正确
        order_id = OrderId(67890)  # ✅ 正确

        # 使用
        print(get_user(user_id))  # ✅ 类型正确
        print(get_order(order_id))  # ✅ 类型正确

        # ❌ 类型检查器会报错
        print(get_user(order_id))  # 错误：期望 UserId，得到 OrderId
        print(get_order(user_id))  # 错误：期望 OrderId，得到 UserId
        ```

#### [x] **Overload**
- 表示重载函数签名。语法：`@overload`。
- 解释:
    @overload 是 Python 类型提示系统中的一个装饰器，用于为同一个函数声明多个不同的类型签名。它让类型检查器（如 mypy）能够根据传入参数的类型，推断出正确的返回类型。
    关键点：@overload 只在静态类型检查时起作用，运行时不执行这些重载签名，Python 仍然只有一个实际的函数实现。
    ```
    from typing import overload

    @overload
    def create_user(name: str) -> dict: ...

    @overload
    def create_user(name: str, age: int) -> dict: ...

    @overload
    def create_user(name: str, age: int, email: str) -> dict: ...

    def create_user(name: str, age: int | None = None, email: str | None = None) -> dict:
        """创建用户字典"""
        user = {"name": name}
        if age is not None:
            user["age"] = age
        if email is not None:
            user["email"] = email
        return user

    # 类型检查器能识别不同的调用方式
    user1 = create_user("Bob")
    user2 = create_user("Bob", 25)
    user3 = create_user("Bob", 25, "bob@example.com")
    ```

#### [x] **get_origin(), get_args(), clear_overloads()**
- `get_origin(tp)` 返回泛型原始类型（`list[int]` → `list`），`get_args(tp)` 返回类型参数（`list[int]` → `(int,)`）。非泛型返回 `None` 和空元组。用于运行时类型检查和框架开发。`clear_overloads()` 清理 `@overload` 重载签名。
- 解释:
    ```python
    from typing import get_origin, get_args
    print(get_origin(list[int]))  # <class 'list'>
    print(get_args(list[int]))    # (<class 'int'>,)
    ``` 


### **4. 类型检查器专用／运行时辅助／版本兼容**

#### [x] **TYPE_CHECKING**
- 布尔常量，在类型检查器运行时为 `True`，而运行时代码可据此跳过某些导入。语法：`from typing import TYPE_CHECKING`。
- 解释: 

#### [x] **cast()**
- 用于告诉类型检查器将某值视为某类型。语法：`cast(T, expr)`。
    ```
    from typing import cast
    result = cast(TargetType, expression)
    ```
- 解释: 
    - cast() 是 typing 模块提供的一个函数，用于告诉类型检查器将某个表达式的类型视为指定的类型。
    1. 重要：cast() 只影响类型检查器（如 mypy），在运行时不做任何类型转换或验证，它只是一个"标记"。
    语法：

    2. 为什么需要
    有时候你（程序员）比类型检查器更了解某个值的真实类型，但类型检查器无法推断出来。这时就需要用 cast() 来"告诉"类型检查器：相信我，这个值就是这个类型。
    常见场景：
    动态加载的对象
    从外部数据源获取的数据
    复杂的类型推断场景，类型检查器无法正确推断
    3. 例子
        ```python
        from typing import cast

        # 场景：从配置中获取值，你知道它是 int，但类型检查器认为是 Any
        def get_config(key: str) -> Any:
            return {"timeout": 30}[key]

        # 不用 cast：mypy 会认为 timeout 是 Any 类型
        timeout = get_config("timeout")  # type: Any

        # 使用 cast：告诉 mypy 这是 int
        timeout = cast(int, get_config("timeout"))  # type: int
        # 现在可以安全地使用 int 的方法
        seconds = timeout + 10  # mypy 知道这是合法的
        ```
        再比如，处理 json 数据
        ```
        import json
        from typing import cast

        # JSON 解析返回 Any 类型
        data = json.loads('{"name": "Alice", "age": 30}')
        # data 的类型是 Any

        # 你知道结构，可以用 cast
        user_dict = cast(dict[str, str | int], data)
        name = user_dict["name"]  # mypy 知道这是 str | int
        # 这种情况，更好的方式用pydantic吧。或者 pydantic +TypedDict
        ```
    4. 陷阱
    陷阱 1：以为 cast 会做类型转换
    陷阱 2：滥用 cast 掩盖真正的类型错误

        


#### [x] **assert_type()**
- 告诉类型检查器断言值的类型（Python 3.11+）。语法：`assert_type(expr, T)`。
- 解释: 
    ```
    from typing import assert_type

    def get_number() -> int:
        return 42

    # 告诉类型检查器：我认为这个表达式的类型是 int
    result = get_number()
    assert_type(result, int)  # ✓ 类型检查器会验证 result 确实是 int

    # 如果断言错误，类型检查器会报错
    assert_type(result, str)  # ✗ 类型检查器报错：Expected type str, got int
    ```
 - 注意
    这是一个测试工具，不应在生产代码中大量使用
    主要用于编写类型检查器的测试用例

#### [x] **assert_never()**
- 用于穷尽性检查，确认代码路径不可达（Python 3.11+）。语法：`assert_never(x)`。
- 解释: 
    “用来锁门的”，一般加这个是为了面向未来写的代码保证类型安全。

#### [x] **reveal_type()**
- 调试工具，显示类型检查器推断的类型（Python 3.11+）。语法：`reveal_type(expr)`。
- 解释: 是一个专门用于调试的工具函数，能让类型检查器（如 mypy）告诉你：在某个位置，变量的类型被推断为什么。一个调试小工具，可以直接在`Problems`中看到这行代码的输出。
    ```python  
    from typing import reveal_type
    def process_data(data: int | str) -> None:
        # 看看类型检查器认为 data 是什么类型
        reveal_type(data)  # mypy 会输出: Revealed type is "int | str"
        
        if isinstance(data, int):
            # 在这个分支里，类型检查器知道 data 是 int
            reveal_type(data)  # Revealed type is "int"
            print(data * 2)
        else:
            # 在这个分支里，类型检查器知道 data 是 str
            reveal_type(data)  # Revealed type is "str"
            print(data.upper())
    ```

#### [x] **overload()**
- 装饰器，用于声明多个函数签名（静态分析用）。语法：`@overload`。
- 解释: 

#### [x] **get_origin(), get_args()**
- 同上（第 3 节已详细说明）。这两个函数在 `typing` 模块中既是类型元编程工具，也是运行时辅助函数。语法：`get_origin(tp)`，`get_args(tp)`。
- 解释: 见第 3 节。

#### [ ] **get_type_hints()**
- 获取对象的类型提示（重要的运行时函数）。语法：`get_type_hints(obj)`。但是
为了性能和表达力，
Pydantic 在底层做了很多黑科技：
它直接用 Rust 重写了类型解析和验证逻辑，而不是用官方的 get_type_hints()
- 解释: 
    ```python
    from typing import get_type_hints, TypedDict

    # 场景1：运行时验证（类似 pydantic 的实现原理）
    def validate_types(func, *args, **kwargs):
        hints = get_type_hints(func)
        # 获取参数名
        import inspect
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        
        # 验证每个参数的类型
        for param_name, param_value in bound_args.arguments.items():
            expected_type = hints.get(param_name)
            if expected_type and not isinstance(param_value, expected_type):
                raise TypeError(
                    f"参数 {param_name} 应该是 {expected_type}，"
                    f"但得到了 {type(param_value)}"
                )
        
        return func(*args, **kwargs)

    def add(x: int, y: int) -> int:
        return x + y

    validate_types(add, 1, 2)      # ✓ 正常
    # validate_types(add, "1", 2)  # ✗ 抛出 TypeError

    # 场景2：自动生成文档
    def generate_signature_doc(func):
        hints = get_type_hints(func)
        params = []
        for name, type_ in hints.items():
            if name != 'return':
                params.append(f"{name}: {type_.__name__}")
        
        return_type = hints.get('return', 'None')
        return f"{func.__name__}({', '.join(params)}) -> {return_type.__name__}"

    print(generate_signature_doc(add))
    # add(x: int, y: int) -> int

    # 场景3：处理 TypedDict
    class Config(TypedDict):
        host: str
        port: int
        debug: bool

    hints = get_type_hints(Config)
    print(hints)
    # {'host': <class 'str'>, 'port': <class 'int'>, 'debug': <class 'bool'>}
    ```

#### [x] **is_protocol()**
- 检查一个类型是否为 `Protocol`（Python 3.14）。语法：`is_protocol(tp)`。仅在 Python 3.14+ 可用（较新的特性）
- 解释: 
    ```python
    from typing import Protocol, is_protocol, get_type_hints

    # 场景：自动注册 Protocol 的实现
    class PluginRegistry:
        def __init__(self):
            self.protocols = {}
            self.implementations = {}
        
        def register_protocol(self, proto):
            if is_protocol(proto):
                self.protocols[proto.__name__] = proto
            else:
                raise TypeError(f"{proto} 不是一个 Protocol")
        
        def register_implementation(self, proto, impl):
            if is_protocol(proto):
                self.implementations[proto] = impl

    registry = PluginRegistry()

    @runtime_checkable
    class Storage(Protocol):
        def save(self, data: str) -> None: ...

    registry.register_protocol(Storage)  # ✓
    # registry.register_protocol(str)    # ✗ TypeError
    ```

#### [ ] **is_typeddict()**
- 检查一个类型是否为 `TypedDict`（Python 3.14）。语法：`is_typeddict(tp)`。
- 解释: 
    ```python
    from typing import TypedDict, is_typeddict, get_type_hints

    # 场景：自动验证 TypedDict
    def validate_typeddict(td_class, data: dict):
        if not is_typeddict(td_class):
            raise TypeError(f"{td_class} 不是 TypedDict")
        
        hints = get_type_hints(td_class)
        for key, expected_type in hints.items():
            if key not in data:
                raise ValueError(f"缺少必需字段: {key}")
            
            value = data[key]
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"字段 {key} 应该是 {expected_type}，"
                    f"但得到了 {type(value)}"
                )
        
        return data

    class Config(TypedDict):
        host: str
        port: int

    config_data = {"host": "localhost", "port": 8000}
    validate_typeddict(Config, config_data)  # ✓
    ```


#### [ ] **clear_overloads()**
- 清理已声明的 `overload`。语法：`clear_overloads()`。
- 解释: 

#### [ ] **@override**
- （PEP 698）用于标记覆写父类方法的装饰器，帮助类型检查。语法：`@override`。
- 解释: 

#### [ ] **@dataclass_transform**
- （PEP 681）用于自定义装饰器的类型提示。语法：`@dataclass_transform()`。
- 解释: 

#### [x] **deprecated()**
- 标记已弃用的函数或类的装饰器。语法：`deprecated("message")` 或 `@deprecated("reason")`（具体用法依 Python 版本）。
- 解释: 

#### [x] **typing_extensions**
- 为旧版本 Python 提供新特性的向后兼容模块。语法：`from typing_extensions import ...`。
- 解释:
