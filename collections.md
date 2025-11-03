# collections.abc



### **1. 可调用类型**

#### [ ] **Callable**
- 表示可被调用的对象（函数／方法／可调用实例）。语法：`Callable[[参数类型...], 返回类型]`。Python 3.9+ 推荐从 `collections.abc` 导入（旧版本从 `typing` 导入）。
- 解释:

---

### **2. 容器基础协议**

#### [ ] **Container**
- 表示支持 `in` 操作的容器（实现 `__contains__` 方法）。语法：直接使用 `Container`。
- 解释:

#### [ ] **Sized**
- 表示支持 `len()` 的对象（实现 `__len__` 方法）。语法：直接使用 `Sized`。
- 解释:

#### [ ] **Hashable**
- 表示可哈希的对象（可用作字典键或集合元素，实现 `__hash__` 方法）。语法：直接使用 `Hashable`。
- 解释:

#### [ ] **Collection**
- 组合了 `Container`、`Sized`、`Iterable` 的抽象基类，表示具有大小、可迭代、支持成员检查的集合类型。语法：`Collection[T]`。
- 解释:

---

### **3. 可迭代／迭代器**

#### [ ] **Iterable**
- 表示可迭代对象（实现 `__iter__` 方法，可用于 `for` 循环）。语法：`Iterable[元素类型]`。
- 解释:

#### [ ] **Iterator**
- 表示迭代器（实现 `__iter__` 和 `__next__` 方法），且是 `Iterable` 的子类型。语法：`Iterator[元素类型]`。
- 解释:

#### [ ] **Reversible**
- 表示可反向迭代的对象（实现 `__reversed__` 方法）。语法：`Reversible[T]`。
- 解释:

#### [ ] **Generator**
- 生成器类型，是 `Iterator` 的子类型。语法：`Generator[YieldType, SendType, ReturnType]`。
- 解释:

---

### **4. 序列类型**

#### [ ] **Sequence**
- 表示不可变序列（如 `tuple`、`str`、`range`）。支持索引访问、切片、长度查询等操作。语法：`Sequence[元素类型]`。
- 解释:

#### [ ] **MutableSequence**
- 表示可变序列（如 `list`、`bytearray`），在 `Sequence` 基础上增加了修改操作（如 `append`、`insert`、`pop` 等）。语法：`MutableSequence[元素类型]`。
- 解释:

#### [ ] **ByteString**
- 表示字节序列（`bytes`、`bytearray`、`memoryview`）。注意：Python 3.12+ 已废弃，推荐直接使用具体类型。语法：直接使用 `ByteString`。
- 解释:

---

### **5. 集合类型**

#### [ ] **Set**
- 表示不可变集合的抽象基类（如 `frozenset`）。语法：`Set[元素类型]`。注意：与内置 `set` 类型名称冲突，导入时需注意。
- 解释:

#### [ ] **MutableSet**
- 表示可变集合（如内置 `set`）。语法：`MutableSet[元素类型]`。
- 解释:

---

### **6. 映射类型**

#### [ ] **Mapping**
- 表示不可变映射（只读字典）的抽象基类，支持键查询、遍历等操作，但不支持修改。语法：`Mapping[KeyType, ValueType]`。
- 解释:

#### [ ] **MutableMapping**
- 表示可变映射（如内置 `dict`），在 `Mapping` 基础上增加了修改操作（如赋值、删除等）。语法：`MutableMapping[KeyType, ValueType]`。
- 解释:

#### [ ] **MappingView**
- 字典视图的基类（`dict.keys()`、`dict.values()`、`dict.items()` 的返回类型）。语法：直接使用 `MappingView`。
- 解释:

#### [ ] **KeysView**
- 字典键视图类型（`dict.keys()` 的返回类型）。语法：`KeysView[KeyType]`。
- 解释:

#### [ ] **ValuesView**
- 字典值视图类型（`dict.values()` 的返回类型）。语法：`ValuesView[ValueType]`。
- 解释:

#### [ ] **ItemsView**
- 字典项视图类型（`dict.items()` 的返回类型）。语法：`ItemsView[KeyType, ValueType]`。
- 解释:

---

### **7. 异步相关**

#### [ ] **Awaitable**
- 表示可等待对象（可用于 `await` 表达式），包括协程或实现 `__await__` 的对象。语法：`Awaitable[返回类型]`。
- 解释:

#### [ ] **Coroutine**
- 表示协程类型（`async def` 定义的函数返回值）。语法：`Coroutine[YieldType, SendType, ReturnType]`。
- 解释:

#### [ ] **AsyncIterable**
- 表示异步可迭代对象（实现 `__aiter__` 方法），可用于 `async for` 循环。语法：`AsyncIterable[元素类型]`。
- 解释:

#### [ ] **AsyncIterator**
- 表示异步迭代器（实现 `__aiter__` 和 `__anext__` 方法）。语法：`AsyncIterator[元素类型]`。
- 解释:

#### [ ] **AsyncGenerator**
- 异步生成器类型（`async def` + `yield`）。语法：`AsyncGenerator[YieldType, SendType]`。
- 解释:

---

### **8. 上下文管理器**

#### [ ] **ContextManager**
- 上下文管理器类型（实现 `__enter__` 和 `__exit__` 方法），可用于 `with` 语句。语法：`ContextManager[返回类型]`。Python 3.9+ 推荐从 `collections.abc` 导入（旧版本从 `typing` 导入）。
- 解释:

#### [ ] **AsyncContextManager**
- 异步上下文管理器（实现 `__aenter__` 和 `__aexit__` 方法），可用于 `async with` 语句。语法：`AsyncContextManager[返回类型]`。Python 3.9+ 推荐从 `collections.abc` 导入（旧版本从 `typing` 导入）。
- 解释:

---

### **9. 其他抽象基类**

#### [ ] **Buffer**
- 表示支持缓冲区协议的对象（Python 3.12+），如 `bytes`、`bytearray`、`memoryview` 等。语法：直接使用 `Buffer`。
- 解释:
