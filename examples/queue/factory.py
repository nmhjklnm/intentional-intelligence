"""队列工厂（配置驱动）

体现 Python 现代类型系统：
- 使用 Literal 限制字符串取值
- 使用 TypeAlias 提供类型别名
- 工厂模式 + 类型安全
"""

from typing import Literal

from .protocol import TaskQueue
from .sqlite_queue import SQLiteTaskQueue
from .redis_queue import RedisTaskQueue
from .memory_queue import InMemoryTaskQueue


# 类型别名：限制队列类型只能是这三种
QueueType = Literal["sqlite", "redis", "memory"]


class QueueFactory:
    """队列工厂类
    
    特点：
    1. 配置驱动：根据配置创建不同实现
    2. 类型安全：返回类型是 TaskQueue Protocol
    3. 易于扩展：新增实现只需添加一个分支
    
    使用示例：
    ```python
    # 开发环境：内存队列
    queue = QueueFactory.create("memory")
    
    # 单机生产：SQLite
    queue = QueueFactory.create("sqlite", db_path="prod.db")
    
    # 分布式生产：Redis
    queue = QueueFactory.create("redis", redis_url="redis://prod:6379")
    ```
    """
    
    @staticmethod
    def create(
        queue_type: QueueType,  # 🔥 Literal 保证只能传入 "sqlite" | "redis" | "memory"
        **kwargs
    ) -> TaskQueue:  # 🔥 返回类型是 Protocol，而不是具体类
        """创建任务队列
        
        Args:
            queue_type: 队列类型（"sqlite" | "redis" | "memory"）
            **kwargs: 传递给具体实现的参数
            
        Returns:
            任务队列实例（满足 TaskQueue Protocol）
            
        Raises:
            ValueError: 不支持的队列类型
        
        类型检查：
        - mypy 会验证 queue_type 只能是三个值之一
        - 如果传入 "mysql"，编译时就会报错
        - 返回值保证实现了 TaskQueue 接口
        """
        if queue_type == "sqlite":
            db_path = kwargs.get("db_path", "tasks.db")
            return SQLiteTaskQueue(db_path=db_path)
        
        elif queue_type == "redis":
            redis_url = kwargs.get("redis_url", "redis://localhost:6379")
            return RedisTaskQueue(redis_url=redis_url)
        
        elif queue_type == "memory":
            return InMemoryTaskQueue()
        
        else:
            # 实际上这个分支永远不会执行（mypy 保证）
            # 但为了运行时安全，还是保留
            raise ValueError(f"Unsupported queue type: {queue_type}")
    
    @staticmethod
    def create_from_config(config: dict) -> TaskQueue:
        """从配置字典创建队列
        
        Args:
            config: 配置字典，格式：
                {
                    "type": "sqlite",
                    "db_path": "tasks.db"
                }
        
        Returns:
            任务队列实例
        """
        queue_type = config.get("type", "memory")
        
        # 移除 type 字段，其余作为参数传递
        kwargs = {k: v for k, v in config.items() if k != "type"}
        
        return QueueFactory.create(queue_type, **kwargs)  # type: ignore


# ==================== 类型检查示例 ====================

def _type_check_example():
    """展示类型系统的威力"""
    
    # ✅ 正确：类型是 Literal 中的值
    queue1: TaskQueue = QueueFactory.create("sqlite")
    queue2: TaskQueue = QueueFactory.create("redis")
    queue3: TaskQueue = QueueFactory.create("memory")
    
    # ❌ 错误：mypy 会报错（字符串不在 Literal 中）
    # queue4 = QueueFactory.create("mysql")  # Error: Argument has incompatible type
    
    # ✅ 正确：返回值实现了 TaskQueue Protocol
    async def use_queue(q: TaskQueue):
        # mypy 知道 q 有 add_task 方法
        # 自动补全、类型检查都有
        pass
    
    # ✅ 动态类型也有类型提示
    queue_type: QueueType = "sqlite"  # IDE 会提示只能是三个值之一
    queue = QueueFactory.create(queue_type)

