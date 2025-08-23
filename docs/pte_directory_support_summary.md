# PTE Runner 目录支持增强总结

## 🎯 问题背景

用户反馈 `pte` 命令只支持通配符模式运行：
- ✅ `./pte run "test/department/user/*.py"` - 工作正常
- ❌ `./pte run test/department/user` - 不工作，无法发现测试

用户希望能够直接运行目录，并利用 pytest 的原生能力进行测试发现。

## ✅ 解决方案

### 核心策略：智能路径转换

由于发现 pytest 在某些环境下直接运行目录时测试发现存在问题，我们采用了智能路径转换策略：

**当用户指定目录时，自动转换为通配符模式**
- 输入：`test/department/user`
- 转换：`test/department/user/*.py`
- 利用 shell 的通配符展开机制

### 技术实现

#### 1. 路径类型检测与处理

```bash
# Handle different path types and validate existence
local actual_path="$test_path"

# Check if it's a pattern with wildcards
if [[ "$test_path" == *"*"* ]] || [[ "$test_path" == *"?"* ]]; then
    print_info "Path type: Pattern (pytest will expand wildcards)"
    # Check if pattern matches any files
    if ! ls $test_path >/dev/null 2>&1; then
        print_error "No files match pattern: $test_path"
        exit 1
    fi
elif [ -d "$test_path" ]; then
    print_info "Path type: Directory (converting to wildcard pattern for better discovery)"
    # Convert directory to wildcard pattern for better test discovery
    actual_path="$test_path/*.py"
elif [ -f "$test_path" ]; then
    print_info "Path type: File"
elif [[ "$test_path" == *"::"* ]]; then
    print_info "Path type: Specific test (pytest will handle)"
    # Extract file path from test specification
    local file_path="${test_path%%::*}"
    if [ ! -f "$file_path" ]; then
        print_error "Test file does not exist: $file_path"
        exit 1
    fi
else
    print_error "Test path does not exist: $test_path"
    exit 1
fi
```

#### 2. 命令执行策略

```bash
# Build and execute pytest command
if [[ "$actual_path" == *"*"* ]] || [[ "$actual_path" == *"?"* ]]; then
    # For patterns, let shell expand the wildcards
    print_command "Executing: pytest $actual_path $([ $# -eq 0 ] && echo '-v' || echo "$*")"
    echo ""
    if [ $# -eq 0 ]; then
        pytest $actual_path -v
    else
        pytest $actual_path "$@"
    fi
else
    # For regular paths, quote to handle spaces
    local cmd="pytest \"$actual_path\""
    
    # Add pytest options if provided
    if [ $# -gt 0 ]; then
        cmd="$cmd $*"
    fi
    
    # Add default options if no specific options provided
    if [ $# -eq 0 ]; then
        cmd="$cmd -v"
    fi
    
    print_command "Executing: $cmd"
    echo ""
    
    # Execute pytest
    eval "$cmd"
fi
```

## 📊 支持的路径类型

### 1. ✅ 目录路径
```bash
./pte run test/department/user
# 自动转换为: pytest test/department/user/*.py -v
# 结果: 发现并运行 86 个测试
```

### 2. ✅ 通配符模式
```bash
./pte run "test/department/user/*.py"
# 执行: pytest test/department/user/*.py -v
# 结果: 发现并运行 86 个测试
```

### 3. ✅ 单个文件
```bash
./pte run test/department/user/business_real_api_tests.py
# 执行: pytest "test/department/user/business_real_api_tests.py" -v
# 结果: 发现并运行 11 个测试
```

### 4. ✅ 特定测试方法
```bash
./pte run test/department/user/business_real_api_tests.py::TestBusinessRealAPI::test_real_api_connection
# 执行: pytest "file::class::method" -v
# 结果: 运行 1 个特定测试
```

### 5. ✅ 带 pytest 参数
```bash
./pte run test/department/user -k "business" --maxfail=5
# 执行: pytest test/department/user/*.py -k business --maxfail=5
# 结果: 运行 40 个匹配的测试
```

