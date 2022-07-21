from re import split
import sys
import os
import types
from pathlib import Path
import csv

def merge_csv(csv1, csv2, output_csv):
    csv1_path = Path(csv1)
    with csv1_path.open('r', encoding='utf-8') as data1_f:
        csv1_data = list(csv.reader(data1_f))
    csv2_path = Path(csv2)
    with csv2_path.open('r', encoding='utf-8') as data2_f:
        csv2_data = list(csv.reader(data2_f))

    output = []
    csv1_idx = 0
    for i in csv1_data:
        if i[0] == "Item":
            csv1_idx = csv1_idx + 1    
            break
        output.append(i)
        csv1_idx = csv1_idx + 1
        
    #Write a new label line as "Env", "Tdx", "None-Tdx"
    label_line = ["Container", "Tdx", "None-Tdx", "Units"]
    #writer.writerow(label_line)
    output.append(label_line)
    
    csv2_idx = csv1_idx
    for i in range(csv1_idx, len(csv1_data)):
        line = []
        line.append(csv1_data[i][0])
        line.append(csv1_data[i][1])
        line.append(csv2_data[i][1])
        line.append(csv1_data[i][2])
        output.append(line)
    
    output_path = Path(output_csv)
    with output_path.open('w', encoding='utf-8') as data3_f:
        writer = csv.writer(data3_f)
        for i in output:
            writer.writerow(i)
    
if __name__ == '__main__':
    merge_csv('tdx-output/boot-times.csv', 'ccv0-output/boot-times.csv', 'merge-output/boot-times.csv')
    merge_csv('tdx-output/memory-footprint.csv', 'ccv0-output/memory-footprint.csv', 'merge-output/memory-footprint.csv')
    merge_csv('tdx-output/memory-footprint-inside-container.csv', 'ccv0-output/memory-footprint-inside-container.csv', 'merge-output/memory-footprint-inside-container.csv')
    merge_csv('tdx-output/mlc.csv', 'ccv0-output/mlc.csv', 'merge-output/mlc.csv')
    merge_csv('tdx-output/blogbench.csv', 'ccv0-output/blogbench.csv', 'merge-output/blogbench.csv')
    merge_csv('tdx-output/memory-footprint-ksm.csv', 'ccv0-output/memory-footprint-ksm.csv', 'merge-output/memory-footprint-ksm.csv')
    
    
    