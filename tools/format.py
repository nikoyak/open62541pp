from argparse import ArgumentParser
from pathlib import Path
import re
from shutil import which
from subprocess import check_call, check_output


CLANG_FORMAT_VERSION = "18.1.3"

HERE = Path(__file__).parent
ROOT = HERE.parent
TOOLS_DIR = ROOT / ".tools"

DIRS = (
    ROOT / "examples",
    ROOT / "include",
    ROOT / "src",
    ROOT / "tests",
)

PATTERNS = ("**/*.cpp", "**/*.h", "**/*.hpp")


def find_clang_format() -> tuple[str, bool]:
    local = [
        path
        for path in TOOLS_DIR.glob("clang-format*")
        if path.is_file() and path.stem == "clang-format"
    ]

    if len(local) > 1:
        raise RuntimeError(f"Multiple local clang-format executables found: {local}")

    if local:
        return str(local[0]), True

    clang_format = which("clang-format")
    if clang_format is None:
        raise RuntimeError("clang-format not found")

    return clang_format, False


def check_clang_format_version(clang_format: str):
    output = check_output(
        (clang_format, "--version"),
        text=True,
    )

    match = re.search(r"\b(\d+\.\d+\.\d+)\b", output)
    if match is None:
        raise RuntimeError(f"Cannot determine clang-format version from: {output.strip()}")

    version = match.group(1)
    if version != CLANG_FORMAT_VERSION:
        raise RuntimeError(
            f"clang-format {CLANG_FORMAT_VERSION} is required, "
            f"but {version} was found"
        )


def main():
    parser = ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    clang_format, is_local = find_clang_format()
    check_clang_format_version(clang_format)

    if is_local:
        print(f"Using local clang-format: {clang_format}")
    else:
        print(f"Using clang-format from PATH: {clang_format}")

    files = [
        file_path
        for dir_path in DIRS
        for pattern in PATTERNS
        for file_path in dir_path.glob(pattern)
    ]

    clang_format_options = ("--dry-run", "--Werror") if args.check else ("-i",)

    check_call(
        (
            clang_format,
            *clang_format_options,
            *(str(file) for file in files),
        )
    )

    action = "Checked" if args.check else "Formatted"
    print(f"{action} {len(files)} files with clang-format {CLANG_FORMAT_VERSION}")


if __name__ == "__main__":
    main()
