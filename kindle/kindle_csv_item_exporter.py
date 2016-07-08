import settings
from scrapy.contrib.exporter import CsvItemExporter

class KindleCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', '\t')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export :
            kwargs['fields_to_export'] = fields_to_export

        super(KindleCsvItemExporter, self).__init__(*args, **kwargs)