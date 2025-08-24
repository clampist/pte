# PTE Framework - Rerun Functionality Guide

## 概述

PTE Framework 集成了 `pytest-rerunfailures` 插件，提供了强大的测试重试功能。这个功能可以帮助处理不稳定的测试（flaky tests），提高测试套件的可靠性。

## 功能特性

- **自动重试失败测试**：配置失败测试的自动重试次数
- **延迟重试**：在重试之间添加延迟，避免过于频繁的请求
- **标记支持**：通过 pytest 标记控制重试行为
- **与 PTE 框架集成**：与日志、并行测试等功能无缝集成
- **灵活配置**：支持命令行参数和配置文件配置

## 安装依赖

确保已安装 `pytest-rerunfailures`：

```bash
pip install pytest-rerunfailures==12.0
```

## 配置

### 全局配置 (pytest.ini)

```ini
[pytest]
addopts = 
    --reruns=1
    --reruns-delay=1
markers =
    flaky: marks tests as potentially flaky (will be retried more times)
    stable: marks tests as stable (no retry needed)
```

### 命令行配置

```bash
# 基本重试
pte run test/department/user --reruns=3

# 带延迟的重试
pte run test/department/user --reruns=2 --reruns-delay=2

# 禁用重试
pte run test/department/user --no-rerun

# 只重试上次失败的测试
pte run test/department/user --rerun-only-failed
```

## 使用方法

### 1. 基本重试

```bash
# 重试失败测试 3 次
pte run test/department/user --reruns=3

# 重试失败测试 2 次，每次重试间隔 2 秒
pte run test/department/user --reruns=2 --reruns-delay=2
```

### 2. 与并行测试结合

```bash
# 并行执行并重试失败测试
pte run test/department/user --parallel --reruns=2

# 指定并行工作进程数和重试次数
pte run test/department/user --parallel=4 --reruns=3
```

### 3. 只重试失败的测试

```bash
# 只运行上次失败的测试并重试
pte run test/department/user --rerun-only-failed --reruns=2
```

### 4. 与其他 pytest 选项结合

```bash
# 与标记选择结合
pte run test/department/user -m "flaky" --reruns=3

# 与测试选择结合
pte run test/department/user -k "api" --reruns=2

# 与详细输出结合
pte run test/department/user -v --reruns=2 --reruns-delay=1
```

## 测试标记

### 预定义标记

- `@pytest.mark.flaky`：标记为不稳定的测试，建议增加重试次数
- `@pytest.mark.stable`：标记为稳定的测试，通常不需要重试
- `@pytest.mark.api`：API 测试，可能因网络问题失败
- `@pytest.mark.integration`：集成测试，可能因外部依赖失败

### 使用示例

```python
import pytest
from core.logger import Log

class TestExample:
    
    @pytest.mark.flaky
    def test_flaky_operation(self):
        """不稳定的操作，需要重试"""
        # 模拟不稳定的操作
        if random.random() < 0.7:
            Log.warn("操作失败，将重试")
            assert False, "操作失败"
        else:
            Log.info("操作成功")
            assert True
    
    @pytest.mark.stable
    def test_stable_operation(self):
        """稳定的操作，不需要重试"""
        Log.info("稳定操作，应该一致通过")
        assert True
    
    @pytest.mark.api
    def test_api_call(self):
        """API 调用，可能因网络问题失败"""
        # 模拟网络问题
        if random.random() < 0.3:
            Log.warn("API 调用因网络问题失败，将重试")
            raise ConnectionError("网络超时")
        else:
            Log.info("API 调用成功")
            assert True
```

## 最佳实践

### 1. 合理设置重试次数

```bash
# 对于不稳定的测试，使用更多重试次数
pte run test/department/user -m "flaky" --reruns=3

# 对于稳定的测试，使用较少重试次数
pte run test/department/user -m "stable" --reruns=1
```

### 2. 设置适当的延迟

```bash
# 对于 API 测试，使用较长延迟
pte run test/department/user -m "api" --reruns=2 --reruns-delay=3

# 对于快速测试，使用较短延迟
pte run test/department/user --reruns=2 --reruns-delay=0.5
```

### 3. 与 PTE 日志集成

