"""Redis 队列实现框架

特点：
- 分布式支持
- 高性能
- 适合大规模任务

注意：这是框架实现，展示如何扩展到 Redis
实际使用需要安装：pip install redis
"""

from typing import Optional
# from redis.asyncio import Redis  # 实际使用时取消注释

from .models import Task, TaskStatus


class RedisTaskQueue:
    """Redis 实现的任务队列（框架）
    
    同样满足 TaskQueue Protocol，可无缝切换
    
    实际部署时的步骤：
    1. pip install redis
    2. 启动 Redis: docker run -p 6379:6379 redis
    3. 取消注释 Redis 导入和实现
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        """初始化 Redis 连接
        
        Args:
            redis_url: Redis 连接 URL
        """
        self.redis_url = redis_url
        # self.redis = Redis.from_url(redis_url, decode_responses=True)
        print(f"[Redis] 初始化连接: {redis_url}")
        print("[Redis] ⚠️  这是框架实现，实际使用需要安装 redis 包")
    
    async def add_task(self, task: Task) -> None:
        """添加任务到队列
        
        实现思路：
        1. 将任务推入 List（作为队列）: LPUSH task_queue task_json
        2. 存储任务详情到 Hash: HSET tasks task_id task_json
        """
        print(f"[Redis] add_task: {task.task_id}")
        # task_json = json.dumps(task.to_dict())
        # await self.redis.lpush("task_queue", task_json)
        # await self.redis.hset("tasks", task.task_id, task_json)
    
    async def get_pending_tasks(self, limit: int = 10) -> list[Task]:
        """获取待处理的任务
        
        实现思路：
        1. 从 List 右侧弹出: RPOP task_queue
        2. 限制数量：循环 limit 次
        """
        print(f"[Redis] get_pending_tasks: limit={limit}")
        # tasks = []
        # for _ in range(limit):
        #     task_json = await self.redis.rpop("task_queue")
        #     if not task_json:
        #         break
        #     tasks.append(Task.from_dict(json.loads(task_json)))
        # return tasks
        return []
    
    async def update_task_status(
        self, 
        task_id: str, 
        status: TaskStatus,
        result: Optional[str] = None,
        error: Optional[str] = None
    ) -> None:
        """更新任务状态
        
        实现思路：
        1. 从 Hash 获取任务: HGET tasks task_id
        2. 更新字段
        3. 写回 Hash: HSET tasks task_id updated_json
        """
        print(f"[Redis] update_task_status: {task_id} -> {status.value}")
        # task_json = await self.redis.hget("tasks", task_id)
        # if task_json:
        #     task_dict = json.loads(task_json)
        #     task_dict['status'] = status.value
        #     task_dict['result'] = result
        #     task_dict['error'] = error
        #     await self.redis.hset("tasks", task_id, json.dumps(task_dict))
    
    async def get_task(self, task_id: str) -> Optional[Task]:
        """查询单个任务
        
        实现思路：
        1. 从 Hash 查询: HGET tasks task_id
        2. 反序列化为 Task 对象
        """
        print(f"[Redis] get_task: {task_id}")
        # task_json = await self.redis.hget("tasks", task_id)
        # if task_json:
        #     return Task.from_dict(json.loads(task_json))
        return None
    
    async def close(self) -> None:
        """关闭 Redis 连接"""
        # await self.redis.close()
        pass


# ==================== 分布式特性说明 ====================

"""
Redis 队列的优势：

1. **分布式支持**：
   - 多个 worker 可以在不同机器上运行
   - 共享同一个 Redis 队列
   - 自动负载均衡

2. **高性能**：
   - 内存存储，读写快
   - 支持持久化（RDB + AOF）
   - 支持主从复制、哨兵、集群

3. **丰富的数据结构**：
   - List: 队列（LPUSH + RPOP）
   - Hash: 任务详情存储
   - Sorted Set: 优先级队列、延迟队列
   - Pub/Sub: 实时通知

4. **原子操作**：
   - BRPOP: 阻塞式弹出（无任务时等待）
   - RPOPLPUSH: 原子性移动（实现可靠队列）
   - Lua 脚本: 复杂原子操作

部署架构示例：
┌─────────┐   ┌─────────┐   ┌─────────┐
│ Worker1 │   │ Worker2 │   │ Worker3 │  (不同机器)
└────┬────┘   └────┬────┘   └────┬────┘
     │             │             │
     └─────────────┼─────────────┘
                   │
            ┌──────▼──────┐
            │    Redis    │  (中心队列)
            └─────────────┘
"""

