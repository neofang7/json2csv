import json
import csv
from pathlib import Path
from TestInfor import TestInfor, Elem, ConfigList


class Result:
    def __init__(self):
        # self.memrequest = Elem()
        # self.memtotal = Elem()
        # self.memfree = Elem()
        # self.memavailable = Elem()
        self.results = {}


class MemoryFootprintInsideContainer:
    def __init__(self):
        self.TestInfor = TestInfor()
        self.Configs = None
        self.Results = []

    def load_from_jsonfile(self, file_name):
        json_path = Path(file_name)
        with json_path.open('r', encoding='utf-8') as data_f:
            data = json.loads(data_f.read())
        self.TestInfor.load_from_dict(data)

        self.load_from_dict(data['memory-footprint-inside-container'])
        return

    def load_from_dict(self, json_dict):
        if self.Configs != None:
            self.Configs.load_from_dict(json_dict['Config'])

        if len(json_dict['Results']) == 0:
            return

        self.Results = json_dict['Results']

        for d in self.Results:
            row = []
            for i in d.keys():
                row.append(str(d[i]['Result']) + d[i]['Units'])
            print(row)

        return

    def to_csv(self, file_name):
        with open(file_name, 'a') as csv_file:
            writer = csv.writer(csv_file)
            self.TestInfor.write_to_csv(writer)
            if self.Configs != None:
                self.Configs.write_to_csv(writer)

            # write label:
            writer.writerow(self.Results[0].keys())
            # write contents:
            for d in self.Results:
                row = []
                for i in d.keys():
                    row.append(str(d[i]['Result']) + d[i]['Units'])
                writer.writerow(row)

# footprint = MemoryFootprintInsideContainer()
# footprint.load_from_jsonfile('results/memory-footprint-inside-container.json')
# footprint.to_csv('output/memory-footprint-inside-contaienr.csv')
