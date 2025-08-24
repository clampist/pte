# PTE Framework Retry功能使用指南

## 概述

PTE Framework提供了强大的重试功能，支持多种重试策略和条件，帮助处理不稳定的操作和网络请求。所有重试功能都集成在core层，可以通过简单的装饰器语法使用。

## 主要特性

- **多种重试策略**: 固定延迟、指数退避、线性退避、随机延迟、斐波那契退避
- **灵活的条件判断**: 支持异常重试、结果条件重试、超时重试
- **丰富的操作符**: 支持等于、不等于、大于、小于、包含等操作符
- **完整的日志记录**: 自动记录重试过程和结果
- **便捷的装饰器**: 提供多种预设的便捷装饰器

## 基础用法

### 1. 基础重试装饰器

```python
from core.retry import retry

@retry(max_attempts=3, delay=1.0, strategy="exponential")
def api_call():
    # 你的API调用代码
    response = requests.get("https://api.example.com/data")
    response.raise_for_status()
    return response.json()
```

### 2. 异常重试

```python
from core.retry import retry_on_exception

@retry_on_exception(
    exceptions=(ConnectionError, TimeoutError),
    max_attempts=5,
    delay=2.0
)
def network_operation():
    # 网络操作代码
    pass
```

### 3. 条件重试

```python
from core.retry import retry_with_condition

# 使用函数条件
@retry_with_condition(
    condition=lambda result: result.get("status") != "ready",
    max_attempts=10,
    delay=1.0
)
def check_processing_status():
    # 检查处理状态的代码
    return {"status": "pending", "progress": 50}
```

## 高级用法

### 1. 字典条件重试

```python
# 简单字典条件
@retry_with_condition(
    condition={"status": "success", "code": 200},
    max_attempts=5
)
def api_request():
    return {"status": "pending", "code": 202}

# 使用操作符的字典条件
@retry_with_condition(
    condition={
        "count": {"operator": "gte", "value": 5},
        "status": "completed"
    },
    max_attempts=10
)
def batch_processing():
    return {"count": 3, "status": "processing"}
```

### 2. 支持的操作符

```python
# 等于
{"field": {"operator": "eq", "value": "expected"}}

# 不等于
{"field": {"operator": "ne", "value": "unexpected"}}

# 大于
{"count": {"operator": "gt", "value": 10}}

# 大于等于
{"count": {"operator": "gte", "value": 5}}

# 小于
{"count": {"operator": "lt", "value": 100}}

# 小于等于
{"count": {"operator": "lte", "value": 50}}

# 包含
{"message": {"operator": "contains", "value": "success"}}

# 不包含
{"message": {"operator": "not_contains", "value": "error"}}

# 在列表中
{"status": {"operator": "in", "value": ["pending", "processing"]}}

# 不在列表中
{"status": {"operator": "not_in", "value": ["failed", "cancelled"]}}
```

### 3. 重试策略

```python
from core.retry import RetryStrategy

# 固定延迟
@retry(strategy=RetryStrategy.FIXED, delay=2.0)

# 指数退避（默认）
@retry(strategy=RetryStrategy.EXPONENTIAL, delay=1.0)

# 线性退避
@retry(strategy=RetryStrategy.LINEAR, delay=1.0)

# 随机延迟
@retry(strategy=RetryStrategy.RANDOM, delay=1.0)

# 斐波那契退避
@retry(strategy=RetryStrategy.FIBONACCI, delay=1.0)
```

## 便捷装饰器

### 1. 常用便捷装饰器

```python
from core.retry import (
    retry_on_false,
    retry_on_none,
    retry_on_empty,
    retry_until_success,
    retry_on_timeout,
    retry_on_exception
)

# 重试直到返回True
@retry_on_false(max_attempts=5, delay=1.0, strategy="exponential")
def wait_for_condition():
    return some_condition()

# 重试直到返回非None值
@retry_on_none(max_attempts=3, delay=0.5)
def get_data():
    return fetch_data()

# 重试直到返回非空结果
@retry_on_empty(max_attempts=4, delay=1.0)
def get_list():
    return fetch_list()

# 重试直到成功
@retry_until_success(max_attempts=10, delay=2.0, strategy="exponential")
def unreliable_operation():
    return risky_operation()

# 带超时的重试
@retry_on_timeout(timeout=30.0, max_attempts=5, delay=1.0)
def long_running_task():
    return slow_operation()

# 异常重试（支持所有参数）
@retry_on_exception(
    exceptions=(ConnectionError, TimeoutError),
    max_attempts=3,
    delay=1.0,
    strategy="exponential",
    timeout=60.0
)
def network_operation():
    return network_call()
```

## 实际应用场景

### 1. API调用重试

