"""可插拔任务队列系统

体现 Python 现代类型系统的强大能力：
- Protocol: 结构化类型
- Literal: 限制字符串取值
- dataclass: 数据类
- Enum: 枚举类型

主要模块：
- models: 核心数据类型
- protocol: 抽象接口
- factory: 队列工厂
- worker: 业务逻辑

使用示例：
```python
from factory import QueueFactory
from models import Task, TaskStatus
from worker import worker

# 创建队列（一行切换实现）
queue = QueueFactory.create("sqlite")

# 添加任务
await queue.add_task(Task(
    task_id="task-1",
    task_type="download",
    params={"url": "example.com"},
    status=TaskStatus.PENDING
))

# 运行 worker
await worker(1, queue, set())
```
"""

from .models import Task, TaskStatus
from .protocol import TaskQueue
from .factory import QueueFactory, QueueType

__all__ = [
    "Task",
    "TaskStatus",
    "TaskQueue",
    "QueueFactory",
    "QueueType",
]

