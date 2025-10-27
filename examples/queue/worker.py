"""工作进程（业务逻辑层）

特点：
- 与存储方式无关
- 只依赖 TaskQueue Protocol
- 可复用的任务处理逻辑
"""

import asyncio
from datetime import datetime
from typing import Callable, Awaitable

from .protocol import TaskQueue
from .models import Task, TaskStatus


async def process_task(task: Task) -> str:
    """处理任务的业务逻辑
    
    这里可以根据 task_type 执行不同的操作
    
    Args:
        task: 任务对象
        
    Returns:
        执行结果
        
    Raises:
        Exception: 任务执行失败
    """
    print(f"[{_timestamp()}] 🔨 处理任务 {task.task_id} (类型: {task.task_type})")
    
    if task.task_type == "download":
        # 模拟下载任务
        url = task.params.get("url", "unknown")
        duration = task.params.get("duration", 2)
        await asyncio.sleep(duration)
        return f"Downloaded: {url}"
    
    elif task.task_type == "compute":
        # 模拟计算任务
        a = task.params.get("a", 0)
        b = task.params.get("b", 0)
        duration = task.params.get("duration", 1)
        await asyncio.sleep(duration)
        return f"Compute result: {a} + {b} = {a + b}"
    
    elif task.task_type == "email":
        # 模拟发送邮件
        to = task.params.get("to", "unknown")
        subject = task.params.get("subject", "")
        duration = task.params.get("duration", 1)
        await asyncio.sleep(duration)
        return f"Email sent to {to}: {subject}"
    
    else:
        raise ValueError(f"Unknown task type: {task.task_type}")


async def worker(
    worker_id: int,
    queue: TaskQueue,  # 🔥 依赖抽象接口，不依赖具体实现
    running_tasks: set[str],
    max_retries: int = 3,
    poll_interval: float = 1.0
) -> None:
    """工作进程
    
    Args:
        worker_id: Worker 编号
        queue: 任务队列（任何实现了 TaskQueue Protocol 的对象）
        running_tasks: 正在运行的任务集合（多 worker 协调用）
        max_retries: 最大重试次数
        poll_interval: 轮询间隔（秒）
    
    类型安全：
    - mypy 会验证 queue 参数必须实现 TaskQueue Protocol
    - 编译时保证类型安全
    - 运行时无需类型检查
    """
    print(f"[{_timestamp()}] 🚀 Worker {worker_id} 启动")
    
    while True:
        # 获取待处理任务
        tasks = await queue.get_pending_tasks(limit=1)
        
        if not tasks:
            # 无任务时等待
            await asyncio.sleep(poll_interval)
            continue
        
        task = tasks[0]
        
        # 避免多个 worker 同时处理同一任务
        if task.task_id in running_tasks:
            continue
        
        running_tasks.add(task.task_id)
        
        try:
            # 标记为运行中
            await queue.update_task_status(task.task_id, TaskStatus.RUNNING)
            print(f"[{_timestamp()}] 📋 Worker {worker_id} 开始处理任务 {task.task_id}")
            
            # 执行任务
            result = await process_task(task)
            
            # 标记为完成
            await queue.update_task_status(
                task.task_id, 
                TaskStatus.COMPLETED,
                result=result
            )
            print(f"[{_timestamp()}] ✅ Worker {worker_id} 完成任务 {task.task_id}: {result}")
        
        except Exception as e:
            # 任务失败处理
            task.retry_count += 1
            error_msg = f"{type(e).__name__}: {str(e)}"
            
            if task.retry_count < max_retries:
                # 重试
                print(f"[{_timestamp()}] ⚠️  Worker {worker_id} 任务 {task.task_id} 失败，"
                      f"重试 {task.retry_count}/{max_retries}: {error_msg}")
                
                # 重新加入队列
                task.status = TaskStatus.PENDING
                await queue.add_task(task)
            
            else:
                # 彻底失败
                print(f"[{_timestamp()}] ❌ Worker {worker_id} 任务 {task.task_id} 失败: {error_msg}")
                await queue.update_task_status(
                    task.task_id,
                    TaskStatus.FAILED,
                    error=error_msg
                )
        
        finally:
            running_tasks.discard(task.task_id)


async def dynamic_worker(
    worker_id: int,
    queue: TaskQueue,
    running_tasks: set[str],
    task_handlers: dict[str, Callable[[Task], Awaitable[str]]],
    max_retries: int = 3,
    poll_interval: float = 1.0
) -> None:
    """动态任务处理器的 Worker
    
    Args:
        worker_id: Worker 编号
        queue: 任务队列
        running_tasks: 运行中任务集合
        task_handlers: 任务类型 -> 处理函数的映射
        max_retries: 最大重试次数
        poll_interval: 轮询间隔
    
    特点：
    - 支持动态注册任务处理器
    - 更灵活的任务处理方式
    """
    print(f"[{_timestamp()}] 🚀 Dynamic Worker {worker_id} 启动")
    print(f"[{_timestamp()}] 📚 已注册任务类型: {list(task_handlers.keys())}")
    
    while True:
        tasks = await queue.get_pending_tasks(limit=1)
        
        if not tasks:
            await asyncio.sleep(poll_interval)
            continue
        
        task = tasks[0]
        
        if task.task_id in running_tasks:
            continue
        
        # 检查是否有对应的处理器
        if task.task_type not in task_handlers:
            print(f"[{_timestamp()}] ⚠️  未找到任务类型 {task.task_type} 的处理器")
            await queue.update_task_status(
                task.task_id,
                TaskStatus.FAILED,
                error=f"No handler for task type: {task.task_type}"
            )
            continue
        
        running_tasks.add(task.task_id)
        
        try:
            await queue.update_task_status(task.task_id, TaskStatus.RUNNING)
            
            # 调用对应的处理器
            handler = task_handlers[task.task_type]
            result = await handler(task)
            
            await queue.update_task_status(
                task.task_id,
                TaskStatus.COMPLETED,
                result=result
            )
            print(f"[{_timestamp()}] ✅ Dynamic Worker {worker_id} 完成: {result}")
        
        except Exception as e:
            task.retry_count += 1
            error_msg = f"{type(e).__name__}: {str(e)}"
            
            if task.retry_count < max_retries:
                task.status = TaskStatus.PENDING
                await queue.add_task(task)
            else:
                await queue.update_task_status(
                    task.task_id,
                    TaskStatus.FAILED,
                    error=error_msg
                )
        
        finally:
            running_tasks.discard(task.task_id)


def _timestamp() -> str:
    """返回格式化的时间戳"""
    return datetime.now().strftime("%H:%M:%S")

