from pymongo import MongoClient
import string
# based on algorithm derived here: https://class.coursera.org/nlp/lecture/25


class NaiveBayes:

    p_neg = 0.5
    p_pos = 0.5
    POSITIVE = True
    NEGATIVE = False

    def calc_probability(self, text):
        dictionary = self.db['dictionary']
        pos_score = 1
        neg_score = 1
        words = text.split(" ")
        words = [w for w in words if w not in string.punctuation]
        entry_list = dictionary.find({"_id": {"$in": words}})
        for entry in entry_list:
            pos_score *= ((entry['value']['pos_freq']) + 1) / (1 + self.pos_class_size + self.vocabulary_size)
            neg_score *= ((entry['value']['neg_freq']) + 1) / (1 + self.neg_class_size + self.vocabulary_size)
        pos_score *= self.p_pos
        neg_score *= self.p_neg
        return pos_score > neg_score

    def __init__(self):
        mongo = MongoClient()
        self.db = mongo['zeitgeist']
        self.vocabulary_size = self.db.dictionary.count()
        self.pos_class_size = self.db.dictionary.find({"value.pos_freq": {"$exists": True, "$gt": 0}}).count()
        self.neg_class_size = self.db.dictionary.find({"value.neg_freq": {"$exists": True, "$gt": 0}}).count()
        print self.pos_class_size
        print self.neg_class_size
        print 'vocabulary size =', self.vocabulary_size