```python
from core.retry import retry_with_condition
from core.logger import Log

@retry_with_condition(
    condition={"status": "success", "data": {"operator": "not_empty", "value": True}},
    max_attempts=5,
    delay=2.0,
    strategy="exponential",
    exceptions=(ConnectionError, TimeoutError)
)
def fetch_user_data(user_id):
    Log.info(f"正在获取用户 {user_id} 的数据")
    
    response = requests.get(f"https://api.example.com/users/{user_id}")
    response.raise_for_status()
    
    data = response.json()
    Log.info(f"API响应: {data}")
    
    return data
```

### 2. 数据库操作重试

```python
from core.retry import retry_on_exception
import pymysql

@retry_on_exception(
    exceptions=(pymysql.Error, ConnectionError),
    max_attempts=3,
    delay=1.0,
    strategy="exponential"
)
def execute_database_query(query, params=None):
    connection = pymysql.connect(
        host='localhost',
        user='username',
        password='password',
        database='testdb'
    )
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            connection.commit()
            return result
    finally:
        connection.close()
```

### 3. 文件操作重试

```python
from core.retry import retry_on_exception
import os

@retry_on_exception(
    exceptions=(FileNotFoundError, PermissionError),
    max_attempts=3,
    delay=0.5
)
def read_file_with_retry(file_path):
    with open(file_path, 'r') as file:
        return file.read()
```

### 4. 异步操作等待

```python
from core.retry import retry_with_condition
import time

@retry_with_condition(
    condition=lambda result: result.get("status") != "completed",
    max_attempts=20,
    delay=1.0
)
def wait_for_async_task(task_id):
    # 检查异步任务状态
    response = requests.get(f"https://api.example.com/tasks/{task_id}")
    return response.json()
```

## 配置选项

### RetryConfig 参数说明

```python
@retry(
    max_attempts=3,           # 最大重试次数
    delay=1.0,               # 基础延迟时间（秒）
    max_delay=60.0,          # 最大延迟时间（秒）
    strategy="exponential",   # 重试策略
    exceptions=(Exception,),  # 需要重试的异常类型
    timeout=None,            # 总体超时时间（秒）
    jitter=True,             # 是否添加随机抖动
    jitter_factor=0.1,       # 抖动因子（0.0-1.0）
    log_retries=True,        # 是否记录重试日志
    log_level="WARNING"      # 重试日志级别
)
```

## 日志集成

重试功能与PTE Framework的日志系统完全集成：

- 自动记录重试次数和原因
- 支持不同日志级别（DEBUG, INFO, WARNING, ERROR）
- 包含LogID追踪
- 记录重试延迟时间

### 日志示例

```
[2024-01-15 10:30:15] [WARNING] [logid:abc123] Function api_call failed on attempt 1/3. Retrying in 1.00s. Exception: ConnectionError: Network timeout
[2024-01-15 10:30:16] [WARNING] [logid:abc123] Function api_call failed on attempt 2/3. Retrying in 2.00s. Exception: ConnectionError: Network timeout
[2024-01-15 10:30:18] [INFO] [logid:abc123] Function api_call succeeded on attempt 3
```

## 最佳实践

### 1. 选择合适的重试策略

- **固定延迟**: 适用于简单的重试场景
- **指数退避**: 适用于网络请求和API调用（推荐）
- **线性退避**: 适用于资源竞争场景
- **随机延迟**: 适用于避免惊群效应
- **斐波那契退避**: 适用于复杂的不稳定场景

### 2. 设置合理的重试次数

```python
# 对于网络请求
@retry(max_attempts=3, delay=1.0)  # 3次重试通常足够

# 对于异步任务等待
@retry_with_condition(condition=..., max_attempts=20, delay=2.0)  # 更多次数用于等待

# 对于关键操作
@retry_until_success(max_attempts=10)  # 重试直到成功
```

### 3. 使用超时控制

```python
# 设置总体超时，避免无限等待
@retry(timeout=60.0, max_attempts=5)
def long_operation():
    pass
```

### 4. 添加抖动避免惊群效应

```python
# 启用抖动，避免多个客户端同时重试
@retry(jitter=True, jitter_factor=0.2)
def api_call():
    pass
```

### 5. 合理使用条件重试

```python
# 只对特定异常重试
@retry_on_exception(exceptions=(ConnectionError, TimeoutError))

# 对特定结果重试
@retry_with_condition(condition=lambda r: r.get("status") == "pending")
```

## 注意事项

1. **避免无限重试**: 始终设置合理的最大重试次数
2. **设置超时**: 对于长时间运行的操作，设置总体超时
3. **选择合适的异常**: 只对可恢复的异常进行重试
4. **监控重试频率**: 过多的重试可能表明系统存在问题
5. **考虑幂等性**: 确保重试操作是幂等的，不会产生副作用

## 总结

PTE Framework的retry功能提供了强大而灵活的重试机制，能够有效处理各种不稳定场景。通过合理使用不同的重试策略和条件，可以显著提高系统的稳定性和可靠性。
