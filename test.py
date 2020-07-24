from unittest import TestCase

from main import (strip_line_comment, strip_string, strip_comment)


class Test(TestCase):
    def test_strip_line_comment(self):
        self.assertEqual(
            strip_line_comment("int x = 5; // variable"),
            "int x = 5; ",
        )

    def test_strip_comment(self):
        self.assertEqual(
            strip_comment("add(/*first*/9,/*second*/3);"),
            "add(9,3);",
        )

    def test_strip_comment_start(self):
        self.assertEqual(
            strip_comment("print(); /* Comment"),
            "print(); ",
        )

    def test_strip_comment_end(self):
        self.assertEqual(
            strip_comment("commetn */ print();"),
            " print();",
        )

    def test_string_regex(self):
        self.assertEqual(
            strip_string('print("hello");'),
            "print();",
        )
