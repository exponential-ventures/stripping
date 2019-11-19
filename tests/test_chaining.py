import uuid
from unittest import TestCase

from stripping import setup_stripping

tmp_dir = f"/tmp/{str(uuid.uuid4())}/cache/"

st, context = setup_stripping(tmp_dir)


@st.step(chain=True)
def test_chain_step_1():
    return "Hello"


# @st.chain
# def test_chain_step_2(prefix: str):
#     return prefix + ' World'


# from typing import Callable
#
#
# def first_decorator(*args, **kwargs):
#     func = None
#
#     breakpoint()
#
#     new_args = list(args)
#
#     if len(new_args) == 1 and callable(new_args[0]):
#         func = new_args.pop(0)
#
#     def default_func(*args, **kwargs):
#         print("using default_func")
#
#     if func is None:
#         func = default_func
#
#     args = tuple(new_args)
#
#     def wrapper():
#         print("first_decorator wrapper before")
#         breakpoint()
#         func(*args, **kwargs)
#         print("first_decorator wrapper after")
#
#     return wrapper
#
#
# def second_decorator(*args, **kwargs):
#     func = None
#
#     if len(args) == 1 and callable(args[0]):
#         func = args[0]
#
#     def default_func():
#         print("using default_func")
#
#     if func is None:
#         func = default_func
#
#     def wrapper(fn: Callable):
#         print("second_decorator wrapper before")
#         fn()
#         print("second_decorator wrapper after")
#
#     return wrapper
#
#
# @first_decorator(skip_cache=True)
# def another_func():
#     print("another_func")
#
#
# if __name__ == '__main__':
#     print("running main")
#     # another_func()

class ChainingTestCase(TestCase):

    def test_chain(self):
        r = st.execute()
        self.assertEqual('Hello', r)
