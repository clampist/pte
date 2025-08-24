# PTE Framework 并行测试指南

## 概述

PTE Framework 现在支持使用 pytest-xdist 进行并行测试执行，可以显著提高测试执行速度。本指南将介绍如何使用并行测试功能。

## 安装依赖

确保已安装 pytest-xdist：

```bash
pip install pytest-xdist
```

或者在项目根目录运行：

```bash
pyenv activate pte
pip install -r requirements.txt
```

## 基本用法

### 1. 自动检测 CPU 核心数运行并行测试

```bash
# 运行所有测试，自动使用所有可用 CPU 核心
pte all --parallel

# 运行特定测试文件，自动使用所有可用 CPU 核心
pte run test/department/user/demo_parallel_testing.py --parallel

# 运行 demo 测试，自动使用所有可用 CPU 核心
pte demo --parallel
```

### 2. 指定并行工作进程数

```bash
# 使用 4 个并行工作进程
pte all --parallel=4

# 使用 2 个并行工作进程运行特定测试
pte run test/department/user/demo_parallel_testing.py --parallel=2

# 使用 8 个并行工作进程运行 business 测试
pte business --parallel=8
```

### 3. 禁用并行执行

```bash
# 明确禁用并行执行
pte all --no-parallel

# 或者直接不使用 --parallel 参数（默认行为）
pte all
```

## 测试标记

### 1. @pytest.mark.parallel

标记测试为并行安全：

```python
import pytest
from core.logger import Log

@pytest.mark.parallel
def test_api_call_safe():
    """API 调用可以安全地并行执行"""
    Log.info("Running API call test")
    # 测试逻辑
    assert True
```

### 2. @pytest.mark.no_parallel

标记测试不应该并行执行：

```python
import pytest
from core.logger import Log

@pytest.mark.no_parallel
def test_database_operation():
    """数据库操作不应该并行执行"""
    Log.info("Running database operation test")
    # 数据库操作逻辑
    assert True
```

### 3. 无标记测试

没有标记的测试会根据 pytest-xdist 的自动检测机制决定是否并行执行。

## 最佳实践

### 1. 何时使用并行测试

**适合并行执行的测试：**
- API 调用测试
- 独立的计算测试
- 无状态的功能测试
- 文件读取测试（只读）

**不适合并行执行的测试：**
- 数据库写入操作
- 共享资源访问
- 文件写入操作
- 需要特定执行顺序的测试

### 2. 性能优化建议

```bash
# 对于 CPU 密集型测试，使用 CPU 核心数
pte all --parallel=$(nproc)

# 对于 I/O 密集型测试，可以使用更多工作进程
pte all --parallel=$(($(nproc) * 2))

# 对于内存密集型测试，减少工作进程数
pte all --parallel=$(($(nproc) / 2))
```

### 3. 调试并行测试

```bash
# 使用详细输出模式
pte run test/department/user/demo_parallel_testing.py --parallel=2 -v

# 使用更详细的输出
pte run test/department/user/demo_parallel_testing.py --parallel=2 -vv

# 显示测试持续时间
pte run test/department/user/demo_parallel_testing.py --parallel=2 --durations=10
```

## 示例

### 1. 运行并行测试演示

```bash
# 运行并行测试演示
pte run test/department/user/demo_parallel_testing.py --parallel=4
```

### 2. 比较并行和串行执行时间

```bash
# 串行执行
time pte run test/department/user/demo_parallel_testing.py

# 并行执行
time pte run test/department/user/demo_parallel_testing.py --parallel=4
```

### 3. 选择性并行执行

```bash
# 只运行标记为并行的测试
pte run test/department/user/demo_parallel_testing.py --parallel=4 -m "parallel"

# 排除标记为不并行的测试
pte run test/department/user/demo_parallel_testing.py --parallel=4 -m "not no_parallel"
```

## 故障排除

### 1. 常见问题

**问题：测试失败且输出混乱**
- 解决方案：检查测试是否有共享状态，添加 `@pytest.mark.no_parallel` 标记

**问题：并行执行没有性能提升**
- 解决方案：检查测试是否真正独立，确保没有 I/O 瓶颈

**问题：内存使用过高**
- 解决方案：减少并行工作进程数

### 2. 调试技巧

```bash
# 使用单个工作进程调试
pte run test/department/user/demo_parallel_testing.py --parallel=1

# 使用 pytest 的调试选项
pte run test/department/user/demo_parallel_testing.py --parallel=2 --tb=long

# 检查测试收集
pte run test/department/user/demo_parallel_testing.py --parallel=2 --collect-only
```

## 配置选项

### pytest.ini 配置

```ini
[pytest]
markers =
    parallel: marks tests as safe for parallel execution
    no_parallel: marks tests that should not run in parallel
```

### 环境变量

```bash
# 设置默认并行工作进程数
export PTE_PARALLEL_WORKERS=4

# 禁用并行执行
export PTE_NO_PARALLEL=1
```

## 性能监控

### 1. 执行时间对比

```bash
# 记录串行执行时间
time pte all > serial.log 2>&1

# 记录并行执行时间
time pte all --parallel=4 > parallel.log 2>&1

# 比较结果
echo "Serial execution time:"
grep "real" serial.log
echo "Parallel execution time:"
grep "real" parallel.log
```

### 2. 资源使用监控

```bash
# 监控 CPU 使用率
top -p $(pgrep -f "pytest.*-n")

# 监控内存使用
ps aux | grep pytest
```

## 总结

并行测试可以显著提高测试执行速度，但需要谨慎使用。遵循以下原则：

1. **正确标记测试**：使用适当的标记指示测试的并行安全性
2. **合理设置工作进程数**：根据系统资源和测试特性调整
3. **监控性能**：定期比较并行和串行执行的性能
4. **调试问题**：遇到问题时使用调试选项进行排查

通过合理使用并行测试功能，可以大大提高 PTE Framework 的测试效率。
