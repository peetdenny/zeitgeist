import unittest
from zeitgeist.classifiers.naive_bayes_classifier import NaiveBayes


class TwitterStreamTests(unittest.TestCase):

    def test_probability_calc(self):
        naive = NaiveBayes()
        self.assertEqual(NaiveBayes.NEGATIVE, naive.calc_probability("Jim was a terrible author, and a shabby shot"))
        self.assertEqual(NaiveBayes.NEGATIVE, naive.calc_probability("Dandilions taste like a horrible housefire with piss on them"))
        self.assertEqual(NaiveBayes.POSITIVE, naive.calc_probability("Jeffery sucked at the delicious milkshake. He thought the date was going well"))
        self.assertEqual(NaiveBayes.POSITIVE, naive.calc_probability("The sunset looks like a beautiful painting in a peaceful house"))



    if __name__ == '__main__':
        unittest.main()