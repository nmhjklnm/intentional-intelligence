"""任务队列抽象接口

体现 Python 的结构化类型系统：
- 使用 Protocol 而不是 ABC（鸭子类型 + 类型检查）
- 任何实现了这些方法的类都满足接口
- 不需要显式继承，mypy 会自动验证
"""

from typing import Protocol, Optional
from .models import TaskStatus, Task


class TaskQueue(Protocol):
    """任务队列协议（接口规范）
    
    Protocol 的优势：
    1. 结构化类型：基于方法签名，而不是继承
    2. 类型安全：mypy 会验证实现是否符合协议
    3. 鸭子类型：无需显式继承，符合 Python 哲学
    4. 灵活性：可以给第三方类"追加"协议支持
    
    示例：
    ```python
    def worker(queue: TaskQueue):  # ✅ mypy 检查参数必须实现 TaskQueue
        task = await queue.get_task("task-1")
    ```
    """
    
    async def add_task(self, task: Task) -> None:
        """添加任务到队列
        
        Args:
            task: 任务对象
        """
        ...
    
    async def get_pending_tasks(self, limit: int = 10) -> list[Task]:
        """获取待处理的任务
        
        Args:
            limit: 最多返回任务数量
            
        Returns:
            任务列表，按创建时间排序
        """
        ...
    
    async def update_task_status(
        self, 
        task_id: str, 
        status: TaskStatus,
        result: Optional[str] = None,
        error: Optional[str] = None
    ) -> None:
        """更新任务状态
        
        Args:
            task_id: 任务 ID
            status: 新状态
            result: 执行结果（可选）
            error: 错误信息（可选）
        """
        ...
    
    async def get_task(self, task_id: str) -> Optional[Task]:
        """查询单个任务
        
        Args:
            task_id: 任务 ID
            
        Returns:
            任务对象，不存在返回 None
        """
        ...


# ==================== 类型检查示例 ====================

async def _type_check_example(queue: TaskQueue) -> None:
    """
    这个函数展示了 Protocol 的类型检查能力
    
    mypy 会验证：
    1. queue 必须实现所有方法
    2. 方法签名必须匹配
    3. 返回类型必须正确
    """
    # ✅ mypy 知道 get_pending_tasks 返回 list[Task]
    tasks: list[Task] = await queue.get_pending_tasks()
    
    # ✅ mypy 知道 get_task 返回 Optional[Task]
    task: Optional[Task] = await queue.get_task("task-1")
    
    # ❌ mypy 会报错：参数类型不匹配
    # await queue.update_task_status(123, "invalid")
    
    # ✅ 类型正确
    await queue.update_task_status("task-1", TaskStatus.COMPLETED)

