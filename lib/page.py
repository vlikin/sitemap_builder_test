__author__ = 'viktor'

import csv

class Page(object):
    '''
       - It parses a page and contains page data
    '''

    def __init__(self, url):
        self.url = url
        self.nested = []
        self.connected_to = []
        self.processed = False

    def to_string(self, level=0):
        '''
            - It represents the object in the string format.
        '''
        if level > Page.max_depth:
            return
        str = '%d %s %s\n' % (self.level, '--' * self.level, self.url)
        print str
        for page in self.nested:
            str = '%s%s' % (str, self.to_string(level + 1))

        return str

    def GetTable(self, parent=None, max_depth=3, level=0):
        '''
            - It goes through the relation tree and build the table.
        '''
        if level > max_depth:
            return []
        if parent == None:
            parent = self
        row_list = []
        row = [id(self), level, self.url, id(parent)]
        row_list.append(row)
        for page in self.nested:
            row_list.extend(page.GetTable(self, max_depth, level+1))

        return row_list

    def SaveTable(self, filename, max_depth=3):
        '''
            - It saves the processed table to a file.
        '''
        table = self.GetTable(max_depth=max_depth)
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in table:
                writer.writerow(row)