#!/usr/bin/env python3
"""运行脚本

确保导入路径正确，然后运行 main.py

用法：
    python run.py          # 运行内存队列演示
    python run.py memory   # 运行内存队列演示
    python run.py sqlite   # 运行 SQLite 队列演示
    python run.py switch   # 运行切换演示
"""

import sys
from pathlib import Path

# 将上级目录添加到 Python 路径，确保可以导入 examples.queue 包
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# 导入并运行 main
if __name__ == "__main__":
    # 以模块方式导入
    from examples.queue import main
    
    # 运行 main 中的 asyncio 程序
    import asyncio
    try:
        asyncio.run(main.main())
    except KeyboardInterrupt:
        print("\n\n⏹️  程序被用户中断")

