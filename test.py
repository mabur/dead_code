from unittest import TestCase

from main import strip_line_comment

class Test(TestCase):
    def test_strip_line_comment(self):
        self.assertEqual(
            strip_line_comment("int x = 5; // variable"),
            "int x = 5; ",
        )
