import os
import git
from collections import Counter
import terminal_colors as bc
import argparse

repo = None
ignored_dirs = [".git", ".bundle"]

def print_content(obj, contributor_list, level):
    spaces = "\t|"
    for _ in range(1, level):
        spaces = spaces + "\t|"
    print(spaces + "___" + bc.bcolors.GREEN + f'{obj}' + bc.bcolors.CYAN + f' {contributor_list}' + bc.bcolors.ENDC)

def check_files(path, level=1,current_level=1):
    if level == current_level:
        dir_list = os.listdir(path)
        for obj in dir_list:
            if os.path.isfile(f'{path}/{obj}'):
                contributors = check_contributors(f'{path}/{obj}')
                # print(bc.bcolors.GREEN + f'{path}/{obj}' + bc.bcolors.CYAN + f'\t{contributors}' + bc.bcolors.ENDC)
                print_content(f'{path}/{obj}', contributors, current_level)
            elif os.path.isdir(f'{path}/{obj}'):
                if obj not in ignored_dirs:
                    contributors = check_contributors(f'{path}/{obj}')
                    # print(bc.bcolors.GREEN + f'{path}/{obj}' + bc.bcolors.CYAN + f'\t{contributors}' + bc.bcolors.ENDC)
                    print_content(f'{path}/{obj}', contributors, current_level)
    else:
        dir_list = os.listdir(path)
        for obj in dir_list:
            if os.path.isfile(f'{path}/{obj}'):
                contributors = check_contributors(f'{path}/{obj}')
                print_content(f'{path}/{obj}', contributors, current_level)
            elif os.path.isdir(f'{path}/{obj}'):
                if obj not in ignored_dirs:
                    contributors = check_contributors(f'{path}/{obj}')
                    print_content(f'{path}/{obj}', contributors, current_level)
                    check_files(f'{path}/{obj}', level=level, current_level=current_level+1)


def check_contributors(path):
    if since:
        contributors_list=repo.git.log("--pretty='%an'", f'--since="{since}"', path).splitlines()
    else:
        contributors_list=repo.git.log("--pretty='%an'", path).splitlines()

    contributor_list = {}

    if len(contributors_list) > 0:
        contributors = Counter(contributors_list)

        for author,count in contributors.most_common(top):
            contributor_list[author] = count
    
    return contributor_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--level")
    parser.add_argument("-p", "--path")
    parser.add_argument("-s", "--since")
    parser.add_argument("-t", "--top")
    args = parser.parse_args()
    
    if args.path is None:
        raise Exception("Path is required")
    
    path = args.path
    level = int(args.level) if args.level else 1
    since = args.since if args.since else None
    top = int(args.top) if args.top else None
    
    repo = git.Repo(path)
    check_files(path,level=level)