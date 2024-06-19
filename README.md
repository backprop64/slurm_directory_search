## Parallelize searching a large directory for files containing specific keywords using slurm

Parallelize the heck out of finding every file that contains specified keyword(s) in a large nested directory with slurm. this codebase assumes you have a file directory on a system with slurm, and miniconda/anaconda. It basically splits up the directory tree into sub trees, and searches each sub tree with a seperate slurm job; tested on big data (large nested file directory with lots of files)

---

### How to Use This Codebase

Create a Conda environment for this project, clone the codebase, and install the requirements:

```sh
$ conda create -n slurm_search python=3.9
$ git clone https://github.com/backprop64/slurm_directory_search
$ pip install tqdm
```

#### Setup Config

Fill in the config file with your information. Some of the defaults are what I used on my system for finding video files.

```json
{
    "account": "your_account",
    "partition": "your_partition",
    "ntasks_per_node": 1,
    "cpus_per_task": 2,
    "time": "15:00",
    "mem": "10G",
    "conda_env": "slurm_search",
    "conda_lib_path": "/path/to/conda/lib",
    "project_directory": "/path/to/slurm_directory_search",
    "keywords": [".mp4", ".avi", ".mov"]
}
```

- `project_directory`: Root directory of this repo (where you git cloned this).
- `account`: SLURM account to use.
- `partition`: SLURM partition to use.
- `ntasks_per_node`: Number of tasks per node.
- `cpus_per_task`: Number of CPUs per task.
- `time`: Maximum time for each job.
- `mem`: Memory allocation per job.
- `conda_env`: Name of the Conda environment to activate.
- `conda_lib_path`: Path to Conda's `lib` directory.
- `keywords`: List of keywords to search for in files.

#### Running The Scripts

1. **Make sure you filled in the configuration file as described above**
2. **Navigate to the project directory and activate the environment**

    ```sh
    cd path/to/slurm_directory_search
    conda activate slurm_search
    ```

3. **(Optional) Use `split_up_directories.py` to create a list of directories that step 3 will parallelize over**

    The `split_up_directories.py` script can be used to create a directories.txt file containing individual subdirectories to search in prallel. The script searches the directory tree to a specified depth, collecting all directories into a directories text file, and saves encountered files to a seperate text file with the relevant keywords along the way. You can also use it to count the number of directories that would be saved aswell (telling you how many jobs will be queued in parallel).

    ```sh
    python split_up_directories.py <command> [--root_dir <root_directory>] [--depth <search_depth>] [--dir_output <directory_output_file>] [--file_output <file_output_file>] [--keywords <filter_keywords>]
    ```

    ##### Commands

    - `save`: Saves directories to parallelize over (and file paths based on specified keywords).
    - `count`: Counts directories and files in the specified root directory.

    ##### Arguments

    - `--root_dir`: Root directory to start the search. Required for both commands.
    - `--depth`: Maximum depth of directories to search.
    - `--dir_output`: (Optional) Output file for directories to seach over (. txt file).
    - `--file_output`: (Optional) Output file for found files (a .txt).
    - `--keywords`: (Required for `save` command) Keywords to filter files.

4. **Launch the SLURM jobs**

   Use the `slurm_search.py` script to launch job submission, creating one job per folder/line in the provided directories `.txt` (by default, it will use the one generated in step 3):

    ```sh
    python slurm_search.py --config config.json --directories path/to/file/of/directories.txt
    ```
    ##### Arguments

    - `--config`: Path to the SLURM configuration JSON file.
    - `--directories`: (Optional) Specifies the file containing the directories to parallelize the search over (by default, it will use the one made in step 3).

5. **Combine all the individual search outputs after all jobs finish running:**

    ```sh
    cat file_batches/*.txt > all_found_files.txt
    ```

