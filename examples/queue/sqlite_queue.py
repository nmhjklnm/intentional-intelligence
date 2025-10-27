"""SQLite 队列实现

特点：
- 单机持久化
- 零依赖
- 适合中小规模任务
"""

import sqlite3
import json
from typing import Optional
from datetime import datetime

from .models import Task, TaskStatus


class SQLiteTaskQueue:
    """SQLite 实现的任务队列
    
    自动满足 TaskQueue Protocol：
    - 无需显式继承
    - mypy 会验证方法签名
    - 鸭子类型 + 类型检查
    """
    
    def __init__(self, db_path: str = "tasks.db"):
        """初始化队列
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self) -> None:
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                task_type TEXT NOT NULL,
                params TEXT NOT NULL,
                status TEXT NOT NULL,
                result TEXT,
                error TEXT,
                retry_count INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        # 创建索引以提升查询性能
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_status_created 
            ON tasks(status, created_at)
        """)
        conn.commit()
        conn.close()
    
    async def add_task(self, task: Task) -> None:
        """添加任务到队列"""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                INSERT OR REPLACE INTO tasks 
                (task_id, task_type, params, status, result, error, retry_count, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.task_id,
                task.task_type,
                json.dumps(task.params),
                task.status.value,
                task.result,
                task.error,
                task.retry_count,
                task.created_at,
                task.updated_at
            ))
            conn.commit()
        finally:
            conn.close()
    
    async def get_pending_tasks(self, limit: int = 10) -> list[Task]:
        """获取待处理的任务"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        try:
            cursor = conn.execute("""
                SELECT * FROM tasks 
                WHERE status = ? 
                ORDER BY created_at 
                LIMIT ?
            """, (TaskStatus.PENDING.value, limit))
            
            tasks: list[Task] = []
            for row in cursor:
                tasks.append(Task(
                    task_id=row['task_id'],
                    task_type=row['task_type'],
                    params=json.loads(row['params']),
                    status=TaskStatus(row['status']),
                    result=row['result'],
                    error=row['error'],
                    retry_count=row['retry_count'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ))
            return tasks
        finally:
            conn.close()
    
    async def update_task_status(
        self, 
        task_id: str, 
        status: TaskStatus,
        result: Optional[str] = None,
        error: Optional[str] = None
    ) -> None:
        """更新任务状态"""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                UPDATE tasks 
                SET status = ?, result = ?, error = ?, updated_at = ?
                WHERE task_id = ?
            """, (
                status.value, 
                result, 
                error, 
                datetime.now().isoformat(), 
                task_id
            ))
            conn.commit()
        finally:
            conn.close()
    
    async def get_task(self, task_id: str) -> Optional[Task]:
        """查询单个任务"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        try:
            cursor = conn.execute(
                "SELECT * FROM tasks WHERE task_id = ?", 
                (task_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return Task(
                task_id=row['task_id'],
                task_type=row['task_type'],
                params=json.loads(row['params']),
                status=TaskStatus(row['status']),
                result=row['result'],
                error=row['error'],
                retry_count=row['retry_count'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        finally:
            conn.close()
    
    async def reset_running_tasks(self) -> int:
        """重置运行中的任务为待处理（用于程序重启恢复）
        
        Returns:
            重置的任务数量
        """
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.execute("""
                UPDATE tasks 
                SET status = ?, updated_at = ?
                WHERE status = ?
            """, (
                TaskStatus.PENDING.value,
                datetime.now().isoformat(),
                TaskStatus.RUNNING.value
            ))
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()

