# testing.py
# Nova Programming Language - Testing Framework

import sys
import traceback
from datetime import datetime

class TestResult:
    """Test result"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.start_time = datetime.now()
        self.end_time = None
    
    def add_pass(self, test_name):
        self.passed += 1
    
    def add_fail(self, test_name, error):
        self.failed += 1
        self.errors.append({
            'test': test_name,
            'error': str(error),
            'traceback': traceback.format_exc()
        })
    
    def add_error(self, test_name, error):
        self.failed += 1
        self.errors.append({
            'test': test_name,
            'error': str(error),
            'traceback': traceback.format_exc()
        })
    
    def finish(self):
        self.end_time = datetime.now()
    
    def get_duration(self):
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0
    
    def to_dict(self):
        return {
            'passed': self.passed,
            'failed': self.failed,
            'total': self.passed + self.failed,
            'errors': self.errors,
            'duration': self.get_duration()
        }
    
    def print_report(self):
        """Print test report"""
        print("\n" + "=" * 50)
        print("🧪 Test Results")
        print("=" * 50)
        
        total = self.passed + self.failed
        print(f"Total: {total}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"⏱️ Duration: {self.get_duration():.3f}s")
        
        if self.errors:
            print("\n" + "=" * 50)
            print("❌ Errors:")
            print("=" * 50)
            for error in self.errors:
                print(f"\nTest: {error['test']}")
                print(f"Error: {error['error']}")
                print(f"Traceback:\n{error['traceback']}")


class Assertion:
    """Assertion utilities"""
    
    @staticmethod
    def equal(actual, expected, message=None):
        """Assert that actual equals expected"""
        if actual != expected:
            msg = message or f"Expected {expected}, got {actual}"
            raise AssertionError(msg)
    
    @staticmethod
    def not_equal(actual, expected, message=None):
        """Assert that actual does not equal expected"""
        if actual == expected:
            msg = message or f"Expected {actual} != {expected}"
            raise AssertionError(msg)
    
    @staticmethod
    def true(condition, message=None):
        """Assert that condition is true"""
        if not condition:
            msg = message or f"Expected True, got False"
            raise AssertionError(msg)
    
    @staticmethod
    def false(condition, message=None):
        """Assert that condition is false"""
        if condition:
            msg = message or f"Expected False, got True"
            raise AssertionError(msg)
    
    @staticmethod
    def is_none(value, message=None):
        """Assert that value is None"""
        if value is not None:
            msg = message or f"Expected None, got {value}"
            raise AssertionError(msg)
    
    @staticmethod
    def is_not_none(value, message=None):
        """Assert that value is not None"""
        if value is None:
            msg = message or f"Expected not None, got None"
            raise AssertionError(msg)
    
    @staticmethod
    def raises(func, exception_type, message=None):
        """Assert that func raises exception_type"""
        try:
            func()
            raise AssertionError(message or f"Expected {exception_type.__name__}, no exception raised")
        except exception_type:
            pass
        except Exception as e:
            raise AssertionError(message or f"Expected {exception_type.__name__}, got {type(e).__name__}")


class TestCase:
    """Base test case"""
    
    def __init__(self, name=None):
        self.name = name or self.__class__.__name__
        self.assertions = Assertion()
        self.setup_called = False
        self.teardown_called = False
    
    def setup(self):
        """Setup method - override in subclasses"""
        pass
    
    def teardown(self):
        """Teardown method - override in subclasses"""
        pass
    
    def run(self):
        """Run the test"""
        self.setup()
        self.setup_called = True
        
        result = TestResult()
        
        # Find all test methods
        test_methods = [
            getattr(self, method) for method in dir(self)
            if method.startswith('test_') and callable(getattr(self, method))
        ]
        
        for test_method in test_methods:
            test_name = f"{self.name}.{test_method.__name__}"
            try:
                test_method()
                result.add_pass(test_name)
            except AssertionError as e:
                result.add_fail(test_name, e)
            except Exception as e:
                result.add_error(test_name, e)
        
        self.teardown()
        self.teardown_called = True
        
        result.finish()
        return result


class TestRunner:
    """Test runner"""
    
    def __init__(self):
        self.tests = []
        self.result = TestResult()
        self.verbose = False
    
    def add_test(self, test_case):
        """Add a test case"""
        self.tests.append(test_case)
    
    def add_test_class(self, test_class):
        """Add all tests from a test class"""
        if isinstance(test_class, type) and issubclass(test_class, TestCase):
            test_instance = test_class()
            self.tests.append(test_instance)
    
    def run(self):
        """Run all tests"""
        print("🧪 Running tests...")
        
        for test in self.tests:
            print(f"  Running: {test.name}")
            test_result = test.run()
            self.result.passed += test_result.passed
            self.result.failed += test_result.failed
            self.result.errors.extend(test_result.errors)
            
            if self.verbose:
                test_result.print_report()
        
        self.result.finish()
        return self.result
    
    def run_single(self, test_case):
        """Run a single test case"""
        if isinstance(test_case, TestCase):
            result = test_case.run()
            self.result.passed += result.passed
            self.result.failed += result.failed
            self.result.errors.extend(result.errors)
            self.result.finish()
            return self.result
        return None


class TestSuite:
    """Test suite for organizing tests"""
    
    def __init__(self, name='TestSuite'):
        self.name = name
        self.tests = []
        self.setup_hooks = []
        self.teardown_hooks = []
    
    def add_test(self, test_case):
        """Add a test case"""
        self.tests.append(test_case)
    
    def add_tests(self, test_cases):
        """Add multiple test cases"""
        self.tests.extend(test_cases)
    
    def setup(self, hook):
        """Add a setup hook"""
        self.setup_hooks.append(hook)
    
    def teardown(self, hook):
        """Add a teardown hook"""
        self.teardown_hooks.append(hook)
    
    def run(self):
        """Run all tests in suite"""
        result = TestResult()
        
        # Run setup hooks
        for hook in self.setup_hooks:
            try:
                hook()
            except Exception as e:
                result.add_error('setup', e)
                return result
        
        # Run tests
        for test in self.tests:
            if isinstance(test, TestCase):
                test_result = test.run()
                result.passed += test_result.passed
                result.failed += test_result.failed
                result.errors.extend(test_result.errors)
            elif isinstance(test, TestSuite):
                test_result = test.run()
                result.passed += test_result.passed
                result.failed += test_result.failed
                result.errors.extend(test_result.errors)
        
        # Run teardown hooks
        for hook in self.teardown_hooks:
            try:
                hook()
            except Exception as e:
                result.add_error('teardown', e)
        
        result.finish()
        return result


def create_test_file(name, tests):
    """Create a test file"""
    content = f'''# {name}.nova
# Test file

import test

class {name.capitalize()}Test extends TestCase:
    
    def setup(self):
        # Setup code
        pass
    
    def teardown(self):
        # Teardown code
        pass
    
    def test_1(self):
        # Test 1
        assert_equal(1 + 1, 2)
        assert_true(True)
    
    def test_2(self):
        # Test 2
        assert_false(False)
        assert_not_none("hello")
    
    def test_3(self):
        # Test 3
        assert_raises(lambda: 1 / 0, ZeroDivisionError)
    
    def test_4(self):
        # Test 4 - with custom message
        assert_equal(2 * 2, 4, "Multiplication works")
'''
    
    with open(f'{name}.nova', 'w') as f:
        f.write(content)
    
    return f'{name}.nova'