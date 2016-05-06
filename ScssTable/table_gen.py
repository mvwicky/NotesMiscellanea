import os
import sys


class HtmlGen(object):
    pass


class TableWriter(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.current_table = None

    def init_file(self):
        if os.path.exists(os.path.abspath(self.file_name)):
            os.unlink(self.file_name)

    def copy_base(self, base_name):
        with open(base_name, 'rt') as in_file, \
             open(self.file_name, 'w') as out_file:
            out_file.write(in_file.read())

    def close_file(self):
        with open(self.file_name, 'a') as out_file:
            out_file.write('\n</body>\n')
            out_file.write('</html>\n')

    def open_table(self, headers):
        if self.current_table:
            print('There is an table already open, close it and try again')
            return -1
        self.current_table = dict()
        self.current_table['num_cols'] = len(headers)
        self.current_table['headers'] = headers
        with open(self.file_name, 'a') as out_file:
            out_file.write('\n')
            out_file.write('<div class="table">\n')
            out_file.write('<div class="trow">\n')
            for elem in headers:
                out_file.write('\t<span class="thead">{}</span>\n'
                               .format(elem))
            out_file.write('</div>\n')

    def write_row(self, row):
        if not self.current_table:
            print('No open table')
            return -1
        if len(row) != len(self.current_table['headers']):
            print('Number of cells does not match')
            return -1
        with open(self.file_name, 'a') as out_file:
            out_file.write('\n')
            out_file.write('<div class="trow">\n')
            for elem in row:
                if elem.replace('.', '').isnumeric():
                    out_file.write('<span class="tnum">{}</span>'
                                   .format(elem))
                else:
                    out_file.write('<span class="tlabel">{}</span>'
                                   .format(elem))
            out_file.write('</div>')

    def close_current_table(self):
        with open(self.file_name, 'a') as out_file:
            out_file.write('\n')
            out_file.write('</div>')
        self.current_table = None


def main():
    tw = TableWriter('out_file.html')
    tw.init_file()
    tw.open_table(['Rank', 'Title', 'IMDB Rating'])
    tw.write_row(['1', 'The Shawshank Redemption', '9.3'])
    tw.write_row(['2', 'The Godfather', '9.2'])
    tw.write_row(['3', 'The Godfather Part II', '9.0'])
    tw.write_row(['4', 'The Dark Knight', '9.0'])
    tw.write_row(['5', 'Schindler\'s List', '8.9'])
    tw.close_current_table()

if __name__ == '__main__':
    main()
