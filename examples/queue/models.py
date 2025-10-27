"""核心数据类型定义

体现 Python 现代类型系统：
- 使用 dataclass 代替传统类
- 使用 Enum 代替字符串常量
- 充分的类型注解
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from datetime import datetime


class TaskStatus(str, Enum):
    """任务状态枚举
    
    继承 str 使得：
    1. 可以直接与字符串比较
    2. JSON 序列化友好
    3. 类型检查器能识别
    """
    PENDING = "pending"      # 等待执行
    RUNNING = "running"      # 执行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"        # 失败


@dataclass
class Task:
    """任务数据模型
    
    使用 dataclass 的好处：
    - 自动生成 __init__, __repr__, __eq__
    - 类型注解清晰
    - IDE 自动补全
    """
    task_id: str
    task_type: str
    params: dict[str, Any]
    status: TaskStatus
    result: Optional[str] = None
    error: Optional[str] = None
    retry_count: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典（用于序列化）"""
        return {
            'task_id': self.task_id,
            'task_type': self.task_type,
            'params': self.params,
            'status': self.status.value,  # Enum 转字符串
            'result': self.result,
            'error': self.error,
            'retry_count': self.retry_count,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Task':
        """从字典创建（用于反序列化）"""
        return cls(
            task_id=data['task_id'],
            task_type=data['task_type'],
            params=data['params'],
            status=TaskStatus(data['status']),  # 字符串转 Enum
            result=data.get('result'),
            error=data.get('error'),
            retry_count=data.get('retry_count', 0),
            created_at=data.get('created_at', datetime.now().isoformat()),
            updated_at=data.get('updated_at', datetime.now().isoformat()),
        )

