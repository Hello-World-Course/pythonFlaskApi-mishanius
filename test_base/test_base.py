import inspect
import os
import sys

import io
import json
import unittest
from contextlib import redirect_stdout
import importlib


class Message:

    def __init__(self, function_name=None,
                 file=None,
                 args=None,
                 expected_result=None,
                 real_result=None,
                 exception=None,
                 test_code=None) -> None:
        super().__init__()
        self.functionName = function_name
        self.file = file
        self.expectedResult = expected_result
        self.args = args
        self.input_values = None
        self.realResult = real_result
        self.real_type = None
        self.expected_type = None
        self.explanation = {'value': 'CODE_MISMATCH'}
        self.exception = exception
        self.test_code = test_code

    def __str__(self) -> str:
        return f"@@@PREFIX@@@{json.dumps(vars(self))}@@@SUFFIX@@@"


class AssignmentTester(unittest.TestCase):
    MINE_SWEEPER_PATH = os.path.join(os.pardir, os.pardir, os.pardir, os.pardir, "minesweeper")

    @classmethod
    def setUpClass(cls):
        debug = os.environ.get('MINESWEEPER_DEBUG')
        if debug == "True":
            import internal as internal
            os_module_path = inspect.getfile(internal)
            internals_dir = os.path.dirname(os_module_path)
            with open(os.path.join(internals_dir, "step_mapping.json")) as step_mapping_json:
                step_mapping = json.load(step_mapping_json)
                test_file = inspect.getfile(cls)
                test_dir = os.path.basename(os.path.dirname(test_file))
                step = step_mapping[test_dir]
                # checkout the desired repository
                os.system(f'cd {AssignmentTester.MINE_SWEEPER_PATH} && git checkout {step}')
                # change to the cloned repository directory
                # add the cloned repository to the Python path
                sys.path.insert(0, AssignmentTester.MINE_SWEEPER_PATH)

    def assertFileImport(self, fileName, expectedResult):
        message = Message(file=fileName, expected_result=expectedResult)
        try:
            output_holder = io.StringIO()
            with redirect_stdout(output_holder):
                importlib.import_module(fileName, package=None)
                print_out = output_holder.getvalue()
                message.realResult = str(print_out)
        except Exception as e:
            message.exception = str(e)
        self.assertEqual(print_out, expectedResult,
                         msg=message)

    def assertInWithMessage(self, val, result_provider, file_name, function_name):
        result, message = self.run_safely(result_provider)
        message.functionName = function_name
        message.file = file_name
        message.expectedResult = f"{val} should be inside the result"
        self.assertIn(val, result,
                      msg=message)

    def assertEqualWithMessage(self, first, second, msg: Message):
        msg.realResult = f"{first}"
        msg.expectedResult = f"{second}"
        msg.expected_type = type(second).__name__
        msg.real_type = type(first).__name__
        self.assertEqual(second, first,
                         msg=msg)

    def run_safely(self, result_provider):
        message = Message()
        result = None
        try:
            result = result_provider()
            message.realResult = str(result)
        except Exception as e:
            message.exception = str(e)
        return result, message

    def assertIsInstanceWithMessage(self, obj_provider, instance_class, file_name, function_name):
        result, message = self.run_safely(obj_provider)
        message.file = file_name
        message.functionName = function_name
        message.expectedResult = f"{result} should be instance of {instance_class}"
        self.assertIsInstance(result, instance_class,
                              msg=message)

    def assertRaisesWithMessage(self, func, *args, error, msg: Message):
        with self.assertRaises(error, msg=msg):
            func(*args)
