import sys
from cravat import BaseAnnotator
from cravat import constants, InvalidData
import sqlite3
import requests
import json
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self):
        self.civicdata = {}
        page_url = 'https://civicdb.org/api/genes?count=500&page=1'
        while page_url is not None:
            r = requests.get(page_url)
            d = json.loads(r.text)
            records = d['records']
            self.civicdata.update({x['name']:x for x in records})
            page_url = d['_meta']['links']['next']
        self.logger.info(self.civicdata['ARID1A'])
                
    def annotate(self, input_data, secondary_data=None):
        out = {}     
        hugo = input_data['hugo']
        match = self.civicdata.get(hugo)
        if match is not None and match['description']:
            out['description'] = match['description'].replace('\n', '').replace('"', "'")
            out['id'] = match['id']
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
