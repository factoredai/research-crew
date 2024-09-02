import argparse
import os


def generate_tree(startpath, ignore_patterns):
    tree = []
    startpath = os.path.abspath(startpath)
    startpath_depth = startpath.count(os.sep)

    for root, dirs, files in os.walk(startpath):
        if any(ignore_pattern in root.split(os.sep) for ignore_pattern in ignore_patterns):
            continue

        depth = root.count(os.sep) - startpath_depth
        if depth == 0:
            tree.append(f"{os.path.basename(root)}/")
        else:
            tree.append("│   " * (depth - 1) + "├── " + os.path.basename(root) + "/")

        for file in sorted(files):
            if not any(ignore_pattern in file for ignore_pattern in ignore_patterns):
                tree.append("│   " * depth + "├── " + file)

        dirs[:] = [d for d in sorted(dirs) if not any(ignore_pattern in d for ignore_pattern in ignore_patterns)]

    return "\n".join(tree)


def main():
    parser = argparse.ArgumentParser(description="Generate a folder structure representation.")
    parser.add_argument("path", help="Path to the project directory (absolute or relative)")
    parser.add_argument(
        "-i",
        "--ignore",
        nargs="+",
        default=[".git", "__pycache__"],
        help="List of patterns to ignore. Default: .git __pycache__",
    )
    parser.add_argument("-o", "--output", help="Output file path (optional)")
    args = parser.parse_args()

    abs_path = os.path.abspath(args.path)

    if not os.path.isdir(abs_path):
        print(f"Error: {abs_path} is not a valid directory")
        return

    print(f"Generating tree for: {abs_path}")
    print(f"Ignoring patterns: {', '.join(args.ignore)}")
    tree = generate_tree(abs_path, args.ignore)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(tree)
        print(f"Tree structure saved to {args.output}")
    else:
        print(tree)


if __name__ == "__main__":
    main()

# python scripts/get_folder_structure.py ./ -i data .git __pycache__ 0src -o here.md
