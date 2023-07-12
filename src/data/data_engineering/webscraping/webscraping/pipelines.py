# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re

class CleaningPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("year"):
            adapter["year"] = adapter["year"].replace('(', '')
            adapter["year"] = adapter["year"].replace(')', '')
        if adapter.get('duration'):
            adapter["duration"] = adapter["duration"].replace(' min', '')
            adapter["duration"] = int(adapter["duration"]) 
        if adapter.get('genre'):
            adapter["genre"] = adapter["genre"].replace('\n', '').rstrip()
        if adapter.get('rating'):
            adapter["rating"] = float(adapter["rating"])
        if adapter.get("directors"):
            adapter["directors"] = re.sub(r'<[^>]+>', '', adapter["directors"])
            adapter["directors"] = adapter["directors"].replace('Director:', '')
            adapter["directors"] = adapter["directors"].replace('Directors:', '')
            adapter["directors"] = adapter["directors"].replace('\n', '').strip()
        if adapter.get("stars"):
            adapter["stars"] = re.sub(r'<[^>]+>', '', adapter["stars"])
            adapter["stars"] = adapter["stars"].replace('Stars:', '')
            adapter["stars"] = adapter["stars"].replace('\n', '').strip()
        if adapter.get("gross"):
            adapter["gross"] = adapter["gross"].replace(',', '')
            adapter["gross"] = int(adapter["gross"])

        return item
    
class DropDuplicatesPipeline:
    def __init__(self):
        self.titles_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["title"] in self.titles_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.titles_seen.add(adapter["title"])
            return item

