"""
演示 LogID attachment 功能的测试
"""
import pytest
from core.logger import Log, generate_logid


class TestLogIDAttachment:
    """测试 LogID attachment 功能"""
    
    def setup_method(self, method):
        """每个测试方法开始前的设置"""
        # 为每个测试方法生成唯一的 LogID
        self.logid = generate_logid()
        Log.set_logid(self.logid)
        Log.start_test(method.__name__)
        Log.info(f"开始测试方法: {method.__name__}")
    
    def teardown_method(self, method):
        """每个测试方法结束后的清理"""
        Log.info(f"结束测试方法: {method.__name__}")
        Log.end_test(method.__name__, "PASSED")
    
    def test_logid_attachment_demo(self):
        """演示 LogID attachment 功能"""
        Log.info("这是一个演示 LogID attachment 功能的测试")
        
        # 记录一些测试步骤
        Log.info("步骤1: 准备测试数据")
        test_data = {
            "user_id": 12345,
            "username": "testuser",
            "email": "test@example.com"
        }
        Log.info("测试数据准备完成", test_data)
        
        # 模拟 API 调用
        Log.api_call(
            method="POST",
            url="/api/users",
            status_code=201,
            response_time=0.5,
            request_data=test_data,
            response_data={"user_id": 12345, "status": "created"}
        )
        
        # 数据验证
        Log.data_validation("user_id", 12345, 12345, True)
        Log.data_validation("username", "testuser", "testuser", True)
        
        # 断言
        Log.assertion("检查用户创建成功", True, 201, 201)
        
        Log.info("LogID attachment 功能演示完成")
    
    def test_multiple_logid_attachments(self):
        """测试多个 LogID attachment"""
        Log.info("这是第二个测试，用于验证多个 LogID attachment")
        
        # 使用装饰器步骤
        @Log.step("用户注册步骤")
        def register_user():
            Log.info("开始用户注册流程")
            return {"user_id": 67890, "status": "registered"}
        
        # 执行步骤
        result = register_user()
        Log.info("用户注册完成", result)
        
        Log.info("多个 LogID attachment 测试完成")


def test_standalone_logid_attachment():
    """独立的 LogID attachment 测试"""
    # 设置 LogID
    logid = generate_logid()
    Log.set_logid(logid)
    
    # 开始测试
    Log.start_test("test_standalone_logid_attachment")
    
    Log.info("开始独立 LogID attachment 测试")
    
    # 执行测试逻辑
    Log.api_call("GET", "/api/health", 200, 0.1)
    Log.assertion("健康检查", True, 200, 200)
    
    Log.info("独立 LogID attachment 测试完成")
    
    # 结束测试
    Log.end_test("test_standalone_logid_attachment", "PASSED")


if __name__ == "__main__":
    # 可以直接运行此文件进行测试
    pytest.main([__file__, "-v"])
