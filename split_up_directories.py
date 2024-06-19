import os
import glob
import argparse
from tqdm import tqdm

def save_paths(root_dir, depth, dir_output, file_output, keywords):
    os.makedirs(os.path.dirname(dir_output), exist_ok=True)
    os.makedirs(os.path.dirname(file_output), exist_ok=True)

    if isinstance(keywords, str):
        keywords = [keywords]
        
    # find all paths at specified depth
    pattern = os.path.join(root_dir, *['*'] * depth)
    paths = glob.glob(pattern, recursive=True)

    directories = []
    files = []
    # add directories and files to their output text files
    for path in tqdm(paths):
        if os.path.isdir(path):
            directories.append(path)
        elif any(keyword.lower() in path.lower() for keyword in keywords):
            files.append(path)

    with open(dir_output, 'w') as df:
        for directory in directories:
            df.write(f"{directory}\n")
    
    with open(file_output, 'w') as ff:
        for file in files:
            ff.write(f"{file}\n")

def count_at_depth(root_dir, depth=2):
    pattern = os.path.join(root_dir, *['*'] * depth)
    paths = glob.glob(pattern, recursive=True)

    num_directories = 0
    num_files = 0

    for path in tqdm(paths):
        if os.path.isdir(path):
            num_directories += 1
        else:
            num_files += 1
    return num_directories, num_files

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Directory and file counting and saving utility.')
    subparsers = parser.add_subparsers(dest='command', required=True)

    parser_save = subparsers.add_parser('save', help='Save directory and file paths.')
    parser_save.add_argument('root_dir', type=str, help='Root directory to search.')
    parser_save.add_argument('--depth', type=int, default=2, help='Depth to search for files and directories.')
    parser_save.add_argument('--dir_output', type=str, default='directories.txt', help='Output file for directories.')
    parser_save.add_argument('--file_output', type=str, default='file_batches/file_batch_0.txt', help='Output file for files.')
    parser_save.add_argument('--keywords', type=str, nargs='+', required=True, help='Keyword(s) to filter files.')

    parser_count = subparsers.add_parser('count', help='Count directories and files.')
    parser_count.add_argument('root_dir', type=str, help='Root directory to search.')
    parser_count.add_argument('--depth', type=int, default=2, help='Depth to search for files and directories.')

    args = parser.parse_args()

    if args.command == 'save':
        save_paths(args.root_dir, args.depth, args.dir_output, args.file_output, args.keywords)
    elif args.command == 'count':
        num_directories, num_files = count_at_depth(args.root_dir, args.depth)
        print(f"Directories: {num_directories}")
        print(f"Files: {num_files}")
