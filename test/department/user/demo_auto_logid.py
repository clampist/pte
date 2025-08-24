"""
演示自动 LogID 功能的测试
"""
import pytest
from core.logger import Log


def test_auto_logid_simple():
    """测试自动 LogID 功能 - 简单日志"""
    # 无需手动设置 LogID，fixture 会自动处理
    Log.info("这是一条自动 LogID 的测试日志")
    Log.warning("这是一条警告日志")
    Log.error("这是一条错误日志")
    
    # 可以获取当前 LogID
    current_logid = Log.get_logid()
    print(f"当前测试的 LogID: {current_logid}")


def test_auto_logid_with_data():
    """测试自动 LogID 功能 - 带数据的日志"""
    # 记录带数据的日志
    test_data = {
        "user_id": 12345,
        "username": "testuser",
        "email": "test@example.com"
    }
    Log.info("用户数据", test_data)
    
    # API 调用日志
    Log.api_call(
        method="POST",
        url="/api/users",
        status_code=201,
        response_time=0.5,
        request_data=test_data,
        response_data={"user_id": 12345, "status": "created"}
    )
    
    # 断言日志
    Log.assertion("检查用户创建成功", True, 201, 201)
    
    # 数据验证日志
    Log.data_validation("user_id", 12345, 12345, True)
    
    current_logid = Log.get_logid()
    print(f"当前测试的 LogID: {current_logid}")


class TestAutoLogIDClass:
    """测试类中的自动 LogID 功能"""
    
    def test_class_method_1(self):
        """类方法测试 1"""
        Log.info("类方法测试 1 的日志")
        Log.warning("类方法测试 1 的警告")
        
        current_logid = Log.get_logid()
        print(f"类方法测试 1 的 LogID: {current_logid}")
    
    def test_class_method_2(self):
        """类方法测试 2"""
        Log.info("类方法测试 2 的日志")
        Log.error("类方法测试 2 的错误")
        
        current_logid = Log.get_logid()
        print(f"类方法测试 2 的 LogID: {current_logid}")


def test_auto_logid_direct_usage():
    """测试直接使用日志方法，无需任何设置"""
    # 直接使用，无需任何 LogID 设置
    Log.info("直接使用的日志")
    Log.warning("直接使用的警告")
    Log.error("直接使用的错误")
    
    # 记录结构化数据
    Log.info("结构化数据", {"key": "value", "number": 123})
    
    # API 调用
    Log.api_call("GET", "/api/health", 200, 0.1)
    
    current_logid = Log.get_logid()
    print(f"直接使用测试的 LogID: {current_logid}")


def test_logid_uniqueness():
    """测试 LogID 唯一性"""
    # 验证 LogID 是否正确设置
    current_logid = Log.get_logid()
    print(f"当前 LogID: {current_logid}")
    
    # 验证 LogID 不为空
    assert current_logid is not None, "LogID 应该不为空"
    assert len(current_logid) > 0, "LogID 应该有内容"
    
    # 记录一些日志
    Log.info("验证 LogID 唯一性的测试")
    Log.warning("这是一个警告")


if __name__ == "__main__":
    # 可以直接运行此文件进行测试
    pytest.main([__file__, "-v"])
