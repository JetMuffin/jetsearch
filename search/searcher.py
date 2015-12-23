from pprint import pprint

from pymongo import MongoClient
from processor.segmenters import JiebaSegmenter


class Searcher(object):
    def __init__(self, mongo_addr, db):
        mongo_host, mongo_port = mongo_addr.split(":")
        self.server = MongoClient(mongo_host, int(mongo_port))
        self.db = self.server[db]

    def search(self, word, page):
        word_list = self.analyze(word)
        docs = {}
        merge_docs = set()
        first = True
        for word in word_list:
            term = self.db.tbl_ranked_term.find_one({'_id': word})
            doc_list = set()
            if term:
                for term_doc in term['value']['docs']:
                    docs[term_doc['id']] = term_doc
                    doc_list.add(term_doc['id'])
                if first:
                    merge_docs = doc_list
                    first = False
                else:
                    merge_docs = merge_docs.intersection(doc_list)

        merge_docs = [docs[doc] for doc in merge_docs]

        merge_docs.sort(key=lambda x: x['rating'], reverse=True)
        number = min(len(merge_docs), number)
        result = []

        for i in range(start, start+number):
            doc = self.db.tbl_page.find_one({"_id": merge_docs[i]["id"]})
            result_doc = {
                "rating": merge_docs[i]['rating'],
                "content": doc['content'],
                "title": doc['title'],
                "pos": merge_docs[i]['pos']
            }
            pprint(result_doc)
            result.append(result_doc)

        return result

    def analyze(self, word):
        segmenter = JiebaSegmenter()
        word_list = segmenter.segment(word, False)
        for word in word_list:
            print word
        return word_list