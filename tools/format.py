from argparse import ArgumentParser
from pathlib import Path
from subprocess import check_call

HERE = Path(__file__).parent
DIRS = (
    HERE.parent / "examples",
    HERE.parent / "include",
    HERE.parent / "src",
    HERE.parent / "tests",
)
PATTERNS = ("**/*.cpp", "**/*.h", "**/*.hpp")


def main():
    parser = ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    files = [
        file_path
        for dir_path in DIRS
        for pattern in PATTERNS
        for file_path in dir_path.glob(pattern)
    ]

    clang_format_options = ("--dry-run", "--Werror") if args.check else ("-i",)
    check_call(("clang-format", *clang_format_options, *(str(file) for file in files)))


if __name__ == "__main__":
    main()
