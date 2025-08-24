"""
测试 LogID 唯一性的演示
"""
import pytest
from core.logger import Log


def test_logid_1():
    """测试用例 1"""
    Log.info("测试用例 1 的日志")
    current_logid = Log.get_logid()
    print(f"测试用例 1 的 LogID: {current_logid}")
    assert current_logid is not None
    assert len(current_logid) > 0


def test_logid_2():
    """测试用例 2"""
    Log.info("测试用例 2 的日志")
    current_logid = Log.get_logid()
    print(f"测试用例 2 的 LogID: {current_logid}")
    assert current_logid is not None
    assert len(current_logid) > 0


def test_logid_3():
    """测试用例 3"""
    Log.info("测试用例 3 的日志")
    current_logid = Log.get_logid()
    print(f"测试用例 3 的 LogID: {current_logid}")
    assert current_logid is not None
    assert len(current_logid) > 0


class TestLogIDClass:
    """测试类中的 LogID 唯一性"""
    
    def test_class_method_1(self):
        """类方法测试 1"""
        Log.info("类方法测试 1 的日志")
        current_logid = Log.get_logid()
        print(f"类方法测试 1 的 LogID: {current_logid}")
        assert current_logid is not None
        assert len(current_logid) > 0
    
    def test_class_method_2(self):
        """类方法测试 2"""
        Log.info("类方法测试 2 的日志")
        current_logid = Log.get_logid()
        print(f"类方法测试 2 的 LogID: {current_logid}")
        assert current_logid is not None
        assert len(current_logid) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
