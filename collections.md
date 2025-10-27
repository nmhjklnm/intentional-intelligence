# collections.abc



### **1. 可调用类型**

#### [ ] **Callable**
- 表示可被调用的对象（函数／方法／可调用实例）。语法：`Callable[[参数类型...], 返回类型]`。Python 3.9+ 推荐从 `collections.abc` 导入（旧版本从 `typing` 导入）
- example:

---

### **2. 容器基础协议**

#### [ ] **Container**
- 表示支持 `in` 操作的容器（实现 `__contains__` 方法）。
- example:

#### [ ] **Sized**
- 表示支持 `len()` 的对象（实现 `__len__` 方法）。
- example:

#### [ ] **Hashable**
- 表示可哈希的对象（可用作字典键或集合元素，实现 `__hash__` 方法）。
- example:

#### [ ] **Collection**
- 组合了 Container, Sized, Iterable 的抽象基类。表示"具有大小、可迭代、支持成员检查"的集合类型。
- example:

---

### **3. 可迭代／迭代器**

#### [ ] **Iterable**
- 表示可迭代对象（实现 `__iter__` 方法，可用于 for 循环）。语法：`Iterable[元素类型]`
- example:

#### [ ] **Iterator**
- 表示迭代器（实现 `__iter__` 和 `__next__` 方法）。Iterator 是 Iterable 的子类型。语法：`Iterator[元素类型]`
- example:

#### [ ] **Reversible**
- 表示可反向迭代的对象（实现 `__reversed__` 方法）。
- example:

#### [ ] **Generator**
- 生成器类型，是 Iterator 的子类型。语法：`Generator[YieldType, SendType, ReturnType]`
- example:

---

### **4. 序列类型**

#### [ ] **Sequence**
- 表示不可变序列（如 tuple, str, range）。支持索引访问、切片、长度查询等操作。语法：`Sequence[元素类型]`
- example:

#### [ ] **MutableSequence**
- 表示可变序列（如 list, bytearray）。在 Sequence 基础上增加了修改操作（如 append, insert, pop 等）。语法：`MutableSequence[元素类型]`
- example:

#### [ ] **ByteString**
- 表示字节序列（bytes, bytearray, memoryview）。注意：Python 3.12+ 已废弃，推荐直接使用具体类型。
- example:

---

### **5. 集合类型**

#### [ ] **Set**
- 表示不可变集合的抽象基类（如 frozenset）。语法：`Set[元素类型]`。注意：与内置 `set` 类型名称冲突，导入时需注意。
- example:

#### [ ] **MutableSet**
- 表示可变集合（如内置 set）。语法：`MutableSet[元素类型]`
- example:

---

### **6. 映射类型**

#### [ ] **Mapping**
- 表示不可变映射（只读字典）的抽象基类。支持键查询、遍历等操作，但不支持修改。语法：`Mapping[KeyType, ValueType]`
- example:

#### [ ] **MutableMapping**
- 表示可变映射（如内置 dict）。在 Mapping 基础上增加了修改操作（如赋值、删除等）。语法：`MutableMapping[KeyType, ValueType]`
- example:

#### [ ] **MappingView**
- 字典视图的基类（dict.keys(), dict.values(), dict.items() 的返回类型）。
- example:

#### [ ] **KeysView**
- 字典键视图类型（dict.keys() 的返回类型）。
- example:

#### [ ] **ValuesView**
- 字典值视图类型（dict.values() 的返回类型）。
- example:

#### [ ] **ItemsView**
- 字典项视图类型（dict.items() 的返回类型）。
- example:

---

### **7. 异步相关**

#### [ ] **Awaitable**
- 表示可等待对象（可用于 await 表达式）。包括协程、实现了 `__await__` 方法的对象。语法：`Awaitable[返回类型]`
- example:

#### [ ] **Coroutine**
- 表示协程类型（async def 定义的函数返回值）。语法：`Coroutine[YieldType, SendType, ReturnType]`
- example:

#### [ ] **AsyncIterable**
- 表示异步可迭代对象（实现 `__aiter__` 方法）。可用于 `async for` 循环。语法：`AsyncIterable[元素类型]`
- example:

#### [ ] **AsyncIterator**
- 表示异步迭代器（实现 `__aiter__` 和 `__anext__` 方法）。语法：`AsyncIterator[元素类型]`
- example:

#### [ ] **AsyncGenerator**
- 异步生成器类型（async def + yield）。语法：`AsyncGenerator[YieldType, SendType]`
- example:

---

### **8. 上下文管理器**

#### [ ] **ContextManager**
- 上下文管理器类型（实现 `__enter__` 和 `__exit__` 方法）。可用于 `with` 语句。语法：`ContextManager[返回类型]`。Python 3.9+ 推荐从 `collections.abc` 导入（旧版本从 `typing` 导入）
- example:

#### [ ] **AsyncContextManager**
- 异步上下文管理器（实现 `__aenter__` 和 `__aexit__` 方法）。可用于 `async with` 语句。语法：`AsyncContextManager[返回类型]`。Python 3.9+ 推荐从 `collections.abc` 导入（旧版本从 `typing` 导入）
- example:

---

### **9. 其他抽象基类**

#### [ ] **Buffer**
- 表示支持缓冲区协议的对象（Python 3.12+）。如 bytes, bytearray, memoryview 等。
- example:
