import os
from models import bulk_insert


class LazyInsertPipeline:

    saved_results = []

    def __init__(self):
        self.limit = 1

    def process_item(self, item, spider):
        bulk_insert([item])
        return item
