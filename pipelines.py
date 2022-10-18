import os
from models import bulk_insert


class LazyInsertPipeline:

    saved_results = []

    def __init__(self):
        self.limit = 1

    def process_item(self, item, spider):
        # self.saved_results.append(item)
        # # print(f"{len(self.saved_results)} Resultados salvos!")

        # if len(self.saved_results) >= self.limit and len(self.saved_results) != 0:
        #     bulk_insert(self.saved_results)
        #     self.saved_results = []

        bulk_insert([item])
        return item

    # def close_spider(self, item):
    #     if len(self.saved_results) < self.limit and len(self.saved_results) != 0:
    #         bulk_insert(self.saved_results)
    #         self.saved_results = []
