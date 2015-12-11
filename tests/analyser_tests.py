import unittest
import os

# sys.path.append('../london')
from zeitgeist.classifiers.naive_bayes_classifier import NaiveBayes


class TwitterStreamTests(unittest.TestCase):
    classifier = NaiveBayes()

    def test_basic_comparison(self):
        self.assertTrue(self.classifier.calc_probability("I Love Sausage"))
        self.assertFalse(self.classifier.calc_probability("I Hate Sausage"))

    def test_compare_multiple_queries(self):
        total=0
        false_positives=0
        false_negatives=0
        phrases = [
            ["The football was excellent tonight", "The football was dismal tonight"],
            ["I like both of these guys", "They were both uninteresting fellows"],
            ["Debbie is an exciting raconteur", "Debbie's stories are often too long"],
            ["This cheese is really tasty", "This cheese is awful"],
            ["That film was great", "What a rubbish film"],
            ["Secret cinema, I'm so excited", "Wow, that was really dull"],
            ["Elon Musk, what a legend", "Jeff Bezos can suck it"],
            ["Had a great time at TGI Fridays", "Don't go to Mcdonalds. The food is terrible"],
        ]

        for phrase in phrases:
            if not self.classifier.calc_probability(phrase[0]):
                false_negatives += 1
            total += 1
            if self.assertFalse(self.classifier.calc_probability(phrase[1])):
                false_positives += 1
            total += 1

            print "False negatives %s, false positives %s" % (false_negatives, false_positives)
            self.assertGreater(0.6, false_positives/total)
            self.assertGreater(0.6, false_negatives/total)

    def run_against_training_set(self, dir, expected_outcome):
        incorrect_matches = 0
        dir_path = 'resources/txt_sentoken/'+dir
        for f in os.listdir(dir_path):
            if self.assess_article_sentiment(dir_path+'/'+f) != expected_outcome:
                # print f, 'was not correctly classified as', expected_outcome
                incorrect_matches += 1

        return incorrect_matches

    def test_can_compare_articles(self):
        # self.assertFalse(self.assess_article_sentiment('tests/mortdecai-review.txt'))
        # self.assertTrue(self.assess_article_sentiment('tests/nightcrawler-review.txt'))
        print self.run_against_training_set('neg', False), 'incorrectly classified negatives'
        print self.run_against_training_set('pos', True), 'incorrectly classified positives'

    def compare_phrases(self, left, right):
        return self.assertGreater(
            self.classifier.calcScore(left),
            self.classifier.calcScore(right),
            left+' should score more highly than '+right
        )

    def assess_article_sentiment(self, filename):
        with open(filename) as f:
            text = f.read()
            return self.classifier.calc_probability(text)

if __name__ == '__main__':
    unittest.main()