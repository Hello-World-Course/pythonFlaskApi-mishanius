import ast
import inspect
import re
import textwrap
from functools import wraps

from test_base.test_base import Message


def get_test_code(function):
    source = inspect.getsource(function)

    start_index = source.find("# test")
    end_index = source.find("# verify")

    if start_index == -1 or end_index == -1:
        raise ValueError("Both START_COMMENT and END_COMMENT must be present in the source code.")

    # Adjust indices to extract the desired portion without the comments themselves
    start_index = source.find('\n', start_index) + 1
    end_index = source.rfind('\n', start_index, end_index)
    return source[start_index:end_index]


def get_input_stubbings(function):
    try:
        source = inspect.getsource(function)
        pattern = r"side_effect=\[(.*?)\]"
        match = re.search(pattern, source)
        if match:
            extracted_list_str = match.group(1)
            extracted_list = ast.literal_eval(f"[{extracted_list_str}]")
            return extracted_list
    except Exception as e:
        pass
    return None


def get_imports(func):
    source = inspect.getsource(func)
    tree = ast.parse(textwrap.dedent(source))
    imports = []
    func = next(ast.iter_child_nodes(tree))
    for node in ast.iter_child_nodes(func):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            for alias in node.names:
                import_path = f"{module}.{alias.name}" if module else alias.name
                imports.append(import_path)
    return imports


def devin_test_decorator(func):
    imports = get_imports(func)
    try:
        test_code = get_test_code(func)
    except Exception as e:
        test_code = ""
    file_name = imports[0] if imports else ""
    message = Message(file=file_name, test_code=test_code)

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            message.input_values = get_input_stubbings(func)
            kwargs['message'] = message
            result = func(self, *args, **kwargs)
        except Exception as e:
            message.exception = str(e)
            if type(e) != AssertionError:
                self.fail(msg=message)
            else:
                self.fail()
        return result

    return wrapper
