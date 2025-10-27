# Python 设计模式

> **说明**：本文档整理常用的设计模式及其在 Python 中的实现。设计模式是软件开发中反复出现问题的通用解决方案。

---

## **设计模式分类**

设计模式通常分为三大类：

1. **创建型模式（Creational）**：关注对象的创建机制
2. **结构型模式（Structural）**：关注类和对象的组合
3. **行为型模式（Behavioral）**：关注对象之间的通信和职责分配

---

## **1. 创建型模式**

### [x] **工厂模式（Factory Pattern）**

**概念**：用一个工厂类来创建对象，调用者不需要知道具体类名。根据配置或参数动态选择实现。

**为什么需要**：
- 解耦对象的创建和使用
- 根据配置动态选择实现
- 便于扩展新的实现类型

**核心要素**：
- 统一的接口/协议（返回类型）
- 工厂方法（接收参数，返回实例）
- 多个具体实现类

**应用场景**：
- 数据库连接：根据配置选择 MySQL/PostgreSQL/SQLite
- 队列系统：根据环境选择内存/Redis/SQLite 队列
- 日志系统：根据级别选择不同的日志处理器
- 支付系统：根据用户选择不同的支付方式

**Python 特性结合**：
- 使用 `Literal` 类型限制参数值
- 使用 `Protocol` 定义返回类型
- 使用 `TypeAlias` 提供类型别名

**example**：
```python
from typing import Literal, Protocol

# 1. 定义协议（统一接口）
class TaskQueue(Protocol):
    async def add_task(self, task: Task) -> None: ...
    async def get_pending_tasks(self) -> list[Task]: ...

# 2. 类型别名：限制队列类型
QueueType = Literal["sqlite", "redis", "memory"]

# 3. 工厂类
class QueueFactory:
    @staticmethod
    def create(queue_type: QueueType, **kwargs) -> TaskQueue:
        """根据类型创建队列"""
        if queue_type == "sqlite":
            return SQLiteTaskQueue(**kwargs)
        elif queue_type == "redis":
            return RedisTaskQueue(**kwargs)
        elif queue_type == "memory":
            return InMemoryTaskQueue()
        else:
            raise ValueError(f"Unsupported: {queue_type}")

# 4. 使用
# 开发环境
dev_queue = QueueFactory.create("memory")
# 生产环境
prod_queue = QueueFactory.create("sqlite", db_path="prod.db")
```

---

### [x] **单例模式（Singleton Pattern）**

**概念**：确保一个类只有一个实例，并提供全局访问点。

**为什么需要**：
- 全局资源管理：避免重复创建
- 状态共享：多处访问同一实例
- 节省资源：如数据库连接池、配置管理器

**核心要素**：
- 私有化实例变量（类变量存储唯一实例）
- 控制实例创建（重写 `__new__` 或使用装饰器）
- 全局访问点

**应用场景**：
- 数据库连接池
- 配置管理器（只加载一次配置文件）
- 日志记录器
- 线程池、进程池

**实现方式**：
1. 重写 `__new__` 方法
2. 使用装饰器
3. 使用元类

**example**：
```python
# 方式 1：重写 __new__
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self.connection = "db_connection"
        self._initialized = True

# 方式 2：装饰器实现
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Config:
    def __init__(self):
        self.settings = {"debug": True}

# 使用
db1 = DatabaseConnection()
db2 = DatabaseConnection()
print(db1 is db2)  # True
```

---

### [x] **建造者模式（Builder Pattern）**

**概念**：将复杂对象的构建过程分步骤进行，使用者可以按需构建。通过链式调用逐步设置参数，最后调用 `build()` 生成对象。

**为什么需要**：
- 构造函数参数太多，不易理解
- 对象构建过程复杂，需要多个步骤
- 同样的构建过程可以创建不同的表示

**核心要素**：
- 建造者类（Builder）：提供构建方法
- 链式调用（返回 self）
- 最终构建方法（build()）

**应用场景**：
- SQL 查询构建器（逐步添加 SELECT、WHERE、ORDER BY）
- HTTP 请求构建器（设置 URL、headers、body）
- 配置对象构建（逐步设置各种选项）
- UI 组件构建（设置样式、属性、事件）

**Python 特性结合**：
- 链式调用（方法返回 `self`）
- 类型提示（返回 `"QueryBuilder"` 确保链式调用类型正确）
- 最终验证（build 方法中检查必需参数）