```python
from core.logger import Log

def test_with_logging():
    test_id = f"test_{int(time.time())}"
    Log.info(f"开始测试: {test_id}")
    
    # 模拟不稳定的操作
    if random.random() < 0.5:
        Log.warn(f"测试 {test_id} 失败，将重试")
        assert False, f"测试 {test_id} 失败"
    else:
        Log.info(f"测试 {test_id} 通过")
        assert True
```

### 4. 使用 PTE 重试装饰器

```python
from core.retry import retry

class TestWithRetry:
    
    def test_with_custom_retry(self):
        """使用 PTE 重试装饰器"""
        
        @retry(max_attempts=3, delay=0.1)
        def flaky_operation():
            if random.random() < 0.6:
                raise ValueError("操作失败")
            return "success"
        
        result = flaky_operation()
        assert result == "success"
```

## 配置选项详解

### 命令行选项

| 选项 | 描述 | 示例 |
|------|------|------|
| `--reruns=N` | 重试失败测试 N 次 | `--reruns=3` |
| `--reruns-delay=N` | 重试间隔 N 秒 | `--reruns-delay=2` |
| `--no-rerun` | 禁用重试功能 | `--no-rerun` |
| `--rerun-only-failed` | 只重试上次失败的测试 | `--rerun-only-failed` |

### 配置文件选项

在 `pytest.ini` 中设置默认值：

```ini
[pytest]
addopts = 
    --reruns=1              # 默认重试 1 次
    --reruns-delay=1        # 默认延迟 1 秒
```

## 输出示例

### 成功重试

```
[INFO] Rerun configuration: 2 retries
[INFO] Rerun delay: 1 seconds
[COMMAND] Executing: pytest test/department/user --reruns=2 --reruns-delay=1 -v
============================= test session starts ==============================
test_rerun_functionality.py::TestRerunBasicFunctionality::test_sometimes_fails FAILED [ 33%]
test_rerun_functionality.py::TestRerunBasicFunctionality::test_sometimes_fails RERUN [ 33%]
test_rerun_functionality.py::TestRerunBasicFunctionality::test_sometimes_fails PASSED [ 33%]
============================== 1 passed in 2.34s ==============================
[SUCCESS] Tests completed successfully
```

### 重试后仍然失败

```
[INFO] Rerun configuration: 2 retries
[COMMAND] Executing: pytest test/department/user --reruns=2 -v
============================= test session starts ==============================
test_rerun_functionality.py::TestRerunBasicFunctionality::test_always_fails FAILED [ 33%]
test_rerun_functionality.py::TestRerunBasicFunctionality::test_always_fails RERUN [ 33%]
test_rerun_functionality.py::TestRerunBasicFunctionality::test_always_fails FAILED [ 33%]
test_rerun_functionality.py::TestRerunBasicFunctionality::test_always_fails RERUN [ 33%]
test_rerun_functionality.py::TestRerunBasicFunctionality::test_always_fails FAILED [ 33%]
============================== 1 failed in 3.45s ==============================
[ERROR] Tests failed with exit code: 1
```

## 故障排除

### 常见问题

1. **重试不生效**
   - 检查是否正确安装了 `pytest-rerunfailures`
   - 确认命令行参数格式正确
   - 检查 pytest.ini 配置

2. **重试次数过多**
   - 调整 `--reruns` 参数
   - 考虑使用 `--no-rerun` 禁用重试

3. **延迟时间过长**
   - 调整 `--reruns-delay` 参数
   - 对于快速测试，可以使用较小的延迟值

### 调试技巧

```bash
# 启用详细输出查看重试过程
pte run test/department/user --reruns=2 -v -s

# 查看重试统计信息
pte run test/department/user --reruns=2 --durations=10
```

## 性能考虑

### 重试对性能的影响

- **执行时间**：重试会增加总执行时间
- **资源消耗**：多次执行可能消耗更多资源
- **测试稳定性**：提高测试套件的整体稳定性

### 优化建议

1. **合理设置重试次数**：避免过度重试
2. **使用适当的延迟**：避免过于频繁的重试
3. **标记不稳定测试**：只对需要的测试启用重试
4. **监控重试统计**：定期分析重试模式

## 总结

PTE Framework 的 rerun 功能提供了强大的测试重试能力，可以有效处理不稳定的测试。通过合理配置和使用，可以显著提高测试套件的可靠性和稳定性。

记住：
- 重试不是解决测试问题的根本方法
- 应该优先修复不稳定的测试
- 重试功能主要用于处理临时的、不可控的失败
- 合理使用重试功能，避免过度依赖
