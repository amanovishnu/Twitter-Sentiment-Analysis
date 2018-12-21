import logging
from FileOps import readExcelFile
import Classifier

TRAINING_DATA_FILE = '../data/training-Obama-Romney-tweets.xlsx'
TEST_DATA_FILE = '../data/testing-Obama-Romney-tweets-spring-2013.xlsx'

def word_feats(words):
    return dict([(word, True) for word in words])

if __name__ == '__main__':    
    nbClassifier = Classifier.NBClassifier()

    training_tweets = readExcelFile(TRAINING_DATA_FILE, 'Obama', 'train') + readExcelFile(TRAINING_DATA_FILE, 'Romney', 'train')
    training_feats = nbClassifier.get_feats(word_feats, training_tweetstest_tweets = readExcelFile(TEST_DATA_FILE, 'Obama', 'test') + readExcelFile(TEST_DATA_FILE, 'Romney', 'test')
    test_feats = nbClassifier.get_feats(word_feats, test_tweets)

    nbClassifier.train(training_feats, test_feats)
    

    nbClassifier.accuracy()

      nbClassifier.stats()
    nbClassifier.confusion_matrix()