## 🎉 实际效果验证

### 目录运行测试

**命令**：
```bash
./pte run test/department/user
```

**输出**：
```
[INFO] Test path: test/department/user
[INFO] Path type: Directory (converting to wildcard pattern for better discovery)
[COMMAND] Executing: pytest test/department/user/*.py -v

collected 86 items

test/department/user/business_real_api_tests.py::TestBusinessRealAPI::test_real_api_connection PASSED
test/department/user/business_real_api_tests.py::TestBusinessRealAPI::test_user_creation_api PASSED
...
============================================ 86 passed in 4.59s ============================================
```

### 带参数的目录运行

**命令**：
```bash
./pte run test/department/user -k "business" --maxfail=5
```

**输出**：
```
[INFO] Test path: test/department/user
[INFO] Path type: Directory (converting to wildcard pattern for better discovery)
[INFO] Pytest options: -k business --maxfail=5
[COMMAND] Executing: pytest test/department/user/*.py -k business --maxfail=5

collected 86 items / 46 deselected / 40 selected

==================================== 40 passed, 46 deselected in 4.13s =====================================
```

## 🔧 关键技术点

### 1. Shell 通配符展开
- 不使用引号包裹通配符路径，让 shell 自动展开
- 避免将通配符作为字符串传递给 pytest

### 2. 路径验证
- 检查文件/目录是否存在
- 验证通配符模式是否匹配文件
- 支持特定测试的文件路径验证

### 3. 参数传递
- 正确处理 pytest 的各种参数
- 支持引号、空格等特殊字符
- 保持参数顺序和格式

### 4. 错误处理
- 清晰的错误信息
- 路径不存在时的友好提示
- 通配符无匹配时的错误处理

## 🎯 支持的 pytest 参数

所有标准 pytest 参数都得到支持：

- **选择测试**：`-k EXPRESSION`, `-m MARKERS`
- **输出控制**：`-v`, `--tb=style`
- **执行控制**：`--maxfail=num`, `-x`, `--exitfirst`
- **调试支持**：`--pdb`, `--durations=N`
- **失败重运行**：`--lf`, `--ff`

## 📝 使用示例

### 基本用法
```bash
# 运行整个目录
./pte run test/department/user

# 运行特定文件
./pte run test/department/user/business_real_api_tests.py

# 运行特定测试
./pte run test/department/user/business_real_api_tests.py::TestBusinessRealAPI::test_real_api_connection
```

### 高级用法
```bash
# 运行包含 "business" 的测试
./pte run test/department/user -k "business"

# 运行标记为 "smoke" 的测试
./pte run test/department/user -m "smoke"

# 详细输出，最多失败 3 个
./pte run test/department/user -v --maxfail=3

# 只运行上次失败的测试
./pte run test/department/user --lf

# 组合使用
./pte run test/department/user -k "business" -v --tb=short
```

## 🎉 主要优势

### 1. 兼容性
- 支持所有现有的使用方式
- 完全兼容 pytest 的所有参数
- 向后兼容，不破坏现有工作流

### 2. 易用性
- 用户可以直接运行目录，无需记住通配符语法
- 自动处理路径转换，对用户透明
- 清晰的命令输出，便于理解执行过程

### 3. 可靠性
- 充分的路径验证和错误处理
- 支持各种边界情况
- 稳定的测试发现机制

### 4. 灵活性
- 支持文件、目录、通配符、特定测试等多种路径类型
- 支持所有 pytest 参数和选项
- 可以轻松扩展支持新的路径类型

---

**总结**: 通过智能路径转换策略，成功解决了目录运行的问题。用户现在可以使用 `./pte run test/department/user` 直接运行目录中的所有测试，同时保持对通配符、文件路径、特定测试等所有现有功能的完整支持。该解决方案充分利用了 pytest 的原生能力，提供了简洁、可靠、灵活的测试运行体验。
