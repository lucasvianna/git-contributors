import os
import git
from collections import Counter
import terminal_colors as bc
import argparse

repo = None
ignored_dirs = [".git", ".bundle"]

def print_tree(full_obj, contributor_list, level):
    spaces = ""
    tree_branch = ""
    obj = full_obj.split("/")[-1]
    if level > 1:
        spaces = "|"
        tree_branch = "___"
        for _ in range(1, level):
            spaces = spaces + "   |"

    print(spaces + 
        tree_branch + 
        bc.bcolors.GREEN + 
        f'{obj}' + 
        bc.bcolors.CYAN + 
        f' {contributor_list}' + 
        bc.bcolors.ENDC)

def check_files(path, depth=1, current_level=1, only_dirs=None):
    if depth == current_level:
        dir_list = os.listdir(path)
        for obj in dir_list:
            if os.path.isfile(f'{path}/{obj}') and only_dirs == False:
                contributors = check_contributors(f'{path}/{obj}')
                print_tree(f'{path}/{obj}', contributors, current_level)
            elif os.path.isdir(f'{path}/{obj}'):
                if obj not in ignored_dirs:
                    contributors = check_contributors(f'{path}/{obj}')
                    print_tree(f'{path}/{obj}', contributors, current_level)
    else:
        dir_list = os.listdir(path)
        for obj in dir_list:
            if os.path.isfile(f'{path}/{obj}') and only_dirs == False:
                contributors = check_contributors(f'{path}/{obj}')
                print_tree(f'{path}/{obj}', contributors, current_level)
            elif os.path.isdir(f'{path}/{obj}'):
                if obj not in ignored_dirs:
                    contributors = check_contributors(f'{path}/{obj}')
                    print_tree(f'{path}/{obj}', contributors, current_level)
                    check_files(f'{path}/{obj}', depth=depth, current_level=current_level+1)


def check_contributors(path):
    if since:
        contributors_list = repo.git.log("--pretty='%an'", f'--since="{since}"', path).splitlines()
    else:
        contributors_list = repo.git.log("--pretty='%an'", path).splitlines()

    contributor_list = {}

    if len(contributors_list) > 0:
        contributors = Counter(contributors_list)

        for author,count in contributors.most_common(top):
            contributor_list[author] = count
    
    return contributor_list

def set_params():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--depth")
    parser.add_argument("-p", "--path")
    parser.add_argument("-s", "--since")
    parser.add_argument("-t", "--top")
    parser.add_argument("--only-dirs", action='store_true')
    
    return parser.parse_args()

if __name__ == "__main__":
    args = set_params()
    
    if args.path is None:
        raise Exception("Path is required")
    
    path = args.path
    depth = int(args.depth) if args.depth else 0
    since = args.since if args.since else None
    top = int(args.top) if args.top else None
    only_dirs = args.only_dirs
    
    repo = git.Repo(path)
    check_files(path, depth=depth, only_dirs=only_dirs)