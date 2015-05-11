__author__ = 'haass'
import json
import string
#from nltk.corpus import words

#text = "wow dirty and slow  the floors felt like they had the days burger grease spilled all over and it took 30 m8n to get our take out order"
#words = text.split()

def cleanse_data(text_in):
    cleansed_text = text_in.replace('\n', ' ').replace('\r', '').lower()
    for punctuation in string.punctuation:
        cleansed_text = cleansed_text.replace(punctuation,"")
    return cleansed_text
pos_words_list = open("pos_words.txt", "r").read().split("\n")
neg_words_list = open("neg_words.txt", "r").read().split("\n")

pos_words = set()
neg_words = set()
for word in pos_words_list:
    pos_words.add(word)
for word in neg_words_list:
    neg_words.add(word)



def compute_score(words):
    score = 0
    for word in words:
        if word in pos_words:
            score += 1
        if word in neg_words:
         score -= 1
    return score



num_correct = 0
num_incorrect= 0

testing_data = open("yelp_rest_reviews.json", "r")
for line in testing_data.readlines():
    jitem = json.loads(line)
    text = cleanse_data(jitem.get("text"))
    #if len(text) > 300 or len(text) < 75:
    #	continue
    stars = jitem.get("stars")
    text_words = text.split()
    score = compute_score(text_words)
    if stars == 3:
	   continue;
    if (score > 0 and (stars == 5 or stars == 4)) or (score < 0 and (stars == 1 or stars == 2)):
        num_correct += 1
    else:
        num_incorrect += 1

print "fraction correct: ", (num_correct)/float(num_incorrect + num_correct)
print "num correct: ", num_correct, " num incorrect: ", num_incorrect


