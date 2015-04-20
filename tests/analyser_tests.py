import unittest
import sys

# sys.path.append('../london')
from zeitgeist import tweet_processor




class TwitterStreamTests(unittest.TestCase):
    analyser = tweet_processor.TweetProcessor()

    def test_basic_comparison(self):
        self.assertGreater(
            self.analyser.calcScore("I Love Sausage"),
            self.analyser.calcScore("I Hate Sausage"),
            "Love should score higher than hate"
        )

    def test_compare_multiple_queries(self):
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
            self.compare_phrases(phrase[0], phrase[1])

    def test_can_compare_articles(self):
        bad_review = self.score_article_sentiment('tests/mortdecai-review.txt')
        good_review = self.score_article_sentiment('tests/nightcrawler-review.txt')
        print 'bad review score: ', bad_review
        print 'good review score: ', good_review

        self.assertGreater(good_review,bad_review)


    def compare_phrases(self, left, right):
        return self.assertGreater(
            self.analyser.calcScore(left),
            self.analyser.calcScore(right),
            left+' should score more highly than '+right
        )

    def score_article_sentiment(self, filename):
        score = 0
        with open(filename) as f:
            for line in f.readlines():
                score += self.analyser.calcScore(line)
        return score
if __name__ == '__main__':
    unittest.main()