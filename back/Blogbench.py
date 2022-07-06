from pathlib import Path
import json
import csv

from TestInfor import TestInfor, Elem, ConfigList

class Result:
    def __init__(self):
        self.write = Elem('write')
        self.read = Elem('read')
        
class Blogbench:
    def __init__(self):
        self.TestInfor = TestInfor()
        self.Configs = ConfigList()
        self.Results = []
        
    def load_from_jsonfile(self, file_name):
        json_path = Path(file_name)
        with json_path.open('r', encoding='utf-8') as data_f:
            data = json.loads(data_f.read())
        self.TestInfor.load_from_dict(data)
        self.load_from_dict(data['blogbench'])
        return
    
    def load_from_dict(self, json_dict):
        self.Configs.load_from_dict(json_dict['Config'])
        for i in json_dict['Results']:
            res = Result()
            res.write.Result = i['write']['Result']
            res.write.Units = i['write']['Units']
            res.read.Result = i['read']['Result']
            res.read.Units = i['read']['Units']
            self.Results.append(res)
        return
    
    def to_csv(self, file_name):
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            self.TestInfor.write_to_csv(writer)
            self.Configs.write_to_csv(writer)
            writer.writerow(['write', 'read'])
            for i in self.Results:
                writer.writerow([str(i.write.Result) + i.write.Units,
                                str(i.read.Result) + i.read.Units])
        return

    def test():
        blogbench = Blogbench()
        blogbench.load_from_jsonfile('results/blogbench.json')
        blogbench.to_csv('output/blogbench.csv')
        print('blogbench.csv generated.')