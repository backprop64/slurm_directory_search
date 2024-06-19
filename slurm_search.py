import os
import tempfile
import time
import json
import argparse
from tqdm import tqdm

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SLURM job launcher for searching files and directories.')
    parser.add_argument('--config', type=str, required=True, help='Path to SLURM configuration JSON file.')
    parser.add_argument('--directories', type=str, default='directories.txt', help='Path to directories.txt file.')

    args = parser.parse_args()

    with open(args.config, 'r') as config_file:
        config = json.load(config_file)

    directories_file = args.directories
    all_directories = [line.strip() for line in open(directories_file)]

    output_root = "file_batches"
    if not os.path.exists(output_root):
        os.makedirs(output_root)

    if not os.path.exists('slurm_logs'):
        os.makedirs('slurm_logs')
        
    for job_num, directory in tqdm(enumerate(all_directories), desc="Launching SLURM jobs"):
        output_file = f"file_batch_{job_num + 1}.txt"
        print(directory)
        SBATCH_STRING = f"""#!/bin/sh
#SBATCH --account={config['account']} 
#SBATCH --partition={config['partition']}
#SBATCH --job-name=searching_subdirectory_{job_num}
#SBATCH --output={os.path.join(config['project_directory'],'slurm_logs/')}file_batch_{job_num + 1}.log
#SBATCH --ntasks-per-node={config['ntasks_per_node']}
#SBATCH --cpus-per-task={config['cpus_per_task']}
#SBATCH --time={config['time']}
#SBATCH --mem={config['mem']}

conda init

conda activate {config['conda_env']}

export LD_LIBRARY_PATH={config['conda_lib_path']}:$LD_LIBRARY_PATH

cd {config['project_directory']}

python search_directories.py "{directory}" "{output_root}" "{output_file}" --keywords {" ".join(config['keywords'])}
"""

        SBATCH_STRING = SBATCH_STRING.format(
            directory=directory,
            output_root= output_root,
            output_file = output_file,
        )

        dirpath = tempfile.mkdtemp()
        script_path = os.path.join(dirpath, "scr.sh")
        with open(script_path, "w") as tmpfile:
            tmpfile.write(SBATCH_STRING)
        os.system(f"sbatch {script_path}")
        print(f"Launched from {script_path}")
        time.sleep(0.01)
