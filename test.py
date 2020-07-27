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
    strip_quotation,
)


class Test(TestCase):
    def test_string_regex1(self):
        self.assertEqual(
            "print();",
            strip_string('print("hello");'),
        )

    def test_string_regex2(self):
        self.assertEqual(
            "            , kDeveloperCredentials.c_str());",
            strip_string('            "Go to http://cli.volumental.com to make one", kDeveloperCredentials.c_str());'),
        )

    def test_quotation_regex1(self):
        self.assertEqual(
            '',
            strip_quotation(r'\"'),
        )

    def test_quotation_regex2(self):
        self.assertEqual(
            r'"Optional path to calibration, eg: ./rig_calibration.json"',
            strip_quotation(r'"Optional path to calibration, eg: \"./rig_calibration.json\""'),
        )

    def test_quotation_and_string_regex(self):
        self.assertEqual(
            '',
            strip_string(strip_quotation(r'"\""')),
        )

    def test_strip_single_line_comment1(self):
        self.assertEqual(
            "int x = 5; ",
            strip_line_comment("int x = 5; // variable"),
        )

    def test_strip_single_line_comment2(self):
        self.assertEqual(
            "    int   passes               =  3; ",
            strip_line_comment("    int   passes               =  3; // How many times should we refine?"),
        )

    def test_strip_multi_line_comment(self):
        self.assertEqual(
            "add(9,3);",
            strip_comment("add(/*first*/9,/*second*/3);"),
        )

    def test_strip_multi_line_comment_start(self):
        self.assertEqual(
            "print(); ",
            strip_comment_start("print(); /* Comment"),
        )

    def test_strip_multi_line_comment_end1(self):
        self.assertEqual(
            " print();",
            strip_comment_end("commetn */ print();"),
        )

    def test_strip_multi_line_comment_end2(self):
        self.assertEqual(
            "",
            strip_comment_end(" and one with a sleeping writer lock for waiting out slow reads (e.g. file system access). */"),
        )

    def test_strip_multi_line_string(self):
        self.assertEqual(
            "print()",
            strip_multi_line_string('print(R"(hello)")'),
        )

    def test_strip_multi_line_start(self):
        self.assertEqual(
            "print(",
            strip_multi_line_string_start('print(R"(hello'),
        )

    def test_strip_multi_line_end(self):
        self.assertEqual(
            ");",
            strip_multi_line_string_end('hello)");'),
        )

    def test_strip_include(self):
        self.assertEqual(
            "",
            strip_include('#include <iostream>'),
        )


    def test_strip_define_macro(self):
        self.assertEqual(
            "",
            strip_define_macro('DEFINE_string(print, "", "Print an urn");'),
        )
