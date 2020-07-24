import argparse
from collections import defaultdict
import os
import re

# Dead code
# unused code
# symbols


file_extensions = ["hpp", "cpp"]
r = r"[a-zA-Z0-9]+\("
string_regex = re.compile(r'"[^"]*"')


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


def strip_line_comment(line: str) -> str:
    comment_index = line.find("//")
    if comment_index == -1:
        return line
    return line[:comment_index]


def strip_string(line: str) -> str:
    return string_regex.sub("", line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dirs", nargs='+')
    args = parser.parse_args()
    function_regex = re.compile(r)
    symbol_table = defaultdict(SymbolLocation)
    for filepath in walk_files(args.dirs):
        with open(filepath, "r") as file:
            try:
                lines = [
                    strip_string(strip_line_comment(line))
                    for line in file.readlines()
                ]
                for line_number, line in enumerate(lines):
                    matches = function_regex.findall(line)
                    for match in matches:
                        symbol = match[:-1]
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
