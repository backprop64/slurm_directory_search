import os
import argparse

def find_files_and_save_paths(input_dir, output_dir, output_filename, keywords):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    matching_paths = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if any(keyword.lower() in file.lower() for keyword in keywords):
                matching_paths.append(os.path.join(root, file))

    output_file_path = os.path.join(output_dir, output_filename)
    with open(output_file_path, "w") as output_file:
        for path in matching_paths:
            output_file.write(f"{path}\n")

    print(f"File paths saved to {output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search a directory for files containing keywords and save their paths to a text file."
    )
    parser.add_argument(
        "input_directory",
        type=str,
        help="Path to the input directory to search for files."
    )
    parser.add_argument(
        "output_directory",
        type=str,
        help="Path to the output directory to save the text file."
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="Name of the output text file."
    )
    parser.add_argument(
        "--keywords",
        type=str,
        nargs='+',
        required=True,
        help="Keyword(s) to search for in the file names."
    )
    args = parser.parse_args()

    find_files_and_save_paths(
        args.input_directory,
        args.output_directory,
        args.output_file,
        args.keywords
    )
