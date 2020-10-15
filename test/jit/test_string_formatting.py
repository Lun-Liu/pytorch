import os
import sys

import torch
from typing import List

# Make the helper files in test/ importable
pytorch_test_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(pytorch_test_dir)
from torch.testing._internal.jit_utils import JitTestCase

if __name__ == '__main__':
    raise RuntimeError("This test file is not meant to be run directly, use:\n\n"
                       "\tpython test/test_jit.py TESTNAME\n\n"
                       "instead.")

class TestStringFormatting(JitTestCase):

    def test_modulo_operator(self):
        def fn(dividend: int, divisor: int) -> int:
            return dividend % divisor
        self.checkScript(fn, (1,))

    def test_string_interpolation_with_string_placeholder_and_string_variable(self):
        def fn(arg1: str):
            return "%s in template" % arg1
        self.checkScript(fn, ("foo",))

    def test_string_interpolation_with_string_placeholder_and_format_string_variable(self):
        def fn(arg1: str):
            return arg1 % "foo"
        self.checkScript(fn, ("%s in template",))

    def test_string_interpolation_with_double_percent_in_string(self):
        def fn(arg1: str):
            return "%s in template %%" % arg1
        self.checkScript(fn, ("foo",))

    def test_string_interpolation_with_percent_in_string(self):
        @torch.jit.script
        def fn(arg1: str) -> str:
            return "%s in template %" % arg1    # noqa: F501

        with self.assertRaisesRegex(RuntimeError, "Incomplete format specifier"):
            fn("foo")

    def test_string_interpolation_with_string_placeholder_and_digit_variable(self):
        def fn(arg1: int) -> str:
            return "%s in template" % arg1
        self.checkScript(fn, (1,))

    def test_string_interpolation_with_digit_placeholder_and_digit_variable(self):
        def fn(arg1: int) -> str:
            return "%d in template" % arg1
        self.checkScript(fn, (1,))

    def test_string_interpolation_with_alternate_digit_placeholder(self):
        def fn(arg1: int) -> str:
            return "%i in template" % arg1
        self.checkScript(fn, (1,))

    def test_string_interpolation_with_digit_placeholder_and_string_variable(self):
        @torch.jit.script
        def fn(arg1: str) -> str:
            return "%d in template" % arg1

        with self.assertRaisesRegex(RuntimeError, "%d requires a number for formatting, but got String"):
            fn("1")

    def test_string_interpolation_with_exponent_placeholder_and_string_variable(self):
        @torch.jit.script
        def fn(arg1: str) -> str:
            return "%e in template" % arg1

        with self.assertRaisesRegex(RuntimeError, "%e requires a number for formatting, but got String"):
            fn("1")

    def test_string_interpolation_with_lowercase_exponent_placeholder_and_digit_variable(self):
        def fn(arg1: int) -> str:
            return "%e in template" % arg1
        self.checkScript(fn, (1,))

    def test_string_interpolation_with_capital_exponent_placeholder_and_digit_variable(self):
        def fn(arg1: int) -> str:
            return "%E in template" % arg1
        self.checkScript(fn, (1,))

    def test_string_interpolation_with_float_placeholder_and_float_variable(self):
        def fn(arg1: float) -> str:
            return "%f in template" % arg1
        self.checkScript(fn, (1.0,))

    def test_string_interpolation_with_float_placeholder_and_digit_variable(self):
        def fn(arg1: int) -> str:
            return "%f in template" % arg1
        self.checkScript(fn, (1,))

    def test_string_interpolation_with_char_placeholder_and_char_variable(self):
        def fn(arg1: str) -> str:
            return "%c in template" % arg1
        self.checkScript(fn, ("a",))

    def test_string_interpolation_with_char_placeholder_and_digit_variable(self):
        def fn(arg1: int) -> str:
            return "%c in template" % arg1
        self.checkScript(fn, (97,))

    def test_string_interpolation_with_char_placeholder_and_true_string_variable(self):
        @torch.jit.script
        def fn(arg1: str) -> str:
            return "%c in template" % arg1

        with self.assertRaisesRegex(RuntimeError, "%c requires an int or char for formatting, but got String"):
            fn("foo")

    def test_string_interpolation_with_multiple_placeholders(self):
        def fn(arg1: str, arg2: int, arg3: float) -> str:
            return "%s %d %f in template" % (arg1, arg2, arg3)
        self.checkScript(fn, ("foo", 1, 1))

    def test_string_interpolation_with_subscript(self):
        def fn(arg1: List[str]) -> str:
            return "%s in template" % arg1[0]
        self.checkScript(fn, (["foo", "bar"],))

    def test_string_interpolation_with_too_few_arguments(self):
        @torch.jit.script
        def fn(arg1: str) -> str:
            return "%s %s in template" % arg1

        with self.assertRaisesRegex(RuntimeError, "Too few arguments for format string"):
            fn("foo")

    def test_string_interpolation_with_too_many_arguments(self):
        @torch.jit.script
        def fn(arg1: str, arg2: str) -> str:
            return "%s in template" % (arg1, arg2)    # noqa: F507

        with self.assertRaisesRegex(RuntimeError, "Too many arguments for format string"):
            fn("foo", "bar")

    def test_string_interpolation_with_unknown_format_specifier(self):
        @torch.jit.script
        def fn(arg1: str) -> str:
            return "%a in template" % arg1    # noqa: F501

        with self.assertRaisesRegex(RuntimeError, "The specifier %a is not supported in TorchScript format strings"):
            fn("foo")
