from goodtables import validate
from tabulator import Stream
import os
import datetime


class ValidateExtract:
    def __init__(self, file, schema, encoding='utf-8', delimiter=','):
        self.file = file
        self.path, self.fileext = os.path.split(self.file)
        self.filename = os.path.splitext(self.fileext)[0]
        self.schema = schema
        self.encoding = encoding
        self.delimiter = delimiter

    def create_backup(self):
        # TODO: create backup function
        # TODO write method which deletes backups older than X days
        pass

    def metric_monitoring(self):
        # TODO: writing row_count, number_of_errors, sane_rows_count into a table
        # with timestamp for better monitoring of data flows
        # tbl fields: csv_source, timestamp, row_count, error_count, sane_rows
        # TODO IDEA: use DataDogHook instead and outsourcing the metrics
        pass

    def is_data_new(self):
        # creation_date is not available under Linux Kernel
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(self.file)).date()
        current_time = datetime.datetime.now().date()
        if file_time != current_time:
            raise Exception('Current Export of ' + self.file + ' is having an older timestamp. Today: ' +
                            str(current_time) + ' vs: ' + str(file_time) + ' of file.')
        pass

    def prerequisite_checking(self):
        defect_rows = []
        error_messages = []
        result = validate(self.file,
                          delimiter=self.delimiter,
                          schema=self.schema,
                          encoding=self.encoding,
                          row_limit=99999999999,
                          skip_checks=['duplicate-row'])

        number_of_errors = (result['error-count'])

        for i in range(0, number_of_errors):
            error_row_number = result['tables'][0]['errors'][i]['row-number']
            error_message = result['tables'][0]['errors'][i]['message']
            defect_rows.append(error_row_number)
            error_messages.append(error_message)

        if len(result['tables']) == 0:
            raise Exception('No tables were loaded. It could be that the schema path is wrong')


        row_count = result['tables'][0]['row-count']
        sane_rows = (set(range(0, (row_count+1))) - set(defect_rows)) - set([0, 1])


        with Stream(self.file, skip_rows=defect_rows, delimiter=self.delimiter, encoding=self.encoding) as stream:
            #target_path = self.path + '/' + self.filename + '_sanitized.csv'
            target_path = self.filename + '_sanitized.csv'
            stream.save(target_path, encoding='utf-8', delimiter=',')
        if number_of_errors != 0:
            # custom parser function
            def add_error_message(extended_rows):
                # TODO: counter is like 1980....
                j = 0
                for row_number, headers, row in extended_rows:
                    if row_number == 1:
                        tmp = ['error_message'] + row
                    else:
                        tmp = [error_messages[i]] + row
                        j = j + 1
                    yield (row_number, headers, tmp)

            with Stream(self.file, skip_rows=sane_rows, post_parse=[add_error_message], encoding=self.encoding,
                        delimiter=self.delimiter) as stream:
                #target_path = self.path + '/' + self.filename + '_dirty.csv'
                target_path = self.filename + '_dirty.csv'
                stream.save(target_path, encoding='utf-8', delimiter=',')





