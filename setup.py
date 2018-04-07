import os
import subprocess
import re
import sys
from typing import List


ignore_patterns: List[str] = [
    'README.md',
    'setup.py',
]

# The directory that the script being run is in
script_dir: str = sys.path[0]


def is_ignore_pattern(target: str) -> bool:
    """
    Return if the target string matches any of the ignore patterns.

    Also return false if given empty string
    """
    matches_ignore_pattern = False
    for pattern in ignore_patterns:
        if re.match(pattern, target):
            matches_ignore_pattern = True
            break
    return matches_ignore_pattern or len(target) <= 0


def get_target_files() -> List[str]:
    """Return all files tracked by git and don't match any ignore_patterns."""
    wd = os.getcwd()
    os.chdir(script_dir)  # Must be in script dir to run git command
    cmd = subprocess.run(['git', 'ls-tree', '-r', 'HEAD', '--name-only'],
                         stdout=subprocess.PIPE)
    os.chdir(wd)
    output = cmd.stdout.decode('utf-8')
    all_files = output.split('\n')
    return list(filter(lambda s: not is_ignore_pattern(s), all_files))


def bool_user_prompt(prompt: str) -> bool:
    """
    Prompt user and return if they respond as "Yes".

    Defaults empty responses to "Yes".

    If q, quit or exit is entered, then quit the program.
    """
    ans = input(f'{prompt}? [Y,n]: ').strip().lower()
    while ans not in ['y', 'n', 'yes', 'no', 'q', 'quit', 'exit', '']:
        ans = input('Invalid reponse [(Y)es, (n)o, (q)uit]: ').strip().lower()
    if ans in ['q', 'quit', 'exit']:
        sys.exit(0)
    return ans in ['y', 'yes', '']


def process_file(source_path: str, install_path: str, backup_path: str) -> None:
    """Prompt user as to how to process file if not linked."""
    if os.path.isfile(install_path):
        if os.path.islink(install_path):
            if os.readlink(install_path) == source_path:
                print(f'OK:  {install_path}')
            else:
                print(f'ERR: {install_path} -> {os.readlink(install_path)} [Symlink points to different file]')
                if bool_user_prompt(f'Change symlink to point to {source_path}'):
                    os.remove(install_path)
                    os.symlink(source_path, install_path)
        else:
            print(f'ERR: {install_path} [Regular file]')
            if bool_user_prompt(f'Backup file and create symlink to {source_path}'):
                os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                os.rename(install_path, backup_path)
                print(f'file backed up to {backup_path}')
                os.symlink(source_path, install_path)
    else:
        print(f'ERR: {install_path} [Does not exist]')
        if bool_user_prompt(f'Create new symlink to {source_path}'):
            os.makedirs(os.path.dirname(install_path), exist_ok=True)
            os.symlink(source_path, install_path)


for target_file in get_target_files():
    repo_path = os.path.join(script_dir, target_file)  # path to file in repo
    install_path = os.path.join(os.environ['HOME'], target_file)  # path to the install path
    backup_path = os.path.join(script_dir, 'backup', target_file)
    process_file(repo_path, install_path, backup_path)