import json
import string
import codecs

__author__ = 'haass'


def cleanse_data(text_in):
    cleansed_text = text_in.replace('\n', ' ').replace('\r', '').lower()
    for punctuation in string.punctuation:
        cleansed_text = cleansed_text.replace(punctuation,"")
    return cleansed_text

data_file = open('yelp_training_data.json')

pos_tweets = []
neg_tweets = []

for line in data_file.readlines():
    item = json.loads(line.encode("UTF-8"))
    text = cleanse_data(item.get("text"))
    if item.get("stars") == 5:
        pos_tweets.append(text)
    elif item.get("stars") <= 2:
        neg_tweets.append(text)


f = codecs.open('yelp_positive_reviews.txt',mode='w+', encoding="utf8")
for tweet in pos_tweets:
    f.write(tweet)
    f.write(',positive\n')

f.close()

f = codecs.open('yelp_negative_reviews.txt', mode='w+', encoding="utf8")
for tweet in neg_tweets:
    f.write(tweet)
    f.write(',negative\n')
f.close()
