#!/usr/bin/env python
import html
import os
from fnmatch import fnmatch
from pathlib import Path

MANUAL_EXCLUDES = {
    "uv.lock",
    ".pytest_cache",
    ".coverage",
    ".ruff_cache",
    "dist",
    "build",
    "__pycache__",
    "*.pyc",
    "node_modules",
    "package-lock.json",
    ".venv",
    ".git",
    "static_source/assets/*",
    "*.svg",
}


def parse_gitignore(gitignore_path: Path) -> set[str]:
    if not gitignore_path.exists():
        return set()

    patterns = set()
    with open(gitignore_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Normalize pattern
            if line.startswith("/"):
                line = line[1:]
            if line.endswith("/"):
                patterns.add(f"{line}**")
                line = line[:-1]

            patterns.add(line)
            # Add pattern with and without leading **/ to catch both absolute and relative paths
            if not line.startswith("**/"):
                patterns.add(f"**/{line}")

    return patterns


def should_include(path: Path, gitignore_patterns: set[str], source_root: Path) -> bool:
    try:
        rel_path = str(path.relative_to(source_root))
    except ValueError:
        return True

    # Check manual excludes first
    for pattern in MANUAL_EXCLUDES:
        if fnmatch(rel_path, pattern) or fnmatch(path.name, pattern):
            return False

    # Check gitignore patterns using full path
    for pattern in gitignore_patterns:
        if fnmatch(rel_path, pattern):
            return False

    return True


def export_project(source_dir: str, output_file: str):
    source_path = Path(source_dir).resolve()
    gitignore_patterns = parse_gitignore(source_path / ".gitignore")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("<documents>\n")

        file_count = 0
        for root_dir, dirs, files in os.walk(source_path):
            root_path = Path(root_dir)
            dirs[:] = [d for d in dirs if should_include(root_path / d, gitignore_patterns, source_path)]

            for file in files:
                file_path = root_path / file
                if not should_include(file_path, gitignore_patterns, source_path):
                    continue

                try:
                    with open(file_path, encoding="utf-8") as src:
                        content = src.read()

                    relative_path = file_path.relative_to(source_path)
                    f.write(f'<document index="{file_count + 1}">\n')
                    f.write(f"<source>{html.escape(str(relative_path))}</source>\n")
                    f.write(
                        f"<document_content>{html.escape(content)}</document_content>\n",
                    )
                    f.write("</document>\n")
                    file_count += 1

                except UnicodeDecodeError:
                    print(f"Skipping binary file: {file_path}")
                    continue

        f.write("</documents>")
        print(f"Exported {file_count} files")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Source directory")
    parser.add_argument("output", help="Output XML file")
    args = parser.parse_args()

    export_project(args.source, args.output)
