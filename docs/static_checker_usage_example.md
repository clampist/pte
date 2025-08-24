# Checker 静态调用方式使用示例

## 概述

本文档展示了如何使用 `Checker` 类的静态调用方式，这种方式更加简洁和高效。

## 基本用法

### 导入
```python
from core.checker import Checker
```

### 数据验证示例

#### 1. 字段存在性验证
```python
# 验证字段存在
Checker.assert_field_exists(user_data, "name")
Checker.assert_field_exists(user_data, "email")

# 验证字段不存在
Checker.assert_field_not_exists(user_data, "password")
```

#### 2. 字段值验证
```python
# 验证字段值
Checker.assert_field_value(user_data, "name", "John Smith")
Checker.assert_field_value(user_data, "age", 25)
Checker.assert_field_value(user_data, "active", True)
```

#### 3. 数据类型验证
```python
# 验证数据类型
Checker.assert_str_data(user_data["name"])
Checker.assert_int_data(user_data["age"])
Checker.assert_bool_data(user_data["active"])
Checker.assert_dict_data(user_data["config"])
```

#### 4. 相等性验证
```python
# 验证相等
Checker.assert_equal(actual_value, expected_value)
Checker.assert_equal(user_data["name"], "John Smith")

# 验证不相等
Checker.assert_not_equal(new_value, old_value)
```

#### 5. 存在性验证
```python
# 验证非空
Checker.assert_not_none(user_data)
Checker.assert_not_none(self.api_client, "api_client")

# 验证非空集合
Checker.assert_not_empty(user_list)
Checker.assert_length_greater_than(user_name, 0)
```

#### 6. 长度验证
```python
# 验证长度
Checker.assert_length(user_list, 3)
Checker.assert_length(user_name, 10)

# 验证长度范围
Checker.assert_string_length(user_name, 1, 50)
```

#### 7. 对象属性验证
```python
# 验证对象有属性
Checker.assert_has_attr(self.api_client, "host")
Checker.assert_has_attr(self.user_ops, "base_url")

# 验证属性值
Checker.assert_attr_equal(self.api_client, "host", "http://localhost:8080")
```

#### 8. 布尔条件验证
```python
# 验证条件为真
Checker.assert_true(user_data["active"])
Checker.assert_true(len(user_list) > 0)

# 验证条件为假
Checker.assert_false(user_data["deleted"])
```

#### 9. 集合验证
```python
# 验证包含元素
Checker.assert_contains(user_list, target_user)
Checker.assert_dict_contains_key(user_data, "name")
Checker.assert_list_contains(permissions, "admin")

# 验证不包含元素
Checker.assert_not_contains(user_list, deleted_user)
```

## 完整测试示例

```python
import pytest
from core.checker import Checker
from api.client import APIClient
from biz.department.user.operations import UserOperations

class TestUserManagement:
    def setup_method(self):
        self.api_client = APIClient()
        self.user_ops = UserOperations()
        self.test_data = {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "age": 25,
            "active": True
        }
    
    def test_user_data_validation(self):
        """测试用户数据验证"""
        
        # 1. 验证数据结构
        Checker.assert_field_exists(self.test_data, "name")
        Checker.assert_field_exists(self.test_data, "email")
        Checker.assert_field_exists(self.test_data, "age")
        Checker.assert_field_exists(self.test_data, "active")
        
        # 2. 验证数据类型
        Checker.assert_str_data(self.test_data["name"])
        Checker.assert_str_data(self.test_data["email"])
        Checker.assert_int_data(self.test_data["age"])
        Checker.assert_bool_data(self.test_data["active"])
        
        # 3. 验证数据值
        Checker.assert_field_value(self.test_data, "name", "John Smith")
        Checker.assert_field_value(self.test_data, "email", "john.smith@example.com")
        Checker.assert_field_value(self.test_data, "age", 25)
        Checker.assert_field_value(self.test_data, "active", True)
        
        # 4. 验证数据范围
        Checker.assert_in_range(self.test_data["age"], 0, 150)
        Checker.assert_string_length(self.test_data["name"], 1, 100)
        Checker.assert_string_length(self.test_data["email"], 5, 255)
        
        # 5. 验证组件存在性
        Checker.assert_not_none(self.api_client, "api_client")
        Checker.assert_not_none(self.user_ops, "user_ops")
        Checker.assert_has_attr(self.api_client, "host")
        Checker.assert_has_attr(self.user_ops, "base_url")
    
    def test_user_creation_workflow(self):
        """测试用户创建流程"""
        
        # 1. 准备测试数据
        user_data = self.test_data.copy()
        
        # 2. 验证输入数据
        Checker.assert_data_structure(user_data, ["name", "email", "age"])
        Checker.assert_not_empty(user_data["name"])
        Checker.assert_not_empty(user_data["email"])
        
        # 3. 模拟API调用
        # response = self.user_ops.create_user(user_data)
        
        # 4. 验证响应数据
        # Checker.assert_status_code(response, 201)
        # Checker.assert_field_exists(response_data, "user_id")
        # Checker.assert_int_data(response_data["user_id"])
        
        # 5. 验证业务逻辑
        Checker.assert_true(user_data["age"] >= 18, "用户年龄必须大于等于18岁")
        Checker.assert_contains(user_data["email"], "@", "邮箱格式必须包含@")
```

## 优势总结

### 静态调用方式的优势

1. **简洁性**: 无需实例化，直接调用
   ```python
   # 静态调用
   Checker.assert_field_exists(data, "name")
   
   # 实例化调用
   self.checker = Checker()
   self.checker.assert_field_exists(data, "name")
   ```

2. **性能**: 减少对象创建开销
   ```python
   # 静态调用 - 无对象创建
   Checker.assert_equal(a, b)
   
   # 实例化调用 - 需要创建对象
   checker = Checker()
   checker.assert_equal(a, b)
   ```

3. **可读性**: 代码更清晰，意图更明确
   ```python
   # 清晰的意图表达
   Checker.assert_field_value(user, "name", "John")
   Checker.assert_not_none(api_client, "API客户端")
   Checker.assert_has_attr(user_ops, "create_user")
   ```

4. **一致性**: 所有断言方法使用统一的调用方式
   ```python
   # 统一的调用模式
   Checker.assert_<验证类型>(<参数>)
   ```

5. **维护性**: 减少代码重复，易于维护
   ```python
   # 无需在每个测试类中重复实例化
   # 无需管理实例的生命周期
   ```

## 最佳实践

1. **导入方式**: 直接导入 `Checker` 类
   ```python
   from core.checker import Checker
   ```

2. **调用方式**: 使用静态方法调用
   ```python
   Checker.assert_<method_name>(<parameters>)
   ```

3. **错误消息**: 提供有意义的错误消息
   ```python
   Checker.assert_not_none(component, "component_name")
   Checker.assert_field_value(data, "age", 25, "用户年龄验证")
   ```

4. **组合使用**: 可以组合多个断言方法
   ```python
   # 先验证存在性，再验证值
   Checker.assert_field_exists(data, "name")
   Checker.assert_field_value(data, "name", "John")
   ```

这种方式让测试代码更加简洁、高效和易于维护！
