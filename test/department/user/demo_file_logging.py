"""
演示文件日志功能的测试示例
"""
import pytest
from core.logger import Log, generate_logid


class TestFileLoggingDemo:
    """演示文件日志功能的测试类"""
    
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
    
    def test_basic_logging(self):
        """测试基本日志功能"""
        Log.info("这是一条信息日志")
        Log.warning("这是一条警告日志")
        Log.error("这是一条错误日志")
        Log.debug("这是一条调试日志")
        
        # 记录结构化数据
        user_data = {
            "user_id": 12345,
            "username": "testuser",
            "email": "test@example.com"
        }
        Log.info("用户数据", user_data)
    
    def test_api_logging(self):
        """测试 API 调用日志"""
        # 模拟 API 调用
        Log.api_call(
            method="POST",
            url="/api/users",
            status_code=201,
            response_time=0.5,
            request_data={"username": "newuser", "email": "new@example.com"},
            response_data={"user_id": 67890, "status": "created"}
        )
        
        # 模拟另一个 API 调用
        Log.api_call(
            method="GET",
            url="/api/users/67890",
            status_code=200,
            response_time=0.2
        )
    
    def test_assertion_logging(self):
        """测试断言日志"""
        # 成功的断言
        Log.assertion("检查用户ID", True, 12345, 12345)
        Log.assertion("检查用户名", True, "testuser", "testuser")
        
        # 失败的断言
        Log.assertion("检查用户年龄", False, 25, 30)
        Log.assertion("检查用户邮箱", False, "test@example.com", "wrong@example.com")
    
    def test_data_validation(self):
        """测试数据验证日志"""
        # 成功的数据验证
        Log.data_validation("用户名", "testuser", "testuser", True)
        Log.data_validation("邮箱格式", "test@example.com", "test@example.com", True)
        
        # 失败的数据验证
        Log.data_validation("用户年龄", 25, 30, False)
        Log.data_validation("用户状态", "active", "inactive", False)
    
    def test_step_logging(self):
        """测试步骤日志"""
        @Log.step("用户注册步骤")
        def register_user():
            Log.info("开始用户注册流程")
            
            @Log.step("验证用户信息")
            def validate_user_info():
                Log.info("验证用户名和邮箱")
                return True
            
            @Log.step("创建用户账户")
            def create_account():
                Log.info("在数据库中创建用户账户")
                return {"user_id": 99999}
            
            # 执行步骤
            validate_user_info()
            account = create_account()
            Log.info("用户注册完成", account)
            return account
        
        # 执行注册流程
        result = register_user()
        Log.info("注册流程执行完成", result)
    
    def test_error_handling(self):
        """测试错误处理日志"""
        try:
            # 模拟一个可能出错的操作
            Log.info("开始执行可能出错的操作")
            
            # 模拟异常
            raise ValueError("这是一个模拟的错误")
            
        except Exception as e:
            Log.error(f"操作执行失败: {str(e)}")
            Log.info("开始错误恢复流程")
            
            # 模拟错误恢复
            Log.info("错误恢复完成")
    
    def test_performance_logging(self):
        """测试性能相关日志"""
        import time
        
        Log.info("开始性能测试")
        
        # 模拟耗时操作
        start_time = time.time()
        time.sleep(0.1)  # 模拟 100ms 的操作
        end_time = time.time()
        
        duration = end_time - start_time
        Log.info(f"操作耗时: {duration:.3f} 秒")
        
        # 记录性能指标
        performance_data = {
            "operation": "data_processing",
            "duration_ms": duration * 1000,
            "status": "success"
        }
        Log.info("性能指标", performance_data)


def test_standalone_function():
    """独立的测试函数示例"""
    # 设置 LogID
    logid = generate_logid()
    Log.set_logid(logid)
    
    Log.info("开始独立函数测试")
    
    # 执行测试逻辑
    Log.api_call("GET", "/api/health", 200, 0.1)
    Log.assertion("健康检查", True, 200, 200)
    
    Log.info("独立函数测试完成")


if __name__ == "__main__":
    # 可以直接运行此文件进行测试
    pytest.main([__file__, "-v"])
