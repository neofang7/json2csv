from asyncore import write
from re import split
import sys
import os
import types

import csv
from fpdf import FPDF

# Merge tdx and ccv0 csvs to pdf.
# One case one page at least
# Two csv files of one case should be merged column by column or line by line.


def write_info_to_pdf(csv_file, pdf):
    with open(csv_file) as f:
        contents = list(csv.reader(f))
        page_width = pdf.w - 2*pdf.l_margin
        pdf.set_font('Times', '', 14.0)
        pdf.cell(page_width, 0.0, "Test Report", align='C')
        th = pdf.font_size
        pdf.ln(th)
        col_width = page_width/3
        for line in contents:
            if line[0] == "Cases":
                break
            pdf.cell(col_width, th, line[0], border=0)
            pdf.cell(col_width, th, line[1], border=0)
            pdf.ln(th)


def write_to_pdf(csv_file, head, pdf):
    try:
        f = open(csv_file, 'r')
    except FileNotFoundError as e:
        print("Ign: No such firle or directory: {}.".format(csv_file))
        return
    contents = list(csv.reader(f))
    page_width = pdf.w - 2*pdf.l_margin
    pdf.set_font('Times', 'B', 14.0)
    pdf.cell(page_width, 0.0, head, align='C')
    pdf.ln(10)

    pdf.set_font('Courier', '', 12)
    col_width = page_width/4

    start = 0
    for line in contents:
        if line[0] == "Cases":
            break
        start = start + 1

    pdf.set_font('Courier', 'B', 13)
    th = pdf.font_size
    row = contents[start]
    for i in row:
        pdf.cell(col_width, th, i, border=1)
    pdf.ln(th)

    for idx in range(start+1, len(contents)):
        pdf.set_font('Courier', 'B', 12)
        th = pdf.font_size
        row = contents[idx]
        # set cell format for row[0]
        pdf.cell(col_width, th, row[0], border=1)
        # pdf.ln(th)
        for j in range(1, len(row)):
            pdf.set_font('Courier', '', 12)
            th = pdf.font_size
            pdf.cell(col_width, th, row[j], border=1)
        pdf.ln(th)

    pdf.ln(10)


if __name__ == '__main__':
    # parse folder and get the generated json files.
    args = sys.argv[1:]
    pdf = FPDF()
    # example to write boot-times csv to a pdf.
    pdf.add_page()
    write_info_to_pdf('merge-output/boot-times.csv', pdf)
    pdf.add_page()
    write_to_pdf('merge-output/boot-times.csv', 'Boot Time', pdf)
    write_to_pdf('merge-output/blogbench.csv', 'Blogbench', pdf)
    write_to_pdf('merge-output/memory-footprint.csv', 'Memory Footprint', pdf)
    write_to_pdf('merge-output/memory-footprint-inside-container.csv',
                 'Memory Footprint Inside Container', pdf)
    write_to_pdf('merge-output/memory-footprint-ksm.csv',
                 'Memory Footprint KSM', pdf)
    pdf.add_page()
    write_to_pdf('merge-output/mlc.csv', 'MLC', pdf)
    write_to_pdf('merge-output/mlc-full.csv', 'MLC Full', pdf)

    pdf.output('Metrics_Test_Report.pdf', 'F')
