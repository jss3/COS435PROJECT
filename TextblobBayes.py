from textblob.classifiers import NaiveBayesClassifier
import json
import string
import pickle


def cleanse_data(text_in):
    cleansed_text = text_in.replace('\n', ' ').replace('\r', '').lower()
    for punctuation in string.punctuation:
        cleansed_text = cleansed_text.replace(punctuation,"")
    return cleansed_text

fh = open("yelp_positive_reviews.txt", "r")
pos_tweets = [tuple(line.decode('utf8', 'ignore').strip().split(",")) for line in fh.readlines()]
fh.close()

fh = open("yelp_negative_reviews.txt", "r")
neg_tweets = [tuple(line.decode('utf8', 'ignore').strip().split(",")) for line in fh.readlines()]
#print neg_tweets
fh.close()

training_data = []
for (words, sentiment) in pos_tweets + neg_tweets:
    review_filtered = ""
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    for word in words_filtered:
        review_filtered += " "
        review_filtered += word
    training_data.append((review_filtered, sentiment))

print "training now!"

#print training_data
classifier = NaiveBayesClassifier(training_data)
f = open('my_classifier_textblob.pickle', 'wb')
pickle.dump(classifier, f)
f.close()

print "training complete, beginning testing"

testing_data = open("yelp_testing_data.json", "r")

n = 0
num_correct = 0
num_incorrect= 0

for line in testing_data.readlines():
    jitem = json.loads(line)
    text = cleanse_data(jitem.get("text"))
    stars = jitem.get("stars")
    classified = classifier.classify(text.decode('utf8', 'ignore').split)
    if (classified == "positive" and (stars == 5 or stars == 4)) or (classified == "negative" and (stars == 1 or stars == 2)):
        num_correct += 1
    elif stars == 3:
        continue
    else:
        num_incorrect += 1

fraction = num_correct /float(num_incorrect + num_correct)
print "fraction correct: ", fraction
print "num correct: ", num_correct, " num incorrect: ", num_incorrect
