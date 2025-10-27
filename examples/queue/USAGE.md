# 使用指南

## 📦 包结构说明

本项目使用 **Python 包（Package）** 结构，所有模块使用**相对导入**：

```python
# ✅ 正确：相对导入
from .models import Task, TaskStatus
from .protocol import TaskQueue

# ❌ 错误：绝对导入
from models import Task  # 找不到模块
from examples.queue.models import Task  # 路径依赖
```

## 🚀 运行方式

### 方式 1：作为模块运行（推荐）

从**项目根目录**运行，使用 `-m` 参数：

```bash
cd /Users/yangyihe/Documents/projects/类型系统

# 运行测试
python -m examples.queue.test_queue

# 运行演示
python -m examples.queue.run memory
python -m examples.queue.run sqlite
python -m examples.queue.run switch
```

**优点**：
- ✅ Python 自动处理包导入
- ✅ 相对导入正常工作
- ✅ 类型检查器（mypy）无错误
- ✅ IDE 智能提示正常

### 方式 2：使用运行脚本

在 `examples/queue/` 目录下：

```bash
cd examples/queue
python run.py memory    # 内存队列
python run.py sqlite    # SQLite 队列
python run.py switch    # 切换演示
```

`run.py` 会自动设置 Python 路径，然后以模块方式导入。

## 🔍 为什么使用相对导入？

### Python 包的最佳实践

```
类型系统/
└── examples/
    └── queue/            # 这是一个包
        ├── __init__.py   # 包标识文件
        ├── models.py     # 使用 from .models import ...
        ├── protocol.py   # 使用 from .models import ...
        └── ...
```

### 相对导入的优势

| 导入方式 | 示例 | 优点 | 缺点 |
|---------|------|------|------|
| **相对导入** | `from .models import Task` | 包结构清晰，易于重命名包 | 必须作为包运行 |
| 简单导入 | `from models import Task` | 看起来简单 | 路径依赖，类型检查报错 |
| 绝对路径 | `from examples.queue.models import Task` | 明确 | 包名硬编码，难以移动 |

### 类型检查器要求

mypy 和其他类型检查器**要求包使用相对导入**：

```bash
# ❌ 简单导入会报错
$ mypy protocol.py
protocol.py:10: error: Cannot find implementation or library stub for module named "models"

# ✅ 相对导入正常
$ mypy protocol.py
Success: no issues found
```

## 📝 在你的项目中使用

### 方式 1：作为子包

```python
# 项目结构
my_project/
├── examples/
│   └── queue/     # 复制整个 queue 目录
└── main.py

# 在 main.py 中
from examples.queue import QueueFactory, Task, TaskStatus

queue = QueueFactory.create("sqlite")
```

### 方式 2：独立使用

```python
# 复制 queue 目录到你的项目
my_project/
└── queue/         # 复制的 queue 目录

# 在代码中
from queue import QueueFactory, Task, TaskStatus

queue = QueueFactory.create("sqlite")
```

### 方式 3：修改代码以使用简单导入

如果你确实需要简单导入（不推荐），可以在每个文件开头添加：

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# 然后使用简单导入
from models import Task
```

**但这不是推荐做法**，会导致：
- ❌ mypy 报错
- ❌ IDE 智能提示失效
- ❌ 不符合 Python 包规范

## 🎓 Python 包与模块的区别

### 模块（Module）

单个 `.py` 文件：

```python
# utils.py - 这是一个模块
def helper():
    pass

# 使用
import utils
utils.helper()
```

### 包（Package）

包含 `__init__.py` 的目录：

```python
# mypackage/          - 这是一个包
#   __init__.py
#   module1.py
#   module2.py

# module1.py 中使用相对导入
from .module2 import something

# 外部使用
from mypackage import module1
from mypackage.module1 import something
```

## 🔧 常见问题

### Q: 为什么不能直接 `python main.py`？

**A**: 因为 `main.py` 中使用了相对导入 `from .models import ...`，直接运行会报错：

```bash
$ python main.py
ImportError: attempted relative import with no known parent package
```

**解决方案**：使用 `-m` 参数作为模块运行：

```bash
$ python -m examples.queue.main  # ✅
```

### Q: mypy 报错 "Cannot find implementation"？

**A**: mypy 需要从包的根目录运行：

```bash
# ❌ 错误
cd examples/queue
mypy protocol.py

# ✅ 正确
cd /path/to/类型系统
mypy examples/queue/protocol.py
```

### Q: IDE 显示导入错误？

**A**: 确保 IDE 的工作目录设置为项目根目录（`/path/to/类型系统/`）。

## 📊 总结

| 场景 | 命令 | 说明 |
|-----|------|------|
| **测试** | `python -m examples.queue.test_queue` | 运行测试 |
| **演示** | `python -m examples.queue.run memory` | 内存队列 |
| **演示** | `python -m examples.queue.run sqlite` | SQLite 队列 |
| **演示** | `python -m examples.queue.run switch` | 切换演示 |
| **类型检查** | `mypy examples/queue/` | 检查所有文件 |
| **便捷脚本** | `cd examples/queue && python run.py` | 简化命令 |

## 💡 核心要点

1. ✅ **使用相对导入**（`from .models import ...`）
2. ✅ **从根目录运行**（`python -m examples.queue.xxx`）
3. ✅ **包含 `__init__.py`**（标识为包）
4. ✅ **符合 Python 规范**（可被 mypy 检查）

---

**Happy Coding! 🎉**

