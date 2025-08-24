# PTE Framework 文件日志功能使用指南

## 概述

PTE Framework 现在支持将日志同时输出到本地文件，方便本地排查和调试。日志文件功能与 Allure 报告功能并行工作，提供完整的日志追踪能力。

## 功能特性

- ✅ **统一配置**: 通过 `config/common.yaml` 统一配置日志行为
- ✅ **日志轮转**: 支持按日期或大小自动轮转日志文件
- ✅ **日志分级**: 支持按日志级别分别输出文件
- ✅ **日志压缩**: 支持自动压缩旧日志文件
- ✅ **日志保留**: 支持设置日志文件保留天数
- ✅ **LogID 追踪**: 所有日志都包含 LogID，支持端到端追踪
- ✅ **格式化输出**: 统一的日志格式，包含时间戳、级别、LogID、调用位置等信息

## 配置说明

### 配置文件位置

日志配置位于 `config/common.yaml` 文件中：

```yaml
# 日志配置
logging:
  # 是否启用文件日志输出
  enable_file_logging: true
  
  # 日志文件配置
  file:
    # 日志文件目录 (相对于项目根目录)
    directory: "logs"
    
    # 日志文件名格式 (支持时间变量)
    # 可用变量: {date}, {time}, {datetime}, {logid}, {level}
    # {date}: YYYYMMDD 格式的日期
    # {time}: HHMMSS 格式的时间
    # {datetime}: YYYYMMDD_HHMMSS 格式的日期时间
    filename_format: "pte_{datetime}_{level}.log"
    
    # 日志级别 (DEBUG, INFO, WARNING, ERROR)
    level: "INFO"
    
    # 日志格式
    format: "[{timestamp}] [{level}] [{logid}] [{caller}] {message}"
    
    # 是否按日期分割日志文件
    rotate_by_date: true
    
    # 是否按日志级别分别输出文件
    separate_by_level: false
    
    # 日志文件保留天数 (0表示不删除)
    retention_days: 30
    
    # 日志文件最大大小 (MB, 0表示不限制)
    max_size_mb: 100
    
    # 是否启用日志压缩
    enable_compression: false
  
  # 控制台输出配置
  console:
    # 是否启用控制台输出
    enabled: true
    
    # 控制台日志级别
    level: "ERROR"
    
    # 控制台日志格式
    format: "[{timestamp}] [{level}] [{logid}] [{caller}] {message}"
  
  # Allure报告配置
  allure:
    # 是否启用Allure日志输出
    enabled: true
    
    # Allure日志级别
    level: "INFO"
    
    # 是否在Allure中显示详细数据
    show_detailed_data: true
```

### 配置参数详解

#### 文件配置 (file)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `directory` | string | "logs" | 日志文件存储目录 |
| `filename_format` | string | "pte_{date}_{level}.log" | 日志文件名格式 |
| `level` | string | "INFO" | 文件日志级别 |
| `format` | string | "[{timestamp}] [{level}] [{logid}] [{caller}] {message}" | 日志格式 |
| `rotate_by_date` | boolean | true | 是否按日期轮转 |
| `separate_by_level` | boolean | false | 是否按级别分别输出 |
| `retention_days` | integer | 30 | 日志保留天数 |
| `max_size_mb` | integer | 100 | 单个文件最大大小(MB) |
| `enable_compression` | boolean | false | 是否启用压缩 |

#### 控制台配置 (console)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enabled` | boolean | true | 是否启用控制台输出 |
| `level` | string | "ERROR" | 控制台日志级别 |
| `format` | string | "[{timestamp}] [{level}] [{logid}] [{caller}] {message}" | 日志格式 |

## 使用方法

### 基本使用

```python
from core.logger import Log

# 设置 LogID (可选，会自动生成)
Log.set_logid("your-custom-logid")

# 记录不同级别的日志
Log.info("这是一条信息日志")
Log.warning("这是一条警告日志")
Log.error("这是一条错误日志")
Log.debug("这是一条调试日志")

# 记录带数据的日志
Log.info("用户登录", {"user_id": 123, "action": "login"})

# 记录 API 调用
Log.api_call("POST", "/api/login", 200, 0.5)

# 记录断言结果
Log.assertion("检查用户ID", True, 123, 123)

# 记录数据验证
Log.data_validation("email", "test@example.com", "test@example.com", True)

# 原始输出 (替代 print)
Log.raw("这是原始输出")
Log.print("这是打印输出")
```

### 在测试中使用

```python
import pytest
from core.logger import Log

class TestUserManagement:
    def test_user_login(self):
        # 开始测试
        Log.start_test("test_user_login")
        
        try:
            # 测试步骤
            Log.info("开始用户登录测试")
            
            # API 调用
            Log.api_call("POST", "/api/login", 200, 0.3)
            
            # 数据验证
            Log.data_validation("token", "expected_token", "actual_token", True)
            
            # 测试完成
            Log.end_test("test_user_login", "PASSED")
            
        except Exception as e:
            Log.error(f"测试失败: {str(e)}")
            Log.end_test("test_user_login", "FAILED")
            raise
```

### 使用装饰器

```python
from core.logger import Log

@Log.step("用户登录步骤")
def login_user(username, password):
    Log.info(f"用户 {username} 开始登录")
    # 登录逻辑
    return {"token": "abc123"}

@Log.step("验证用户信息")
def verify_user_info(user_id):
    Log.info(f"验证用户 {user_id} 的信息")
    # 验证逻辑
    return True
```

