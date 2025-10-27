# 项目总览

## 📦 完整文件列表

```
queue/
├── models.py              # 核心数据模型（Task, TaskStatus）
├── protocol.py            # 抽象接口（TaskQueue Protocol）
├── sqlite_queue.py        # SQLite 实现
├── redis_queue.py         # Redis 实现框架
├── memory_queue.py        # 内存实现
├── worker.py              # 业务逻辑（任务处理）
├── factory.py             # 工厂模式（队列创建）
├── main.py                # 主程序（演示示例）
├── run.py                 # 运行脚本
├── test_queue.py          # 功能测试
├── __init__.py            # 包初始化
├── README.md              # 使用文档
├── TYPE_SYSTEM.md         # 类型系统特性详解
├── PROJECT_OVERVIEW.md    # 本文件
├── requirements.txt       # 依赖声明
└── .gitignore             # Git 忽略规则
```

## 🎯 学习路径

### 1. 初学者路径

如果你是第一次接触 Python 类型系统：

1. **阅读** [`README.md`](README.md) - 了解项目整体
2. **阅读** [`models.py`](models.py) - 理解 dataclass 和 Enum
3. **运行** `python run.py switch` - 看切换演示
4. **阅读** [`protocol.py`](protocol.py) - 理解 Protocol
5. **阅读** [`TYPE_SYSTEM.md`](TYPE_SYSTEM.md) - 深入类型系统

### 2. 进阶路径

如果你想深入理解架构设计：

1. **阅读** [`protocol.py`](protocol.py) - 抽象接口设计
2. **对比** [`sqlite_queue.py`](sqlite_queue.py) 和 [`memory_queue.py`](memory_queue.py) - 不同实现
3. **阅读** [`worker.py`](worker.py) - 业务逻辑与存储解耦
4. **阅读** [`factory.py`](factory.py) - 工厂模式 + 类型安全
5. **运行** `python test_queue.py` - 理解测试方法

### 3. 实战路径

如果你想在项目中使用：

1. **复制** 整个 `queue` 目录到你的项目
2. **修改** `models.py` - 定义你的任务类型
3. **修改** `worker.py` 中的 `process_task` - 实现你的业务逻辑
4. **选择** 存储方式：开发用 `memory`，生产用 `sqlite` 或 `redis`
5. **扩展** 添加新的队列实现（如 PostgreSQL、RabbitMQ）

## 🔑 核心概念

### 依赖倒置原则（Dependency Inversion）

```
高层模块（worker）
      ↓ 依赖
   抽象接口（Protocol）
      ↑ 实现
底层模块（SQLite/Redis/Memory）
```

**好处**：
- 业务逻辑不依赖具体实现
- 轻松切换存储方式
- 易于测试（Mock）

### 结构化类型（Structural Typing）

```python
# 不需要：
class MyQueue(TaskQueue):  # 显式继承
    ...

# 只需要：
class MyQueue:  # 实现方法即可
    async def add_task(self, task: Task) -> None:
        ...
    # ... 其他方法

# mypy 自动验证
```

### 工厂模式（Factory Pattern）

```python
# 配置驱动
queue = QueueFactory.create("sqlite")

# 类型安全
queue_type: QueueType = "sqlite"  # IDE 只提示 3 个选项
```

## 📈 扩展方向

### 已实现 ✅

- [x] Protocol 抽象接口
- [x] SQLite 持久化
- [x] 内存队列（测试）
- [x] Redis 框架
- [x] 工厂模式
- [x] 重试机制
- [x] 多 Worker
- [x] 断点续传

### 待扩展 📋

#### 高级功能
- [ ] 优先级队列（Sorted Set）
- [ ] 延迟队列（定时任务）
- [ ] 任务依赖（DAG）
- [ ] 任务链（Chain）
- [ ] 任务组（Group）

#### 分布式特性
- [ ] 分布式锁（避免重复执行）
- [ ] 心跳检测（Worker 健康检查）
- [ ] 任务超时（自动失败）
- [ ] 任务取消（Cancel）

#### 监控和管理
- [ ] Prometheus 指标
- [ ] Web 管理界面
- [ ] 任务日志记录
- [ ] 性能统计

#### 存储实现
- [ ] PostgreSQL 队列
- [ ] RabbitMQ 适配
- [ ] Kafka 适配
- [ ] AWS SQS 适配

## 🎓 教学价值

### 对系统开发工程师

- ✅ **类型系统**：从动态到静态的渐进式类型
- ✅ **架构设计**：依赖倒置、接口抽象
- ✅ **设计模式**：工厂、策略模式
- ✅ **异步编程**：asyncio 生产者-消费者
- ✅ **持久化**：SQLite、Redis 使用
- ✅ **可扩展性**：插件化架构

### 对代码质量的提升

- ✅ **类型安全**：编译时发现错误
- ✅ **自文档化**：类型注解即文档
- ✅ **IDE 支持**：自动补全、跳转
- ✅ **重构友好**：修改接口，编译器提示所有需要修改的地方
- ✅ **测试友好**：依赖注入，易于 Mock

## 💻 运行示例

### 快速测试

```bash
# 进入目录
cd examples/queue

# 运行测试
python test_queue.py

# 运行演示
python run.py memory   # 内存队列
python run.py sqlite   # SQLite 队列
python run.py switch   # 切换演示
```

### 集成到你的项目

```python
import sys
sys.path.append('path/to/queue')

from models import Task, TaskStatus
from factory import QueueFactory
from worker import worker
import asyncio

async def main():
    # 创建队列
    queue = QueueFactory.create("sqlite", db_path="my_app.db")
    
    # 添加任务
    await queue.add_task(Task(
        task_id="email-1",
        task_type="email",
        params={"to": "user@example.com", "subject": "Hello"},
        status=TaskStatus.PENDING
    ))
    
    # 启动 workers
    running_tasks = set()
    workers = [worker(i, queue, running_tasks) for i in range(4)]
    await asyncio.gather(*workers)

asyncio.run(main())
```

## 🤝 贡献指南

如果你想扩展这个项目：

1. **添加新的队列实现**
   - 创建 `xxx_queue.py`
   - 实现 `TaskQueue` Protocol 的所有方法
   - 添加到 `factory.py`

2. **添加新的任务类型**
   - 修改 `worker.py` 中的 `process_task`
   - 或使用 `dynamic_worker` 注册处理器

3. **添加高级特性**
   - 优先级队列：修改 `get_pending_tasks` 排序逻辑
   - 延迟队列：添加 `schedule_at` 字段
   - 任务依赖：添加 `depends_on` 字段

## 📚 参考资料

- [PEP 544 - Protocols](https://peps.python.org/pep-0544/)
- [PEP 604 - Union Operator](https://peps.python.org/pep-0604/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [mypy Documentation](https://mypy.readthedocs.io/)

---

**问题反馈**：如有问题或建议，欢迎提 Issue 或 PR！

**License**: MIT

