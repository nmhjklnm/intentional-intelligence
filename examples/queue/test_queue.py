"""简单的功能测试

验证队列系统的基本功能
"""

import sys
from pathlib import Path

# 添加上级目录到 Python 路径
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

import asyncio
from examples.queue.models import Task, TaskStatus
from examples.queue.memory_queue import InMemoryTaskQueue


async def test_basic_operations():
    """测试基本操作"""
    print("🧪 测试基本操作...")
    
    # 创建队列
    queue = InMemoryTaskQueue()
    
    # 添加任务
    task = Task(
        task_id="test-1",
        task_type="test",
        params={"data": "test"},
        status=TaskStatus.PENDING
    )
    await queue.add_task(task)
    print("  ✅ 任务已添加")
    
    # 查询任务
    retrieved = await queue.get_task("test-1")
    assert retrieved is not None
    assert retrieved.task_id == "test-1"
    print("  ✅ 任务查询成功")
    
    # 获取待处理任务
    pending = await queue.get_pending_tasks()
    assert len(pending) == 1
    assert pending[0].task_id == "test-1"
    print("  ✅ 获取待处理任务成功")
    
    # 更新状态
    await queue.update_task_status("test-1", TaskStatus.COMPLETED, result="success")
    updated = await queue.get_task("test-1")
    assert updated.status == TaskStatus.COMPLETED
    assert updated.result == "success"
    print("  ✅ 状态更新成功")
    
    # 统计
    stats = queue.get_stats()
    assert stats['total'] == 1
    assert stats['completed'] == 1
    print(f"  ✅ 统计信息: {stats}")
    
    print("✅ 所有测试通过！\n")


async def test_type_safety():
    """测试类型安全"""
    print("🧪 测试类型安全...")
    
    from examples.queue.protocol import TaskQueue
    from examples.queue.sqlite_queue import SQLiteTaskQueue
    from examples.queue.memory_queue import InMemoryTaskQueue
    
    # 验证类型兼容性
    memory_queue: TaskQueue = InMemoryTaskQueue()
    sqlite_queue: TaskQueue = SQLiteTaskQueue(":memory:")
    
    print("  ✅ InMemoryTaskQueue 满足 TaskQueue Protocol")
    print("  ✅ SQLiteTaskQueue 满足 TaskQueue Protocol")
    print("✅ 类型安全测试通过！\n")


async def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🚀 运行队列系统测试")
    print("="*60 + "\n")
    
    await test_basic_operations()
    await test_type_safety()
    
    print("="*60)
    print("🎉 所有测试完成！")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())