**example**：
```python
class QueryBuilder:
    def __init__(self):
        self._table: Optional[str] = None
        self._fields: list[str] = []
        self._where: Optional[str] = None
        self._limit: Optional[int] = None
    
    def table(self, name: str) -> "QueryBuilder":
        """设置表名（返回 self 支持链式调用）"""
        self._table = name
        return self
    
    def select(self, *fields: str) -> "QueryBuilder":
        self._fields.extend(fields)
        return self
    
    def where(self, condition: str) -> "QueryBuilder":
        self._where = condition
        return self
    
    def limit(self, count: int) -> "QueryBuilder":
        self._limit = count
        return self
    
    def build(self) -> str:
        """构建 SQL 查询"""
        if not self._table:
            raise ValueError("必须指定表名")
        
        sql = f"SELECT {', '.join(self._fields or ['*'])} FROM {self._table}"
        if self._where:
            sql += f" WHERE {self._where}"
        if self._limit:
            sql += f" LIMIT {self._limit}"
        return sql

# 使用：链式调用
query = (
    QueryBuilder()
    .table("users")
    .select("id", "name", "email")
    .where("age > 18")
    .limit(10)
    .build()
)
print(query)  # SELECT id, name, email FROM users WHERE age > 18 LIMIT 10
```

---

## **2. 结构型模式**

### [x] **Mixin 模式**

**概念**：通过多重继承，将特定功能"混入"到类中，实现代码复用。Mixin 类通常不单独实例化，只提供某些方法或属性。

**为什么需要**：
- 多个类需要相同的功能，但不适合用继承
- 避免重复代码
- 功能模块化，可灵活组合

**核心要素**：
- Mixin 类：提供特定功能（如时间戳、序列化）
- 主类：通过多重继承混入功能
- 命名约定：Mixin 类名通常以 Mixin 结尾

**应用场景**：
- 添加时间戳（CreatedAt、UpdatedAt）
- 添加序列化功能（to_dict、from_dict）
- 添加日志功能
- 添加缓存功能

**Python 特性结合**：
- 多重继承（`class Model(TimestampMixin, SerializeMixin)`）
- 方法解析顺序（MRO）
- 类型提示（Protocol 确保 Mixin 正确使用）

**example**：
```python
from datetime import datetime

class TimestampMixin:
    """时间戳 Mixin"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def touch(self):
        """更新修改时间"""
        self.updated_at = datetime.now()

class SerializeMixin:
    """序列化 Mixin"""
    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() 
                if not k.startswith('_')}

# 使用 Mixin
class User(TimestampMixin, SerializeMixin):
    def __init__(self, name: str, email: str):
        super().__init__()  # 调用 Mixin 的 __init__
        self.name = name
        self.email = email

user = User("Alice", "alice@example.com")
print(user.created_at)  # 自动有时间戳
print(user.to_dict())   # 自动有序列化
```

---

### [x] **协议模式（Protocol Pattern）**

**概念**：定义一组方法签名（接口），任何实现了这些方法的类都满足该协议。基于"结构化类型"（鸭子类型），不需要显式继承。

**为什么需要**：
- Python 的"鸭子类型"：如果它走路像鸭子、叫声像鸭子，那它就是鸭子
- 不需要继承，更灵活
- 静态类型检查：mypy 可以验证是否符合协议
- 可以给第三方类"追加"协议支持

**核心要素**：
- 使用 `typing.Protocol` 定义协议
- 定义方法签名（方法体用 `...`）
- 实现类无需继承协议类
- mypy 自动检查实现是否符合

**应用场景**：
- 定义接口规范（如任务队列、数据库连接）
- 替代抽象基类（ABC）
- 类型约束（函数参数必须实现某协议）
- 第三方库集成

**与 ABC 的区别**：
- Protocol：结构化类型，基于方法签名
- ABC：名义类型，必须显式继承

**example**：
```python
from typing import Protocol, Optional

# 1. 定义协议
class TaskQueue(Protocol):
    """任务队列协议（接口规范）"""
    async def add_task(self, task: Task) -> None: ...
    async def get_task(self, task_id: str) -> Optional[Task]: ...

# 2. 实现类（无需继承）
class MemoryQueue:
    async def add_task(self, task: Task) -> None:
        # 实现...
        pass
    
    async def get_task(self, task_id: str) -> Optional[Task]:
        # 实现...
        return None

# 3. 类型检查
async def process_queue(queue: TaskQueue):
    """接受任何实现了 TaskQueue 协议的对象"""
    await queue.add_task(task)  # ✅ mypy 知道有 add_task 方法
    
# MemoryQueue 无需继承 TaskQueue，mypy 也能识别
memory_queue = MemoryQueue()
await process_queue(memory_queue)  # ✅ 类型检查通过
```

