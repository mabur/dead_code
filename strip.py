import re
from typing import List

quotation_regex = re.compile(r'\\"')
string_regex = re.compile(r'"[^"]*"')
function_regex = re.compile(r"[a-zA-Z_]\w+")
include_regex = re.compile(r"#include[\w\W]+")
define_macro_regex = re.compile(r"DEFINE_[\w\W]+")
single_line_comment_regex = re.compile(r"//.*")
multi_line_comment_regex = re.compile(r"/\*[^(\*/)]*\*/")
multi_line_comment_regex_start = re.compile(r"/\*[^(\*/)]*")
multi_line_comment_regex_end = re.compile(r"[^(\*/)]*\*/")
multi_line_string_regex = re.compile(r'R"\([^(\)")]*\)"')
multi_line_string_regex_start = re.compile(r'R"\([^(\)")]*')
multi_line_string_regex_end = re.compile(r'[^(\)")]*\)"')


def strip_quotation(line: str) -> str:
    return quotation_regex.sub("", line)


def strip_include(line: str) -> str:
    return include_regex.sub("", line)


def strip_define_macro(line: str) -> str:
    return define_macro_regex.sub("", line)


def strip_line_comment(line: str) -> str:
    return single_line_comment_regex.sub("", line)


def strip_comment(line: str) -> str:
    return multi_line_comment_regex.sub("", line)


def strip_comment_start(line: str) -> str:
    i = line.find('/*')
    return line[:i]
    return multi_line_comment_regex_start.sub("", line)


def strip_comment_end(line: str) -> str:
    i = line.find('*/')
    return line[i + 2:]
    return multi_line_comment_regex_end.sub("", line)


def strip_multi_line_string(line: str) -> str:
    return multi_line_string_regex.sub("", line)


def strip_multi_line_string_start(line: str) -> str:
    i = line.find('R"(')
    return line[:i]
    return multi_line_string_regex_start.sub("", line)


def strip_multi_line_string_end(line: str) -> str:
    i = line.find(')"')
    return line[i+2:]
    return multi_line_string_regex_end.sub("", line)


def strip_string(line: str) -> str:
    return string_regex.sub("", line)


def strip_multi_line_commenst(lines: List[str]) -> List[str]:
    is_inside = False
    lines = [strip_comment(line)  for line in lines]
    for index, line in enumerate(lines):
        if "/*" in line:
            is_inside = True
            lines[index] = strip_comment_start(line)
        if "*/" in line:
            is_inside = False
            lines[index] = strip_comment_end(line)
        if is_inside:
            lines[index] = ""
    return lines


def strip_multi_line_strings(lines: List[str]) -> List[str]:
    is_inside = False
    lines = [strip_multi_line_string(line)  for line in lines]
    for index, line in enumerate(lines):
        if 'R"(' in line:
            is_inside = True
            lines[index] = strip_multi_line_string_start(line)
        if ')"' in line:
            is_inside = False
            lines[index] = strip_multi_line_string_end(line)
        if is_inside:
            lines[index] = ""
    return lines


def strip_line(line: str) -> str:
    return strip_string(strip_quotation(strip_line_comment(strip_define_macro(strip_include(line)))))


def strip_lines(lines: List[str]) -> List[str]:
    lines = [strip_line(line) for line in lines]
    lines = strip_multi_line_commenst(lines)
    lines = strip_multi_line_strings(lines)
    return lines