## 日志文件管理

### 日志文件位置

默认情况下，日志文件存储在项目根目录的 `logs/` 文件夹中：

```
pte/
├── logs/
│   ├── pte_20250824_094227_all.log   # 09:42:27 执行的日志
│   ├── pte_20250824_094218_all.log   # 09:42:18 执行的日志
│   └── pte_20250824_094206_all.log   # 09:42:06 执行的日志
```

### 日志文件命名

日志文件名格式：`pte_{datetime}_{level}.log`

- `{date}`: 日期，格式为 YYYYMMDD
- `{time}`: 时间，格式为 HHMMSS
- `{datetime}`: 日期时间，格式为 YYYYMMDD_HHMMSS
- `{level}`: 日志级别 (all, debug, info, warning, error)
- `{logid}`: 日志ID (在格式化时替换)

**示例文件名：**
- `pte_20250824_094227_all.log` - 2025年8月24日 09:42:27 的日志
- `pte_20250824_143052_info.log` - 2025年8月24日 14:30:52 的 INFO 级别日志

### 日志轮转

#### 按日期轮转 (默认)

- 每天午夜自动创建新的日志文件
- 旧文件重命名为 `.YYYYMMDD` 后缀
- 超过保留天数的文件自动删除

#### 按大小轮转

- 当文件大小超过 `max_size_mb` 时自动轮转
- 保留最近的 5 个文件

### 日志压缩

启用压缩功能后，轮转的日志文件会自动压缩为 `.gz` 格式：

```
pte_20250824_all.log.20250823.gz
```

## 日志格式

### 标准格式

```
[2025-08-24 09:23:34] [INFO] [ea077c1afae685e47237204fd54e6fac] [test_file.py:25] 日志内容
```

### 格式变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `{timestamp}` | 时间戳 | 2025-08-24 09:23:34 |
| `{level}` | 日志级别 | INFO, WARNING, ERROR, DEBUG |
| `{logid}` | 日志ID | ea077c1afae685e47237204fd54e6fac |
| `{caller}` | 调用位置 | test_file.py:25 |
| `{message}` | 日志消息 | 用户登录成功 |

## 最佳实践

### 1. 合理设置日志级别

- **生产环境**: 设置为 WARNING 或 ERROR
- **测试环境**: 设置为 INFO
- **调试环境**: 设置为 DEBUG

### 2. 使用有意义的 LogID

```python
# 为每个测试用例设置唯一的 LogID
Log.set_logid(f"test_{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
```

### 3. 合理配置日志轮转

```yaml
file:
  # 按日期轮转，适合大多数场景
  rotate_by_date: true
  
  # 保留 30 天的日志
  retention_days: 30
  
  # 启用压缩节省空间
  enable_compression: true
```

### 4. 监控日志文件大小

```yaml
file:
  # 限制单个文件大小为 100MB
  max_size_mb: 100
  
  # 按大小轮转时保留 5 个文件
  # (在代码中硬编码)
```

### 5. 使用结构化数据

```python
# 记录结构化数据，便于分析
Log.info("API 调用完成", {
    "method": "POST",
    "url": "/api/users",
    "status_code": 201,
    "response_time": 0.5,
    "user_id": 12345
})
```

## 故障排除

### 常见问题

1. **日志文件未生成**
   - 检查 `enable_file_logging` 是否设置为 `true`
   - 检查 `logs/` 目录是否存在且有写权限
   - 检查日志级别设置

2. **LogID 显示为 N/A**
   - 确保在记录日志前调用了 `Log.set_logid()`
   - 检查日志处理器配置

3. **日志文件过大**
   - 调整 `max_size_mb` 参数
   - 启用日志压缩
   - 减少日志保留天数

4. **日志格式不正确**
   - 检查 `format` 参数设置
   - 确保格式变量名称正确

### 调试技巧

1. **查看配置**
```python
from config.settings import _config_loader
config = _config_loader.get_common_config()
print(config.get('logging', {}))
```

2. **检查日志文件**
```bash
# 查看最新日志
tail -f logs/pte_$(date +%Y%m%d)_all.log

# 搜索特定 LogID
grep "your-logid" logs/*.log
```

3. **清理旧日志**
```bash
# 手动清理超过 30 天的日志
find logs/ -name "*.log*" -mtime +30 -delete
```

## 示例

### 完整的测试示例

```python
import pytest
from core.logger import Log, generate_logid

class TestUserAPI:
    def setup_method(self):
        # 为每个测试方法设置唯一的 LogID
        self.logid = generate_logid()
        Log.set_logid(self.logid)
        Log.start_test(self._testMethodName)
    
    def teardown_method(self):
        Log.end_test(self._testMethodName, "PASSED")
    
    def test_create_user(self):
        Log.info("开始创建用户测试")
        
        # 准备测试数据
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        Log.info("测试数据准备完成", user_data)
        
        # 执行 API 调用
        Log.api_call("POST", "/api/users", 201, 0.8, user_data)
        
        # 验证结果
        Log.assertion("检查用户创建成功", True, 201, 201)
        Log.data_validation("username", "testuser", "testuser", True)
        
        Log.info("用户创建测试完成")
```

这个示例展示了如何在测试中正确使用文件日志功能，包括设置 LogID、记录测试步骤、API 调用、断言结果等。