---

### [x] **适配器模式（Adapter Pattern）**

**概念**：将一个类的接口转换成客户期望的另一个接口。让原本不兼容的类可以一起工作。

**为什么需要**：
- 集成第三方库，但接口不匹配
- 复用旧代码，但接口已过时
- 统一不同来源的数据格式

**核心要素**：
- 目标接口（期望的接口）
- 被适配者（需要适配的类）
- 适配器（实现目标接口，内部调用被适配者）

**应用场景**：
- 统一不同日志库的接口
- 统一不同数据库的接口
- 统一不同支付接口
- 数据格式转换（JSON ↔ XML）

**实现方式**：
1. 对象适配器（组合）：推荐
2. 类适配器（多重继承）

**example**：
```python
from typing import Protocol

# 1. 目标接口：我们期望的统一接口
class Logger(Protocol):
    def log(self, level: str, message: str) -> None: ...

# 2. 被适配者 A（接口不同）
class ThirdPartyLoggerA:
    def write_log(self, msg: str, severity: int) -> None:
        print(f"[LoggerA] Severity {severity}: {msg}")

# 3. 适配器 A：将 ThirdPartyLoggerA 适配为 Logger
class LoggerAdapterA:
    def __init__(self, logger: ThirdPartyLoggerA):
        self.logger = logger
    
    def log(self, level: str, message: str) -> None:
        # 转换：level 字符串 -> severity 数字
        severity_map = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
        severity = severity_map.get(level.upper(), 1)
        self.logger.write_log(message, severity)

# 4. 使用统一接口
def use_logger(logger: Logger):
    logger.log("INFO", "应用启动")
    logger.log("ERROR", "发生错误")

# 适配第三方库
adapter = LoggerAdapterA(ThirdPartyLoggerA())
use_logger(adapter)  # ✅ 统一接口
```

---

## **3. 行为型模式**

### [x] **策略模式（Strategy Pattern）**

**概念**：定义一系列算法，把它们封装起来，使它们可以互相替换。算法的变化独立于使用算法的客户。

**为什么需要**：
- 避免大量 if-elif-else
- 算法可以独立变化
- 便于添加新算法
- 运行时动态切换算法

**核心要素**：
- 策略协议（定义算法接口）
- 具体策略（实现不同算法）
- 上下文类（使用策略）

**应用场景**：
- 支付方式：支付宝、微信、银行卡
- 排序算法：快速排序、归并排序、冒泡排序
- 压缩算法：ZIP、RAR、GZIP
- 数据处理：转大写、转小写、反转
- 任务重试策略：固定间隔、指数退避、随机延迟

**Python 特性结合**：
- 使用 Protocol 定义策略接口
- 策略可以是类、函数、lambda
- 运行时切换策略

**example**：
```python
from typing import Protocol

# 1. 策略协议
class DataProcessor(Protocol):
    def process(self, data: str) -> str: ...

# 2. 具体策略
class UpperCaseProcessor:
    def process(self, data: str) -> str:
        return data.upper()

class LowerCaseProcessor:
    def process(self, data: str) -> str:
        return data.lower()

class ReverseProcessor:
    def process(self, data: str) -> str:
        return data[::-1]

# 3. 上下文类：使用策略
class TextEditor:
    def __init__(self, processor: DataProcessor):
        self.processor = processor
    
    def set_processor(self, processor: DataProcessor):
        """运行时切换策略"""
        self.processor = processor
    
    def transform(self, text: str) -> str:
        return self.processor.process(text)

# 使用
text = "Hello World"
editor = TextEditor(UpperCaseProcessor())
print(editor.transform(text))  # HELLO WORLD

editor.set_processor(LowerCaseProcessor())
print(editor.transform(text))  # hello world
```

---

### [x] **观察者模式（Observer Pattern）**

**概念**：定义对象间的一对多依赖，当一个对象状态改变时，所有依赖它的对象都会收到通知并自动更新。

**为什么需要**：
- 解耦：被观察者不需要知道观察者的细节
- 事件驱动：状态改变自动通知
- 动态订阅：可以随时添加/移除观察者
- 一对多关系

**核心要素**：
- 被观察者（Subject）：维护观察者列表，状态改变时通知
- 观察者（Observer）：接收通知并做出反应
- 订阅/取消订阅机制

**应用场景**：
- 任务状态变化监听（完成时发邮件、记日志）
- UI 事件系统（按钮点击、数据更新）
- 消息队列订阅
- 文件系统监听

