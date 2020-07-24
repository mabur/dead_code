from unittest import TestCase

from main import (
    strip_line_comment,
    strip_string,
    strip_comment,
    strip_comment_start,
    strip_comment_end,
    strip_multi_line_string,
    strip_multi_line_string_start,
    strip_multi_line_string_end,
    strip_include,
    strip_define_macro,
)


class Test(TestCase):
    def test_string_regex(self):
        self.assertEqual(
            strip_string('print("hello");'),
            "print();",
        )

    def test_strip_single_line_comment(self):
        self.assertEqual(
            strip_line_comment("int x = 5; // variable"),
            "int x = 5; ",
        )

    def test_strip_multi_line_comment(self):
        self.assertEqual(
            strip_comment("add(/*first*/9,/*second*/3);"),
            "add(9,3);",
        )

    def test_strip_multi_line_comment_start(self):
        self.assertEqual(
            strip_comment_start("print(); /* Comment"),
            "print(); ",
        )

    def test_strip_multi_line_comment_end(self):
        self.assertEqual(
            strip_comment_end("commetn */ print();"),
            " print();",
        )

    def test_strip_multi_line_string(self):
        self.assertEqual(
            strip_multi_line_string('print(R"(hello)")'),
            "print()"
        )

    def test_strip_multi_line_start(self):
        self.assertEqual(
            strip_multi_line_string_start('print(R"(hello'),
            "print("
        )

    def test_strip_multi_line_end(self):
        self.assertEqual(
            strip_multi_line_string_end('hello)");'),
            ");"
        )

    def test_strip_include(self):
        self.assertEqual(
            strip_include('#include <iostream>'),
            ""
        )


    def test_strip_define_macro(self):
        self.assertEqual(
            strip_define_macro('DEFINE_string(print, "", "Print an urn");'),
            ""
        )
