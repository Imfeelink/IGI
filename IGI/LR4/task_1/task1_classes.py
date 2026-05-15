import pickle
import csv
import sys
import os

#appends parent folder(LR4) to system path Python 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import mixins

class TreeRecord():
    created_records = 0

    def __init__(self, tree_type: str, total: int, healthy: int):
        self.tree_type = tree_type
        self.total = total
        self.healthy = healthy
        self.created_records += 1
    

    @property
    def healthy(self):
        return self._healthy

    @healthy.setter
    def healthy(self, val):
            if(val > self.total):
                raise ValueError("Amount of healthy trees can't be greater then total amount of trees")
            self._healthy = val

    def __str__(self):
        return f"type = {self.tree_type} \t total = {self.total} \t healthy = {self.healthy}"
    
class BaseManager():
    def __init__(self, filepath: str, records: dict):
        self.filepath = filepath
        #using class ConvertDict
        self.records = records
    
    def get_total_trees(self):
        return sum(tree.total for tree in self.records.values())
    
    def get_healthy_trees(self):
        return sum(tree.healthy for tree in self.records.values())
    
    def get_sick_percent(self):
        return (self.get_total_trees() - self.get_healthy_trees()) / self.get_total_trees() * 100
    
    def get_every_tree_percent(self):
        for tree in self.records.values():
            print(f"{tree.tree_type}: {round(tree.total / self.get_total_trees(), 2) * 100}%")
            print(f"sick to total this type: {round((tree.total - tree.healthy) / tree.total, 2) * 100}%")
            
    def get_tree_info(self, target_type: str):
        return self.records[target_type]

    def save_to_file():
        pass

    def load_from_file():
        pass

class CSVManager(BaseManager, mixins.LogMixin):
    def __init__(self, filepath: str, records: dict):
        super().__init__(filepath, records)

    def save_to_file(self):
        with open(self.filepath, 'w', encoding='utf-8', newline='') as file:
            field_names = ['tree_type', 'total', 'healthy']
            writer = csv.DictWriter(file, field_names)

            writer.writeheader()

            for tree in self.records.values():
                writer.writerow({
                    'tree_type': tree.tree_type,
                    'total': tree.total,
                    'healthy': tree.healthy
                })
            self.log(f"Successful writing data to {self.filepath} using CSV")
            
    def load_from_file(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8', newline='') as file:
                reader = csv.DictReader(file)
                self.records = {}

                for row in reader:
                    tree_name = row['tree_type']
                    total_trees = int(row['total'])
                    healthy_trees = int(row['healthy'])
                    self.records[tree_name] = TreeRecord(tree_name, total_trees, healthy_trees)

            self.log(f"Successful loading data from {self.filepath} using CSV")
        except FileNotFoundError:
            self.log(f"Error! File not found, loading empty tree records")
            self.records = {}

class PickleManager(BaseManager, mixins.LogMixin):
    def __init__(self, filepath: str, records: dict):
        super().__init__(filepath, records)

    def save_to_file(self):
        #wb - binary writing
        with open(self.filepath, 'wb') as file:
            pickle.dump(self.records, file)
        self.log(f"Successful writing data to {self.filepath} using Pickle")

    def load_from_file(self):
        try:
            #rb - binary reading
            with open(self.filepath, 'rb') as file:
                self.records = pickle.load(file)
            self.log(f"Successful loading data from {self.filepath} using Pickle")
        except FileNotFoundError:
            self.log(f"Error! File not found, loading empty tree records")
            self.records = {}      

class ConvertDict:
    @staticmethod
    def get_tree_records(dict: dict) -> dict:
        tree_dict = {}
        for key, specs in dict.items():
            tree_dict[key] = TreeRecord(key, specs["total"], specs["healthy"])
        return tree_dict

class ProgramManager():
    manager = None

    def __init__(self, tree_dict: dict):
        self.tree_dict = tree_dict

    def manager_choice(self):
        while True:
            choice = input(
                "1 - csv" \
                "\n2 - pickle" \
                "\ninput: "
                ).strip()
            match choice:
                case '1':
                    self.manager = CSVManager("csv_data.csv", self.tree_dict)
                    self.manager.log("Current manager is CSV")
                    break
                case '2':
                    self.manager = PickleManager("pickle_data.pkl", self.tree_dict)
                    self.manager.log("Current manager is Pickle")
                    break
                case _:
                    print("Wrong input!")

    def menu(self):
        while True:
            choice = input(
            "1 - get total trees" \
            "\n2 - get healthy trees" \
            "\n3 - get sick to total trees percent" \
            "\n4 - get every tree concentration percent and sick percent every tree type" \
            "\n5 - change manager" \
            "\n6 - save data" \
            "\n7 - load data" \
            "\n0 - stop" \
            "\ninput: "
            ).strip()
            match choice:
                case '1':
                    self.manager.log(f"Total trees amount: {self.manager.get_total_trees()}")
                case '2':
                    self.manager.log(f"Healthy trees amount: {self.manager.get_healthy_trees()}")
                case '3':
                    self.manager.log(f"Sick trees concentration percent: {self.manager.get_sick_percent()}%")
                case '4':
                    self.manager.get_every_tree_percent()
                case '5':
                    self.manager_choice()
                case '6':
                    pass
                case '7':
                    pass
                case '0':
                    break
                case _:
                    print("Wrong input! Try again")
    