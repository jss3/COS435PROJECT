__author__ = 'haass'
import nltk
import json
import string

#TODO: read these from files, set up yelp parser
#pos_tweets = [('I love this car', 'positive'),
#              ('This view is amazing', 'positive'),
#              ('I feel great this morning', 'positive'),
#             ('I am so excited about the concert', 'positive'),
#              ('He is my best friend', 'positive')]

def cleanse_data(text_in):
    cleansed_text = text_in.replace('\n', ' ').replace('\r', '').lower()
    for punctuation in string.punctuation:
        cleansed_text = cleansed_text.replace(punctuation,"")
    return cleansed_text

fh = open("yelp_positive_reviews.txt", "r")
pos_tweets = [tuple(line.strip().split(",")) for line in fh.readlines()]
fh.close()

fh = open("yelp_negative_reviews.txt", "r")
neg_tweets = [tuple(line.strip().split(",")) for line in fh.readlines()]
fh.close()

print "here1"

tweets = []
for (words, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

print "here2"
print len(tweets)

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    print "here3"
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    print "here4"
    return word_features

word_features = get_word_features(get_words_in_tweets(tweets))

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

training_set = nltk.classify.util.apply_features(extract_features, tweets)

classifier = nltk.NaiveBayesClassifier.train(training_set)

print "training complete, beginning testing"

num_correct = 0
num_incorrect= 0

testing_data = open("yelp_testing_data.json", "r")

for line in testing_data.readlines():
    jitem = json.loads(line)
    text = cleanse_data(jitem.get("text"))
    stars = jitem.get("stars")
    classified = classifier.classify(extract_features(text.split()))
    if (classified == "positive" and (stars == 5 or stars == 4)) or (classified == "negative" and (stars == 1 or stars == 2)):
        num_correct += 1
    elif stars == 3:
        continue
    else:
        num_incorrect += 1

fraction = num_correct /float(num_incorrect + num_correct)
print "fraction correct: ", fraction
print "num correct: ", num_correct, " num incorrect: ", num_incorrect


