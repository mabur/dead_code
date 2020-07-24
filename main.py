import argparse
from collections import defaultdict
import os
import re
from typing import List


file_extensions = ["hpp", "cpp"]

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


class SymbolLocation:
    def __init__(self):
        self.occurances = 0
        self.line_number = -1
        self.file_path = ""


def walk_files(dir_paths):
    for dir_path in dir_paths:
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for file_name in files:
                if file_name.split(".")[-1] in file_extensions:
                    yield os.path.join(root, file_name)


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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dirs", nargs='+')
    args = parser.parse_args()

    symbol_table = defaultdict(SymbolLocation)
    for filepath in walk_files(args.dirs):
        with open(filepath, "r") as file:
            try:
                lines = [strip_line(line) for line in file.readlines()]
                lines = strip_multi_line_commenst(lines)
                lines = strip_multi_line_strings(lines)
                for line_number, line in enumerate(lines):
                    matches = function_regex.findall(line)
                    for symbol in matches:
                        symbol_table[symbol].occurances += 1
                        symbol_table[symbol].line_number = line_number
                        symbol_table[symbol].file_path = filepath
            except UnicodeDecodeError:
                print("Could not read: {}".format(filepath))
    unused_functions = {k: v for k, v in symbol_table.items() if v.occurances == 1}

    for k, v in unused_functions.items():
            print("{:<33} Line {:>4} in {}".format(k, v.line_number, v.file_path))
    print()
    print("Found {} possibly unused functions".format(len(unused_functions)))


if __name__ == "__main__":
    main()