**Python 特性结合**：
- 使用 Protocol 定义观察者接口
- 使用 `@property.setter` 触发通知
- 可以用装饰器简化订阅

**example**：
```python
from typing import Protocol
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"

# 1. 观察者协议
class TaskObserver(Protocol):
    def on_status_change(
        self, task_id: str, 
        old_status: TaskStatus, 
        new_status: TaskStatus
    ) -> None: ...

# 2. 被观察者
class Task:
    def __init__(self, task_id: str):
        self.task_id = task_id
        self._status = TaskStatus.PENDING
        self._observers: list[TaskObserver] = []
    
    def attach(self, observer: TaskObserver):
        """添加观察者"""
        self._observers.append(observer)
    
    def notify(self, old_status: TaskStatus, new_status: TaskStatus):
        """通知所有观察者"""
        for observer in self._observers:
            observer.on_status_change(self.task_id, old_status, new_status)
    
    @property
    def status(self) -> TaskStatus:
        return self._status
    
    @status.setter
    def status(self, new_status: TaskStatus):
        """状态改变时自动通知"""
        if new_status != self._status:
            old_status = self._status
            self._status = new_status
            self.notify(old_status, new_status)

# 3. 具体观察者
class LoggerObserver:
    def on_status_change(self, task_id: str, old: TaskStatus, new: TaskStatus):
        print(f"[日志] {task_id}: {old.value} -> {new.value}")

class EmailObserver:
    def on_status_change(self, task_id: str, old: TaskStatus, new: TaskStatus):
        if new == TaskStatus.COMPLETED:
            print(f"[邮件] 任务 {task_id} 已完成")

# 使用
task = Task("task-001")
task.attach(LoggerObserver())
task.attach(EmailObserver())

task.status = TaskStatus.RUNNING   # 自动通知
task.status = TaskStatus.COMPLETED  # 自动通知
```

---

### [x] **装饰器模式（Decorator Pattern）**

**概念**：动态地给对象添加新功能，而不改变其结构。通过包装的方式扩展功能，符合"开放-封闭原则"。

**为什么需要**：
- 遵循开放-封闭原则：对扩展开放，对修改封闭
- 比继承更灵活（可以动态添加/移除功能）
- 可以组合多个装饰器
- 不修改原有代码

**核心要素**：
- 原始对象
- 装饰器函数/类（接收对象，返回增强的对象）
- 可叠加使用

**应用场景**：
- 函数计时、日志记录
- 权限检查、登录验证
- 缓存、重试
- 性能监控、错误处理

**Python 特性结合**：
- 函数装饰器（`@decorator`）
- 类装饰器
- `functools.wraps` 保留元信息
- 可叠加装饰器

**Python 特有优势**：
- 原生支持装饰器语法
- 装饰器可以是函数、类、方法

**example**：
```python
from functools import wraps
import time

# 1. 函数装饰器
def timer(func):
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 耗时: {end - start:.3f}秒")
        return result
    return wrapper

def logger(func):
    """日志装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}，参数: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 返回: {result}")
        return result
    return wrapper

# 2. 叠加使用（从下往上应用）
@timer
@logger
def calculate(x: int, y: int) -> int:
    time.sleep(1)
    return x + y

# 3. 类装饰器
class RetryDecorator:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(self.max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"第 {attempt + 1} 次尝试失败: {e}")
                    if attempt == self.max_retries - 1:
                        raise
        return wrapper

@RetryDecorator(max_retries=3)
def unstable_function():
    # 不稳定的函数
    pass
```

---

## **4. 设计模式总结对比**

| 模式 | 类别 | 核心目的 | 主要优势 | 典型场景 |
|------|------|----------|----------|----------|
| **工厂模式** | 创建型 | 解耦对象创建 | 配置驱动、易扩展 | 多种数据库/队列选择 |
| **单例模式** | 创建型 | 全局唯一实例 | 节省资源、状态共享 | 配置管理器、连接池 |
| **建造者模式** | 创建型 | 分步构建对象 | 链式调用、清晰易读 | SQL 查询、HTTP 请求 |
| **Mixin** | 结构型 | 功能混入 | 代码复用、灵活组合 | 时间戳、序列化 |
| **协议模式** | 结构型 | 定义接口规范 | 鸭子类型、类型检查 | 任务队列、数据处理 |
| **适配器模式** | 结构型 | 接口转换 | 统一接口、兼容旧代码 | 第三方库集成 |
| **策略模式** | 行为型 | 算法可替换 | 避免 if-else、易扩展 | 支付方式、排序算法 |
| **观察者模式** | 行为型 | 状态变化通知 | 解耦、事件驱动 | 任务监听、UI 事件 |
| **装饰器模式** | 行为型 | 动态添加功能 | 不修改原代码、可叠加 | 日志、计时、缓存 |

