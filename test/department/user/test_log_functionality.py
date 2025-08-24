"""
PTE 日志功能综合测试
整合了 LogID 生成、日志记录、附件功能等所有日志相关的测试
"""
import pytest
import allure
import os
from config.settings import TestEnvironment
from api.client import APIClient
from biz.department.user.operations import UserOperations
from data.department.user.test_data import UserTestData
from core.logger import Log, generate_logid
from core.checker import Checker


@allure.epic("PTE Framework")
@allure.feature("Log Functionality")
class TestLogFunctionality:
    """PTE 日志功能综合测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        os.environ['TEST_IDC'] = 'local_test'
        os.environ['TEST_ENV'] = 'local'
        
        # Initialize components
        self.api_client = APIClient()
        self.user_ops = UserOperations()
        self.test_data = UserTestData()
    
    @allure.story("Basic Log Functions")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_basic_log_functions(self):
        """测试基础日志功能 - info/warning/error/debug"""
        # 第1步：设置 LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # 第2步：开始测试
        Log.start_test("test_basic_log_functions")
        
        try:
            # 测试基础日志功能
            Log.info("这是一条信息日志")
            Log.warning("这是一条警告日志")
            Log.error("这是一条错误日志")
            Log.debug("这是一条调试日志")
            
            # 测试带数据的日志
            test_data = {
                "user_id": 12345,
                "username": "testuser",
                "email": "test@example.com"
            }
            Log.info("用户数据", test_data)
            
            # 测试结构化数据
            Log.info("结构化数据", {"key": "value", "number": 123})
            
            Log.info("基础日志功能测试完成")
            
        except Exception as e:
            Log.error(f"基础日志功能测试失败: {str(e)}")
            Log.end_test("test_basic_log_functions", "FAILED")
            raise
        else:
            # 最后一步：结束测试
            Log.end_test("test_basic_log_functions", "PASSED")
    
    @allure.story("LogID Management")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logid_management(self):
        """测试 LogID 管理功能"""
        # 第1步：设置 LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # 第2步：开始测试
        Log.start_test("test_logid_management")
        
        try:
            # 测试 LogID 生成和获取
            original_logid = Log.get_logid()
            Log.info(f"当前 LogID: {original_logid}")
            
            # 验证 LogID 不为空
            Checker.assert_not_none(original_logid, "LogID")
            Checker.assert_length_greater_than(original_logid, 0, "LogID")
            
            # 测试 LogID 一致性
            current_logid = Log.get_logid()
            Checker.assert_equal(original_logid, current_logid, "LogID")
            
            # 测试新 LogID 生成
            new_logid = generate_logid()
            Checker.assert_not_equal(new_logid, original_logid, "LogID")
            
            Log.info("LogID 管理功能测试完成")
            
        except Exception as e:
            Log.error(f"LogID 管理功能测试失败: {str(e)}")
            Log.end_test("test_logid_management", "FAILED")
            raise
        else:
            # 最后一步：结束测试
            Log.end_test("test_logid_management", "PASSED")
    
    @allure.story("API Call Logging")
    @allure.severity(allure.severity_level.NORMAL)
    def test_api_call_logging(self):
        """测试 API 调用日志功能"""
        # 第1步：设置 LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # 第2步：开始测试
        Log.start_test("test_api_call_logging")
        
        try:
            # 测试简单 API 调用日志
            Log.api_call("GET", "/api/health", 200, 0.1)
            
            # 测试完整 API 调用日志
            test_data = {
                "user_id": 12345,
                "username": "testuser",
                "email": "test@example.com"
            }
            Log.api_call(
                method="POST",
                url="/api/users",
                status_code=201,
                response_time=0.5,
                request_data=test_data,
                response_data={"user_id": 12345, "status": "created"}
            )
            
            # 测试不同状态码的 API 调用
            Log.api_call("GET", "/api/users/999", 404, 0.2)
            Log.api_call("PUT", "/api/users/123", 500, 1.0)
            
            Log.info("API 调用日志功能测试完成")
            
        except Exception as e:
            Log.error(f"API 调用日志功能测试失败: {str(e)}")
            Log.end_test("test_api_call_logging", "FAILED")
            raise
        else:
            # 最后一步：结束测试
            Log.end_test("test_api_call_logging", "PASSED")
    
    @allure.story("Data Validation Logging")
    @allure.severity(allure.severity_level.NORMAL)
    def test_data_validation_logging(self):
        """测试数据验证日志功能"""
        # 第1步：设置 LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # 第2步：开始测试
        Log.start_test("test_data_validation_logging")
        
        try:
            # 测试成功的数据验证
            Log.data_validation("用户名", "testuser", "testuser", True)
            Log.data_validation("用户ID", 12345, 12345, True)
            Log.data_validation("邮箱格式", "test@example.com", "test@example.com", True)
            
            # 测试失败的数据验证
            Log.data_validation("用户年龄", 25, 30, False)
            Log.data_validation("用户状态", "active", "inactive", False)
            Log.data_validation("权限级别", "admin", "user", False)
            
            # 测试不同数据类型的验证
            Log.data_validation("布尔值", True, True, True)
            Log.data_validation("浮点数", 3.14, 3.14, True)
            Log.data_validation("列表长度", 3, 5, False)
            
            Log.info("数据验证日志功能测试完成")
            
        except Exception as e:
            Log.error(f"数据验证日志功能测试失败: {str(e)}")
            Log.end_test("test_data_validation_logging", "FAILED")
            raise
        else:
            # 最后一步：结束测试
            Log.end_test("test_data_validation_logging", "PASSED")
    
    @allure.story("Assertion Logging")
    @allure.severity(allure.severity_level.NORMAL)
    def test_assertion_logging(self):
        """测试断言日志功能"""
        # 第1步：设置 LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # 第2步：开始测试
        Log.start_test("test_assertion_logging")
        
        try:
            # 测试成功的断言
            Log.assertion("检查用户ID", True, 12345, 12345)
            Log.assertion("检查用户名", True, "testuser", "testuser")
            Log.assertion("检查状态码", True, 200, 200)
            
            # 测试失败的断言
            Log.assertion("检查用户年龄", False, 25, 30)
            Log.assertion("检查用户邮箱", False, "test@example.com", "wrong@example.com")
            Log.assertion("检查响应时间", False, 0.5, 1.0)
            
            # 测试不同类型的断言
            Log.assertion("布尔断言", True, True, True)
            Log.assertion("字符串断言", True, "success", "success")
            Log.assertion("数值断言", True, 100, 100)
            
            Log.info("断言日志功能测试完成")
            
        except Exception as e:
            Log.error(f"断言日志功能测试失败: {str(e)}")
            Log.end_test("test_assertion_logging", "FAILED")
            raise
        else:
            # 最后一步：结束测试
            Log.end_test("test_assertion_logging", "PASSED")
    
    @allure.story("Step Decorator")
    @allure.severity(allure.severity_level.NORMAL)
    def test_step_decorator(self):
        """测试步骤装饰器功能"""
        # 第1步：设置 LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # 第2步：开始测试
        Log.start_test("test_step_decorator")
        
        try:
            # 测试步骤装饰器
            @Log.step("用户注册步骤")
            def register_user():
                Log.info("开始用户注册流程")
                return {"user_id": 67890, "status": "registered"}
            
            @Log.step("用户验证步骤")
            def validate_user():
                Log.info("验证用户信息")
                return {"valid": True}
            
            @Log.step("用户激活步骤")
            def activate_user():
                Log.info("激活用户账户")
                return {"activated": True}
            
            # 执行步骤
            register_result = register_user()
            Log.info("用户注册完成", register_result)
            
            validate_result = validate_user()
            Log.info("用户验证完成", validate_result)
            
            activate_result = activate_user()
            Log.info("用户激活完成", activate_result)
            
            Log.info("步骤装饰器功能测试完成")
            
        except Exception as e:
            Log.error(f"步骤装饰器功能测试失败: {str(e)}")
            Log.end_test("test_step_decorator", "FAILED")
            raise
        else:
            # 最后一步：结束测试
            Log.end_test("test_step_decorator", "PASSED")
    
    @allure.story("LogID Attachment")
    @allure.severity(allure.severity_level.NORMAL)
    def test_logid_attachment(self):
        """测试 LogID 附件功能"""
        # 第1步：设置 LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # 第2步：开始测试
        Log.start_test("test_logid_attachment")
        
        try:
            Log.info("开始 LogID 附件功能测试")
            
            # 记录测试步骤
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
            
            Log.info("LogID 附件功能测试完成")
            
        except Exception as e:
            Log.error(f"LogID 附件功能测试失败: {str(e)}")
            Log.end_test("test_logid_attachment", "FAILED")
            raise
        else:
            # 最后一步：结束测试
            Log.end_test("test_logid_attachment", "PASSED")
    
    @allure.story("Headers with LogID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_headers_with_logid(self):
        """测试带 LogID 的请求头功能"""
        # 第1步：设置 LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # 第2步：开始测试
        Log.start_test("test_headers_with_logid")
        
        try:
            Log.info("测试带 LogID 的请求头功能")
            
            # 获取带 LogID 的请求头
            headers = Log.get_headers_with_logid({
                'Authorization': 'Bearer token123',
                'Content-Type': 'application/json',
                'Custom-Header': 'value'
            })
            
            Log.info("请求头生成完成", {
                "headers": headers,
                "logid": Log.get_logid()
            })
            
            # 验证 LogID 在请求头中
            Checker.assert_contains(headers, 'logId')
            Checker.assert_equal(headers['logId'], Log.get_logid(), "logId in headers")
            
            # 验证其他请求头保持不变
            Checker.assert_equal(headers['Authorization'], 'Bearer token123', "Authorization header")
            Checker.assert_equal(headers['Content-Type'], 'application/json', "Content-Type header")
            Checker.assert_equal(headers['Custom-Header'], 'value', "Custom-Header")
            
            Log.info("带 LogID 的请求头功能测试完成")
            
        except Exception as e:
            Log.error(f"带 LogID 的请求头功能测试失败: {str(e)}")
            Log.end_test("test_headers_with_logid", "FAILED")
            raise
        else:
            # 最后一步：结束测试
            Log.end_test("test_headers_with_logid", "PASSED")
    
    @allure.story("Integration with Framework Components")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_framework_integration(self):
        """测试与框架组件的集成"""
        # 第1步：设置 LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # 第2步：开始测试
        Log.start_test("test_framework_integration")
        
        try:
            Log.info("测试与框架组件的集成")
            
            # 测试与 API 客户端的集成
            Log.info("测试 API 客户端集成")
            response = self.api_client.get("/api/users")
            Log.info("API 调用完成", {
                "status_code": response.status_code,
                "url": "/api/users"
            })
            
            # 测试与业务操作的集成
            Log.info("测试业务操作集成")
            result = self.user_ops.get_all_users()
            Log.info("业务操作完成", {
                "result_keys": list(result.keys()) if isinstance(result, dict) else "Not a dict"
            })
            
            # 测试与测试数据的集成
            Log.info("测试数据集成")
            user_data = self.test_data.VALID_USER_1
            Log.info("测试数据获取完成", {"user_data": user_data})
            
            # 验证数据
            Checker.assert_field_value(user_data, "name", "John Smith")
            Checker.assert_field_value(user_data, "email", "john.smith@example.com")
            Checker.assert_field_value(user_data, "age", 25)
            
            Log.info("框架组件集成测试完成")
            
        except Exception as e:
            Log.error(f"框架组件集成测试失败: {str(e)}")
            Log.end_test("test_framework_integration", "FAILED")
            raise
        else:
            # 最后一步：结束测试
            Log.end_test("test_framework_integration", "PASSED")


# 独立的测试函数
def test_standalone_log_functionality():
    """独立的日志功能测试"""
    # 第1步：设置 LogID
    logid = generate_logid()
    Log.set_logid(logid)
    
    # 第2步：开始测试
    Log.start_test("test_standalone_log_functionality")
    
    try:
        Log.info("开始独立日志功能测试")
        
        # 测试基础日志
        Log.info("独立测试中的信息日志")
        Log.warning("独立测试中的警告日志")
        
        # 测试 API 调用
        Log.api_call("GET", "/api/health", 200, 0.1)
        
        # 测试断言
        Log.assertion("健康检查", True, 200, 200)
        
        # 测试数据验证
        Log.data_validation("健康状态", "ok", "ok", True)
        
        Log.info("独立日志功能测试完成")
        
    except Exception as e:
        Log.error(f"独立日志功能测试失败: {str(e)}")
        Log.end_test("test_standalone_log_functionality", "FAILED")
        raise
    else:
        # 最后一步：结束测试
        Log.end_test("test_standalone_log_functionality", "PASSED")


def test_logid_consistency_across_calls():
    """测试多次调用中 LogID 的一致性"""
    # 第1步：设置 LogID
    logid = generate_logid()
    Log.set_logid(logid)
    
    # 第2步：开始测试
    Log.start_test("test_logid_consistency_across_calls")
    
    try:
        # 记录初始 LogID
        initial_logid = Log.get_logid()
        Log.info(f"初始 LogID: {initial_logid}")
        
        # 多次调用日志方法，验证 LogID 一致性
        for i in range(5):
            Log.info(f"第 {i+1} 次日志调用")
            current_logid = Log.get_logid()
            Checker.assert_equal(current_logid, initial_logid, f"LogID at call {i+1}")
        
        # 调用不同类型的日志方法
        Log.warning("警告日志测试")
        Checker.assert_equal(Log.get_logid(), initial_logid, "LogID after warning")
        
        Log.error("错误日志测试")
        Checker.assert_equal(Log.get_logid(), initial_logid, "LogID after error")
        
        Log.api_call("GET", "/test", 200, 0.1)
        Checker.assert_equal(Log.get_logid(), initial_logid, "LogID after API call")
        
        Log.assertion("测试断言", True, "expected", "expected")
        Checker.assert_equal(Log.get_logid(), initial_logid, "LogID after assertion")
        
        Log.info("LogID 一致性测试完成")
        
    except Exception as e:
        Log.error(f"LogID 一致性测试失败: {str(e)}")
        Log.end_test("test_logid_consistency_across_calls", "FAILED")
        raise
    else:
        # 最后一步：结束测试
        Log.end_test("test_logid_consistency_across_calls", "PASSED")


if __name__ == "__main__":
    # 可以直接运行此文件进行测试
    pytest.main([__file__, "-v"])
