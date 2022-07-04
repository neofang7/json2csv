from pathlib import Path
import json
import csv

from TestInfor import TestInfor, Elem, ConfigList

class Result:
    def __init__(self):
        self.average = Elem('average')
        self.qemus = Elem('qemus')
        self.virtiofsds = Elem('virtiofsds')
        self.shims = Elem('shims')

    def print_myself(self):
        self.average.print_myself()
        self.qemus.print_myself()
        self.virtiofsds.print_myself()
        self.shims.print_myself()


class MemoryFootprint:
    def __init__(self):
        self.TestInfor = TestInfor()
        self.Configs = ConfigList()
        self.Results = []

    def load_from_jsonfile(self, file_name):
        json_path = Path(file_name)
        with json_path.open('r', encoding='utf-8') as data_f:
            data = json.loads(data_f.read())
        self.TestInfor.load_from_dict(data)
        self.load_from_dict(data['memory-footprint'])
        return

    def load_from_dict(self, json_dict):
        # fetch config
        self.Configs.load_from_dict(json_dict['Config'])

        # fetch results
        for i in json_dict['Results']:
            res = Result()
            res.average.Result = i['average']['Result']
            res.average.Units = i['average']['Units']
            res.qemus.Result = i['qemus']['Result']
            res.qemus.Units = i['qemus']['Units']
            res.virtiofsds.Result = i['virtiofsds']['Result']
            res.virtiofsds.Units = i['virtiofsds']['Units']
            res.shims.Result = i['shims']['Result']
            res.shims.Units = i['shims']['Units']

            self.Results.append(res)
        return

    def to_csv(self, file_name):
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            self.TestInfor.write_to_csv(writer)
            self.Configs.write_to_csv(writer)
            writer.writerow(['average', 'qemus', 'virtiofsds', 'shims'])
            for i in self.Results:
                writer.writerow([str(i.average.Result) + i.average.Units,
                                 str(i.qemus.Result) + i.qemus.Units,
                                 str(i.virtiofsds.Result) + i.virtiofsds.Units,
                                 str(i.shims.Result) + i.shims.Units])
        return


memory_footprint = MemoryFootprint()
memory_footprint.load_from_jsonfile('results/memory-footprint.json')
memory_footprint.to_csv('output/memory-footprint.csv')
print('memory-footprint.csv generated.')
