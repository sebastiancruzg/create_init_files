import os
import argparse

def create_init_files(root_dir, exclude_dirs=None):
    """
    Recursively create __init__.py files in all subdirectories of root_dir,
    excluding specified directories.

    Args:
        root_dir (str): The root directory to start from
        exclude_dirs (list): List of directory names to exclude (optional)
    """
    if exclude_dirs is None:
        exclude_dirs = ["__pycache__"]

    # Normalize exclude_dirs for case-insensitive comparison
    exclude_dirs = {d.lower() for d in exclude_dirs}.union({"__pycache__"})

    for dirpath, _, _ in os.walk(root_dir):
        current_dir = os.path.basename(dirpath).lower()

        # Skip excluded directories
        if current_dir in exclude_dirs:
            print(f"Skipping excluded directory: {dirpath}")
            continue

        init_file = os.path.join(dirpath, '__init__.py')

        # Create __init__.py if it doesn't exist
        if not os.path.exists(init_file):
            try:
                with open(init_file, 'w') as f:
                    f.write('# This file makes the directory a Python package\n')
                print(f"Created: {init_file}")
            except OSError as e:
                print(f"Error creating {init_file}: {e}")
        else:
            print(f"Already exists: {init_file}")

def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Create __init__.py files in subdirectories.')
    parser.add_argument('root_dir', help='Root directory to start from')
    parser.add_argument('--exclude', nargs='*', default=["__pycache__"],
                        help='List of directory names to exclude')
    return parser.parse_args()

def main():
    """
    Main function to handle argument parsing and initiate __init__.py creation.
    """
    args = parse_args()

    if not os.path.isdir(args.root_dir):
        print(f"Error: {args.root_dir} is not a valid directory")
        return

    print(f"Starting from root directory: {args.root_dir}")
    if args.exclude:
        print(f"Excluding directories: {', '.join(args.exclude)}")

    create_init_files(args.root_dir, args.exclude)

if __name__ == "__main__":
    main()
