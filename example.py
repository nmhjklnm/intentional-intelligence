# Mixin 示例：为什么 langchain 和 llamaindex 会用它

# ========== 不使用 Mixin（传统继承）==========
class Animal:
    def __init__(self, name: str):
        self.name = name
    
    def speak(self) -> str:
        return "Some sound"

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"
    
    # 如果多个类都需要 JSON 序列化，需要在每个类中重复实现
    def to_json(self) -> dict:
        return {"name": self.name, "sound": self.speak()}

class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"
    
    # 重复的代码！
    def to_json(self) -> dict:
        return {"name": self.name, "sound": self.speak()}


# ========== 使用 Mixin（组合能力）==========

# 1. 定义功能模块（Mixin）
class JSONSerializableMixin:
    """提供 JSON 序列化能力的 Mixin"""
    def to_json(self) -> dict:
        # 假设对象有 __dict__
        return {
            "class": self.__class__.__name__,
            "data": self.__dict__
        }

class LoggableMixin:
    """提供日志记录能力的 Mixin"""
    def log(self, message: str) -> None:
        print(f"[{self.__class__.__name__}] {message}")

class ValidatableMixin:
    """提供验证能力的 Mixin"""
    def validate(self) -> bool:
        # 检查是否有 name 属性
        return hasattr(self, 'name') and bool(self.name)


# 2. 通过多重继承"混入"能力
class ModernDog(Animal, JSONSerializableMixin, LoggableMixin, ValidatableMixin):
    """现代狗类：继承 Animal，混入多个功能"""
    def speak(self) -> str:
        self.log(f"{self.name} is speaking")  # 使用 LoggableMixin
        return "Woof!"

class ModernCat(Animal, JSONSerializableMixin, ValidatableMixin):
    """现代猫类：只混入需要的功能"""
    def speak(self) -> str:
        return "Meow!"


# ========== 使用示例 ==========
if __name__ == "__main__":
    dog = ModernDog("Buddy")
    
    # 来自 Animal
    print(dog.speak())  # Woof!
    
    # 来自 JSONSerializableMixin
    print(dog.to_json())  # {"class": "ModernDog", "data": {"name": "Buddy"}}
    
    # 来自 LoggableMixin
    dog.log("Playing fetch")  # [ModernDog] Playing fetch
    
    # 来自 ValidatableMixin
    print(dog.validate())  # True
    
    print("\n" + "="*50 + "\n")
    
    # Cat 没有 LoggableMixin，所以没有 log 方法
    cat = ModernCat("Whiskers")
    print(cat.speak())  # Meow!
    print(cat.to_json())  # {"class": "ModernCat", "data": {"name": "Whiskers"}}
    # cat.log("...")  # 这会报错：AttributeError


# ========== 为什么 LangChain 和 LlamaIndex 用 Mixin？ ==========

# 场景：不同的数据加载器需要不同的能力组合

class BaseMixin:
    """基础能力"""
    pass

class CacheableMixin:
    """缓存能力"""
    _cache: dict = {}
    
    def get_cached(self, key: str):
        return self._cache.get(key)
    
    def set_cache(self, key: str, value):
        self._cache[key] = value

class AsyncMixin:
    """异步能力"""
    async def load_async(self):
        # 异步加载逻辑
        pass

class StreamableMixin:
    """流式处理能力"""
    def stream(self):
        # 流式处理逻辑
        yield from []


# 不同的加载器按需组合能力
class SimpleLoader(BaseMixin):
    """简单加载器：只有基础能力"""
    pass

class CachedLoader(BaseMixin, CacheableMixin):
    """缓存加载器：基础能力 + 缓存"""
    pass

class AdvancedLoader(BaseMixin, CacheableMixin, AsyncMixin, StreamableMixin):
    """高级加载器：所有能力"""
    pass


# ========== 总结 ==========
"""
Mixin 的本质：
1. 不是"主要身份"（不单独实例化）
2. 提供一组相关的方法/属性
3. 可以与其他类组合使用
4. 解决多重继承的"菱形问题"

为什么 LangChain/LlamaIndex 用它：
- 它们有很多不同的组件（Loader, Retriever, Generator 等）
- 每个组件需要不同的能力组合（缓存、异步、流式、序列化...）
- 用 Mixin 可以灵活组合，避免代码重复
- 符合"组合优于继承"的设计原则

命名约定：
- Mixin 类名以 "Mixin" 结尾
- 通常放在继承列表的右侧（Animal, MixinA, MixinB）
- 不单独实例化（不会 x = JSONSerializableMixin()）
"""