---

## **5. 在实际项目中的应用**

### **queue 项目中已使用的模式**

#### ✅ **工厂模式** - `QueueFactory`
```python
# factory.py
queue = QueueFactory.create("sqlite", db_path="prod.db")
```

#### ✅ **协议模式** - `TaskQueue Protocol`
```python
# protocol.py
class TaskQueue(Protocol):
    async def add_task(self, task: Task) -> None: ...
```

#### ✅ **Mixin 模式** - `TimestampMixin`
```python
# models.py
class Task(TimestampMixin):
    # 自动获得 created_at、updated_at
    pass
```

### **可以添加的模式**

#### 建议 1：**观察者模式** - 任务状态监听
```python
# 监听任务完成，发送通知
class TaskCompletionObserver:
    async def on_task_completed(self, task_id: str, result: str):
        # 发送邮件、webhook 等
        pass
```

#### 建议 2：**策略模式** - 任务重试策略
```python
# 不同的重试策略
class RetryStrategy(Protocol):
    def get_delay(self, attempt: int) -> float: ...

class FixedRetryStrategy:
    def get_delay(self, attempt: int) -> float:
        return 5.0  # 固定 5 秒

class ExponentialRetryStrategy:
    def get_delay(self, attempt: int) -> float:
        return 2 ** attempt  # 指数退避
```

#### 建议 3：**装饰器模式** - 任务计时
```python
@timer
@retry(max_attempts=3)
async def process_task(task: Task) -> str:
    # 自动计时、自动重试
    pass
```

---

## **6. 设计模式的选择原则**

### **何时使用？**

1. **工厂模式**：当你需要根据配置/参数创建不同类型的对象
2. **单例模式**：当你需要全局唯一的资源（谨慎使用，可能导致测试困难）
3. **建造者模式**：当构造函数参数超过 5 个，或构建过程复杂
4. **Mixin**：当多个类需要相同的辅助功能（时间戳、序列化等）
5. **协议模式**：当你需要定义接口，但不想强制继承（推荐！）
6. **适配器模式**：当你需要集成接口不兼容的第三方库
7. **策略模式**：当你有多个算法/实现，且需要运行时切换
8. **观察者模式**：当一个对象状态改变需要通知多个其他对象
9. **装饰器模式**：当你需要动态添加功能（日志、缓存、权限检查等）

### **不要过度设计**

- **YAGNI 原则**：You Aren't Gonna Need It（你不会需要它）
- **先简单实现**，有需求再重构
- **设计模式是工具**，不是目的
- **代码可读性优先**

---

## **7. Python 设计模式的特点**

### **Python 的优势**

1. **鸭子类型**：Protocol 让接口更灵活
2. **一等函数**：策略可以是函数，不一定要类
3. **装饰器语法**：原生支持装饰器模式
4. **多重继承**：Mixin 模式更自然
5. **动态类型**：工厂模式更简洁

### **与静态语言的区别**

| 特性 | Python | Java/C++ |
|------|--------|----------|
| 接口定义 | Protocol（结构化类型） | Interface/Abstract Class（名义类型） |
| 装饰器 | 语法糖 `@decorator` | 需要手动实现包装类 |
| 单例 | 装饰器/元类 | 私有构造函数 + 静态方法 |
| 策略 | 可以用函数 | 通常需要类 |

---

## **8. 推荐阅读**

- **《设计模式：可复用面向对象软件的基础》**（GoF，四人帮）
- **《Head First 设计模式》**（图解版，易懂）
- **Python 官方文档**：typing 模块、collections.abc 模块
- **pydantic 源码**：大量使用了工厂、协议、Mixin 模式

---

## **9. 快速参考**

### **创建对象时**
- 需要根据配置选择实现 → **工厂模式**
- 需要全局唯一实例 → **单例模式**
- 参数太多、构建复杂 → **建造者模式**

### **组合类时**
- 需要混入辅助功能 → **Mixin**
- 需要定义接口规范 → **协议模式**
- 需要统一不同接口 → **适配器模式**

### **处理行为时**
- 需要切换算法 → **策略模式**
- 需要状态通知 → **观察者模式**
- 需要动态添加功能 → **装饰器模式**

