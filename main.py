import argparse
from collections import defaultdict
import os

from strip import strip_lines, find_symbols

file_extensions = ["hpp", "cpp"]


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dirs", nargs='+')
    args = parser.parse_args()

    symbol_table = defaultdict(SymbolLocation)
    for filepath in walk_files(args.dirs):
        with open(filepath, "r") as file:
            try:
                lines = file.readlines()
                lines_clean = strip_lines(lines)
                for line_number, line in enumerate(lines_clean):
                    symbols = find_symbols(line)
                    for symbol in symbols:
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
