"""主程序入口

演示如何使用可插拔的任务队列系统
"""

import asyncio
from typing import Literal

from .models import Task, TaskStatus
from .factory import QueueFactory, QueueType
from .worker import worker
from .sqlite_queue import SQLiteTaskQueue


async def producer(queue_type: QueueType = "memory"):
    """生产者示例：动态添加任务"""
    print("\n" + "="*60)
    print(f"🎬 启动任务队列系统 (存储: {queue_type})")
    print("="*60 + "\n")
    
    # 🔥 一行代码切换存储方式
    queue = QueueFactory.create(queue_type)
    
    # 如果是 SQLite，重置运行中的任务（断点续传）
    if isinstance(queue, SQLiteTaskQueue):
        reset_count = await queue.reset_running_tasks()
        if reset_count > 0:
            print(f"♻️  已恢复 {reset_count} 个中断的任务\n")
    
    # 添加初始任务
    print("📝 添加初始任务...")
    await queue.add_task(Task(
        task_id="task-1",
        task_type="download",
        params={"url": "http://example.com/file1.zip", "duration": 2},
        status=TaskStatus.PENDING
    ))
    
    await queue.add_task(Task(
        task_id="task-2",
        task_type="compute",
        params={"a": 100, "b": 200, "duration": 1.5},
        status=TaskStatus.PENDING
    ))
    
    await queue.add_task(Task(
        task_id="task-3",
        task_type="email",
        params={"to": "user@example.com", "subject": "Test Email", "duration": 1},
        status=TaskStatus.PENDING
    ))
    
    # 模拟动态添加任务
    await asyncio.sleep(2)
    print("\n📝 动态添加新任务...")
    await queue.add_task(Task(
        task_id="task-4",
        task_type="download",
        params={"url": "http://example.com/file2.zip", "duration": 1},
        status=TaskStatus.PENDING
    ))
    
    return queue


async def run_workers(queue, num_workers: int = 2, duration: int = 10):
    """运行 worker 处理任务
    
    Args:
        queue: 任务队列（任何实现了 TaskQueue 的对象）
        num_workers: Worker 数量
        duration: 运行时长（秒）
    """
    running_tasks: set[str] = set()
    
    # 创建多个 worker
    workers = [
        worker(i+1, queue, running_tasks, max_retries=3, poll_interval=0.5)
        for i in range(num_workers)
    ]
    
    # 运行一段时间后停止
    try:
        await asyncio.wait_for(
            asyncio.gather(*workers),
            timeout=duration
        )
    except asyncio.TimeoutError:
        print(f"\n⏰ 运行时长达到 {duration} 秒，停止 workers")


async def show_results(queue):
    """显示任务执行结果"""
    print("\n" + "="*60)
    print("📊 任务执行结果")
    print("="*60)
    
    for task_id in ["task-1", "task-2", "task-3", "task-4"]:
        task = await queue.get_task(task_id)
        if task:
            status_emoji = {
                TaskStatus.PENDING: "⏳",
                TaskStatus.RUNNING: "🔄",
                TaskStatus.COMPLETED: "✅",
                TaskStatus.FAILED: "❌",
            }
            emoji = status_emoji.get(task.status, "❓")
            
            print(f"\n{emoji} {task.task_id}")
            print(f"   类型: {task.task_type}")
            print(f"   状态: {task.status.value}")
            if task.result:
                print(f"   结果: {task.result}")
            if task.error:
                print(f"   错误: {task.error}")
    
    print("\n" + "="*60 + "\n")


async def demo_memory():
    """演示：内存队列（适合测试）"""
    queue = await producer("memory")
    await run_workers(queue, num_workers=2, duration=8)
    await show_results(queue)


async def demo_sqlite():
    """演示：SQLite 队列（适合单机生产）"""
    queue = await producer("sqlite")
    await run_workers(queue, num_workers=2, duration=8)
    await show_results(queue)


async def demo_switch_queue():
    """演示：轻松切换队列实现"""
    print("\n" + "="*60)
    print("🔄 演示：切换队列实现")
    print("="*60 + "\n")
    
    # 场景1：开发环境用内存队列
    print("💻 开发环境：使用内存队列（快速测试）")
    dev_queue = QueueFactory.create("memory")
    await dev_queue.add_task(Task(
        task_id="dev-task",
        task_type="compute",
        params={"a": 1, "b": 2, "duration": 0.1},
        status=TaskStatus.PENDING
    ))
    print("   ✅ 任务已添加到内存队列\n")
    
    # 场景2：单机生产用 SQLite
    print("🏢 单机生产：使用 SQLite（持久化）")
    prod_queue = QueueFactory.create("sqlite", db_path="production.db")
    await prod_queue.add_task(Task(
        task_id="prod-task",
        task_type="download",
        params={"url": "prod-file.zip", "duration": 0.1},
        status=TaskStatus.PENDING
    ))
    print("   ✅ 任务已添加到 SQLite 队列\n")
    
    # 场景3：分布式生产用 Redis（框架）
    print("🌐 分布式生产：使用 Redis（高性能）")
    redis_queue = QueueFactory.create("redis", redis_url="redis://prod-server:6379")
    await redis_queue.add_task(Task(
        task_id="redis-task",
        task_type="email",
        params={"to": "user@prod.com", "duration": 0.1},
        status=TaskStatus.PENDING
    ))
    print("   ⚠️  这是框架实现，实际使用需要安装 redis 包\n")
    
    print("🎉 切换队列只需要改变 create() 的第一个参数！")
    print("   业务代码完全不需要修改\n")


async def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "memory":
            await demo_memory()
        elif mode == "sqlite":
            await demo_sqlite()
        elif mode == "switch":
            await demo_switch_queue()
        else:
            print(f"❌ 未知模式: {mode}")
            print("用法: python main.py [memory|sqlite|switch]")
    else:
        # 默认运行内存队列演示
        print("💡 提示：可以指定运行模式")
        print("   python main.py memory   - 内存队列")
        print("   python main.py sqlite   - SQLite 队列")
        print("   python main.py switch   - 切换演示\n")
        
        await demo_memory()


if __name__ == "__main__":
    # 运行主程序
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  程序被用户中断")

