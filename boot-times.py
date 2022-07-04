import pandas as pd
from pathlib import Path
import json
import csv

from test_infor import TestInfor, Elem

class Result:
    def __init__(self):
        self.results = {}
        self.total = Elem('total')
        self.to_workload = Elem('to-workload')
        self.in_kernel = Elem('in-kernel')
        self.to_kernel = Elem('to-kernel')
        self.to_quit = Elem('to-quit')

    def print_myself(self):
        self.total.print_myself()
        self.to_workload.print_myself()
        self.to_kernel.print_myself()
        self.in_kernel.print_myself()

class BootTimes:
    def __init__(self):
        self.TestInfor = TestInfor()
        self.Results = []

    def load_from_jsonfile(self, file_name):
        json_path = Path(file_name)
        with json_path.open('r', encoding='utf-8') as data_f:
            dat = json.loads(data_f.read())
        self.TestInfor.load_from_dict(dat)
        self.load_from_dict(dat['boot-times'])
        return

    def to_csv(self, file_name):
        with open(file_name, "w") as csv_file:
            writer = csv.writer(csv_file)
            self.TestInfor.write_to_csv(writer)
            writer.writerow(['total', 'to-workload', 'in-kernel', 'to-kernel', 'to-quit'])
            for i in self.Results:
                writer.writerow([str(i.total.Result) + i.total.Units,
                    str(i.to_workload.Result) + i.to_workload.Units,
                    str(i.in_kernel.Result) + i.in_kernel.Units,
                    str(i.to_kernel.Result) + i.to_kernel.Units,
                    str(i.to_quit.Result) + i.to_quit.Units])
        return

    #json_dict: dict['boot-times']
    def load_from_dict(self, json_dict):
        if type(json_dict) is not dict:
            print("Not a valid dict")
            return
        for i in json_dict['Results']:
            res = Result()
            res.total.Result = i['total']['Result']
            res.total.Units = i['total']['Units']
            res.to_workload.Result = i['to-workload']['Result']
            res.to_workload.Units = i['to-workload']['Units']
            res.in_kernel.Result = i['in-kernel']['Result']
            res.in_kernel.Units = i['in-kernel']['Units']
            res.to_kernel.Result = i['to-kernel']['Result']
            res.to_kernel.Units = i['to-kernel']['Units']
            res.to_quit.Result = i['to-quit']['Result']
            res.to_quit.Units = i['to-quit']['Units']
            self.Results.append(res)
            
        return

    def get_average(self, key):
        sum = 0
        unit = ''

        if len(self.Results) == 0:
            return 0

        for i in self.Results:
            if key == 'total':
                pair = i.total
            elif key == 'to-workload':
                pair = i.to_workload
            elif key == 'in-kernel':
                pair = i.in_kernel
            elif key == 'to-kernel':
                pair = i.to_kernel
            elif key == 'to-quit':
                pair = i.to_quit
            else:
                sum = 0
                break
            sum = sum + float(pair.Result)

        if sum != 0:
            unit = pair.Units
        return (sum / len(self.Results), unit)
    
    def print_myself(self):
        self.TestInfor.print_myself()
        for i in self.Results:
            i.print_myself()
        

boot_times = BootTimes()
boot_times.load_from_jsonfile('results/boot-times.json')
boot_times.to_csv('output/boot-times.csv')
print("boot-times.csv generated.")