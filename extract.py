# Python 2/3 compatibility
from __future__ import print_function

from alchemyapi import AlchemyAPI
import json
import duckduckgo

class App:
    def __init__(self):
        self.alchemyapi = AlchemyAPI()
        self.raw_text = ''
        self.concepts = None
        self.keywords = None

    def parse_url(self, url=None):
        text_response = self.alchemyapi.text('url', url)
        if text_response['status'] == 'OK':
            self.raw_text =  text_response['text'].encode('utf-8')
        else:
            print('Error in text extraction call: ', text_response['statusInfo'])

    def extract_concepts(self):
        concept_response = self.alchemyapi.concepts('text', self.raw_text)
        if concept_response['status'] == 'OK':
            self.concepts = concept_response['concepts']
            # print('## Concepts ##')
            # for concept in self.concepts:
            #     print('text: ', concept['text'])
            #     print('relevance: ', concept['relevance'])
            #     print('')
        else:
            print('Error in concept tagging call: ', concept_response['statusInfo'])

    def extract_keywords(self):
        keyword_response = self.alchemyapi.keywords('text', self.raw_text, {'sentiment': 1})
        if keyword_response['status'] == 'OK':
            self.keywords = keyword_response['keywords']
            # print('')
            # print('## Keywords ##')
            # for keyword in self.keywords:
            #     print('text: ', keyword['text'].encode('utf-8'))
            #     print('relevance: ', keyword['relevance'])
            #     print('sentiment: ', keyword['sentiment']['type'])
            #     if 'score' in keyword['sentiment']:
            #         print('sentiment score: ' + keyword['sentiment']['score'])
            #     print('')
        else:
            print('Error in keyword extaction call: ', keyword_response['statusInfo'])

    def define_concepts(self):
        for concept in self.concepts:
            definition = duckduckgo.get_zci(concept['text'])
            print('%s -> %s' % (concept['text'], definition))
            print('')

    def define_keywords(self):
        for keyword in self.keywords:
            definition = duckduckgo.get_zci(keyword['text'])
            print('%s -> %s' % (keyword['text'], definition))
            print('')

def main():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print('[INFO] Processing')
    print('')

    url = 'http://www.history.com/topics/world-war-i/world-war-i-history'

    app = App()
    app.parse_url(url)
    app.extract_concepts()
    app.extract_keywords()
    app.define_concepts()
    app.define_keywords()

    print('')
    # pdb.set_trace()

if __name__ == '__main__':
    main()
