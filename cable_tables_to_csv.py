#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import optparse

from pyautocad import Autocad, utils
from pyautocad.contrib.excel import CsvWriter, XlsWriter


def iter_cable_tables(acad, block):
    for table in acad.iter_objects("table", block):
        if table.Columns != 9:
            continue
        ncols = table.Columns
        for row in xrange(3, table.Rows):
            yield [utils.mtext_to_string(table.GetText(row, col)) for col in xrange(ncols)]

def extract_tables_from_dwg(acad, writer, skip_model=True):
    for layout in acad.iter_layouts(skip_model=skip_model):
        for row in iter_cable_tables(acad, layout.Block):
            writer.writerow(row)

def main():
    writers = {'csv': CsvWriter, 'xls': XlsWriter}
    parser = optparse.OptionParser()
    parser.add_option('-f', '--format',
                      choices=writers.keys(), dest='format', metavar='FMT', default='csv',
                      help=u"Формат файла (%s) по умолчанию - csv" % ', '.join(writers.keys()))
    parser.add_option('-m', '--model',
                      dest='include_model', default=False, action='store_true',
                      help=u"Включить пространство Модели в область поиска")

    options, args = parser.parse_args()
    acad = Autocad()
    filename = args[0] if args else 'kab_list.%s' % options.format
    writer = writers[options.format](filename)
    extract_tables_from_dwg(acad, writer, not options.include_model)
    writer.close()

if __name__ == '__main__':
    with utils.timing():
        main()
