'''
there is class which stores data about trees
saves data to files using pickle and csv
Vania
task1
var14
14.04.2026
'''

from task1_classes import *

trees_dict = {
    "oak": {"total": 4, "healthy": 3},
    "birch": {"total": 6, "healthy": 3}
}

def task1_main():
    trees = ConvertDict.get_tree_records(trees_dict)
    
    manager = ProgramManager(trees)
    manager.manager_choice()
    manager.menu()


if __name__ == "__main__":
    task1_main()