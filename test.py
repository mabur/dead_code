from unittest import TestCase

from main import (
    strip_line_comment,
    strip_string,
    strip_comment,
    strip_comment_start,
    strip_comment_end,
)


class Test(TestCase):
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

    def test_string_regex(self):
        self.assertEqual(
            strip_string('print("hello");'),
            "print();",
        )
