from pathlib import Path
import json
import csv
from sre_constants import NOT_LITERAL

from TestInfor import TestInfor, Elem


class Result:
    def __init__(self):
        self.bandwidth = Elem('bandwidth')
        self.jitter = Elem('jitter')
        # self.items = []
        # self.item_keys = []


class NetworkIperf3:
    def __init__(self):
        self.TestInfor = TestInfor()
        self.Configs = None
        self.Results = []

    def load_from_jsonfile(self, file_name):
        json_path = Path(file_name)
        with json_path.open('r', encoding='utf-8') as data_f:
            data = json.loads(data_f.read())
        self.TestInfor.load_from_dict(data)
        testname = self.TestInfor.Contents['testname']
        self.load_from_dict(data[testname])
        return

    def load_from_dict(self, json_dict):
        # fetch config
        if self.Configs != None:
            self.Configs.load_from_dict(json_dict['Config'])

        if len(json_dict['Results']) == 0:
            return

        # fetch results
        for i in json_dict['Results']:
            res = Result()
            res.bandwidth.Result = i['bandwidth']['Result']
            res.bandwidth.Units = i['bandwidth']['Units']
            res.jitter.Result = i['jitter']['Result']
            res.jitter.Units = i['jitter']['Units']
            self.Results.append(res)
        return

    def to_csv(self, file_name):
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            self.TestInfor.write_to_csv(writer)
            if self.Configs != None:
                self.Configs.write_to_csv(writer)
            writer.writerow(['bandwidth', 'jitter'])
            for i in self.Results:
                writer.writerow([str(i.bandwidth.Result) + i.bandwidth.Units,
                                 str(i.jitter.Result) + i.jitter.Units])
        return

    def test():
        perf_data = NetworkIperf3()
        perf_data.load_from_jsonfile('results/network-iperf3.json')
        perf_data.to_csv('output/network-iperf3.csv')
