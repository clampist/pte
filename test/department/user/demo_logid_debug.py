"""
调试 LogID 生成问题
"""
import pytest
from core.logger import Log, generate_logid


def test_logid_debug_1():
    """调试测试 1"""
    # 直接生成 LogID
    direct_logid = generate_logid()
    print(f"直接生成的 LogID: {direct_logid}")
    
    # 获取当前 LogID
    current_logid = Log.get_logid()
    print(f"当前 LogID: {current_logid}")
    
    # 记录日志
    Log.info("调试测试 1 的日志")
    
    # 再次获取 LogID
    final_logid = Log.get_logid()
    print(f"最终 LogID: {final_logid}")
    
    # 验证
    assert current_logid == final_logid, f"LogID 应该保持一致: {current_logid} vs {final_logid}"


def test_logid_debug_2():
    """调试测试 2"""
    # 直接生成 LogID
    direct_logid = generate_logid()
    print(f"直接生成的 LogID: {direct_logid}")
    
    # 获取当前 LogID
    current_logid = Log.get_logid()
    print(f"当前 LogID: {current_logid}")
    
    # 记录日志
    Log.info("调试测试 2 的日志")
    
    # 再次获取 LogID
    final_logid = Log.get_logid()
    print(f"最终 LogID: {final_logid}")
    
    # 验证
    assert current_logid == final_logid, f"LogID 应该保持一致: {current_logid} vs {final_logid}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
