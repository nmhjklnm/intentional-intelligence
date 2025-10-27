# 可插拔任务队列系统

这是一个**类型安全、可扩展、可插拔**的异步任务队列系统，展示了 Python 现代类型系统的强大能力。

## 🌟 核心特性

### 1. 结构化类型系统（Protocol）

使用 `Protocol` 而不是传统的抽象基类（ABC），体现 Python 从"动态鸭子类型"到"可验证的结构化类型"的进化：

```python
from protocol import TaskQueue

# ✅ 任何实现了 TaskQueue 方法的类都自动满足协议
# ✅ mypy 在编译时验证实现是否正确
# ✅ 无需显式继承，保持 Python 灵活性

def worker(queue: TaskQueue):  # 类型安全！
    task = await queue.get_task("task-1")
```

### 2. 依赖注入 + 抽象接口

业务逻辑只依赖接口，不依赖具体实现：

```python
# worker.py 完全不知道存储方式
async def worker(queue: TaskQueue, ...):
    # 可能是 SQLite，可能是 Redis，也可能是内存
    # 业务代码完全相同！
    tasks = await queue.get_pending_tasks()
```

### 3. 一行代码切换存储

```python
# 开发环境：内存队列（快速测试）
queue = QueueFactory.create("memory")

# 单机生产：SQLite（持久化）
queue = QueueFactory.create("sqlite", db_path="prod.db")

# 分布式：Redis（高性能）
queue = QueueFactory.create("redis", redis_url="redis://prod:6379")
```

### 4. 类型安全的配置

使用 `Literal` 限制字符串取值：

```python
QueueType = Literal["sqlite", "redis", "memory"]

# ✅ mypy 允许
queue = QueueFactory.create("sqlite")

# ❌ mypy 报错：不在 Literal 中
queue = QueueFactory.create("mysql")
```

## 📁 项目结构

```
queue/
├── types.py           # 核心数据类型（dataclass + Enum）
├── protocol.py        # 抽象接口（Protocol）
├── sqlite_queue.py    # SQLite 实现
├── redis_queue.py     # Redis 实现框架
├── memory_queue.py    # 内存实现
├── worker.py          # 业务逻辑（与存储无关）
├── factory.py         # 工厂模式（类型安全）
├── main.py            # 主程序入口
└── README.md          # 本文档
```

## 🚀 快速开始

### 运行演示

```bash
# 从项目根目录运行（推荐）
cd /path/to/类型系统

# 1. 运行测试
python -m examples.queue.test_queue

# 2. 内存队列演示
python -m examples.queue.run memory

# 3. SQLite 队列演示  
python -m examples.queue.run sqlite

# 4. 切换演示
python -m examples.queue.run switch

# 或者使用便捷脚本（在 queue 目录下）
cd examples/queue
python run.py memory
```

### 基本使用

```python
import asyncio
from models import Task, TaskStatus
from factory import QueueFactory
from worker import worker

async def main():
    # 1. 创建队列
    queue = QueueFactory.create("sqlite")
    
    # 2. 添加任务
    await queue.add_task(Task(
        task_id="task-1",
        task_type="download",
        params={"url": "example.com", "duration": 2},
        status=TaskStatus.PENDING
    ))
    
    # 3. 启动 worker
    running_tasks = set()
    await worker(1, queue, running_tasks)

asyncio.run(main())
```

## 🎯 设计理念

### Python 类型系统的进化

| 传统方式 | 现代方式 | 优势 |
|---------|---------|------|
| 鸭子类型，无类型检查 | Protocol + 类型注解 | 编译时发现错误 |
| 字符串常量 | Literal + Enum | 限制取值范围 |
| 字典传参 | dataclass | IDE 自动补全 |
| 抽象基类（ABC） | Protocol | 结构化类型，更灵活 |
| 注释说明类型 | 类型注解 | mypy 自动验证 |

### 核心原则

1. **抽象（Protocol）** - 定义"做什么"
2. **实现（Concrete Classes）** - 定义"怎么做"
3. **依赖注入** - 业务逻辑依赖抽象
4. **类型安全** - mypy 编译时验证
5. **易于扩展** - 新增实现不影响业务

## 📊 架构对比

### 传统方式（紧耦合）

```python
# ❌ 业务逻辑直接依赖具体实现
def worker(db_path: str):
    conn = sqlite3.connect(db_path)
    # 硬编码 SQL 查询...
    # 切换到 Redis？重写整个函数！
```

### 现代方式（松耦合）

```python
# ✅ 业务逻辑依赖抽象接口
def worker(queue: TaskQueue):  # 任何实现都可以
    tasks = await queue.get_pending_tasks()
    # 业务代码完全相同，切换存储零成本！
```

## 🔧 扩展到新的存储

添加新的存储方式（如 PostgreSQL）只需 3 步：

```python
# 1. 创建实现类（自动满足 Protocol）
class PostgresTaskQueue:
    async def add_task(self, task: Task) -> None:
        # 实现...
    
    async def get_pending_tasks(self, limit: int = 10) -> list[Task]:
        # 实现...
    
    # ... 其他方法

# 2. 添加到工厂
def create(queue_type: Literal["sqlite", "redis", "memory", "postgres"], **kwargs):
    if queue_type == "postgres":
        return PostgresTaskQueue(**kwargs)
    # ...

# 3. 使用（业务代码不变）
queue = QueueFactory.create("postgres", connection_string="...")
await worker(1, queue, running_tasks)  # 完全相同！
```

## 🎓 学习价值

这个项目展示了：

1. **Protocol 的实际应用**：结构化类型系统
2. **依赖注入模式**：解耦业务与存储
3. **工厂模式**：配置驱动 + 类型安全
4. **类型注解的价值**：编译时错误检测
5. **现代 Python 最佳实践**：dataclass、Enum、Literal

## 📈 扩展方向

- [ ] 添加优先级队列（使用 Sorted Set）
- [ ] 添加延迟队列（定时任务）
- [ ] 添加任务依赖（DAG）
- [ ] 添加分布式锁（避免重复执行）
- [ ] 添加监控和统计（Prometheus）
- [ ] 添加 Web 界面（查看任务状态）

## 💡 关键要点

> **核心思想**：写一个好的队列系统，可以用很久，并且可以轻松切换不同的持久化方案。

这正是软件工程的核心价值：
- **抽象**：隔离变化
- **类型**：保证正确
- **扩展**：应对未来

---

**Happy Coding! 🎉**

