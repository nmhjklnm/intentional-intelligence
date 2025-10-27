"""内存队列实现

特点：
- 无需外部依赖
- 适合测试和开发
- 程序重启后数据丢失
"""

from typing import Optional
from datetime import datetime

from .models import Task, TaskStatus


class InMemoryTaskQueue:
    """内存实现的任务队列
    
    满足 TaskQueue Protocol，适合：
    - 单元测试
    - 本地开发
    - 临时任务
    """
    
    def __init__(self):
        """初始化内存存储"""
        self.tasks: dict[str, Task] = {}
        self.pending_queue: list[str] = []  # 只存 task_id
    
    async def add_task(self, task: Task) -> None:
        """添加任务到队列"""
        self.tasks[task.task_id] = task
        
        # 如果是待处理任务，加入队列
        if task.status == TaskStatus.PENDING:
            if task.task_id not in self.pending_queue:
                self.pending_queue.append(task.task_id)
    
    async def get_pending_tasks(self, limit: int = 10) -> list[Task]:
        """获取待处理的任务"""
        # 获取前 limit 个任务 ID
        task_ids = self.pending_queue[:limit]
        
        # 转换为 Task 对象
        tasks: list[Task] = []
        for task_id in task_ids:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                # 确保状态仍是 PENDING
                if task.status == TaskStatus.PENDING:
                    tasks.append(task)
        
        return tasks
    
    async def update_task_status(
        self, 
        task_id: str, 
        status: TaskStatus,
        result: Optional[str] = None,
        error: Optional[str] = None
    ) -> None:
        """更新任务状态"""
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        task.status = status
        task.result = result
        task.error = error
        task.updated_at = datetime.now().isoformat()
        
        # 从待处理队列中移除（如果不是 PENDING 状态）
        if status != TaskStatus.PENDING and task_id in self.pending_queue:
            self.pending_queue.remove(task_id)
        
        # 如果改回 PENDING，重新加入队列
        if status == TaskStatus.PENDING and task_id not in self.pending_queue:
            self.pending_queue.append(task_id)
    
    async def get_task(self, task_id: str) -> Optional[Task]:
        """查询单个任务"""
        return self.tasks.get(task_id)
    
    def get_stats(self) -> dict[str, int]:
        """获取队列统计信息（测试用）
        
        Returns:
            统计信息：各状态任务数量
        """
        stats: dict[str, int] = {
            'total': len(self.tasks),
            'pending': 0,
            'running': 0,
            'completed': 0,
            'failed': 0,
        }
        
        for task in self.tasks.values():
            stats[task.status.value] += 1
        
        return stats

