import os
from models import bulk_insert
from scrapper_boilerplate import dataToCSV


class LazyInsertPipeline:

    saved_results = []

    def __init__(self):
        self.limit = 1

    def process_item(self, item, spider):
        bulk_insert([item])
        return item


class CSVCustomPipeline:

    def process_item(self, item, spider):
        dataToCSV(item, "data/data.csv")
        return item
