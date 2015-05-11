import sys
import nltk

files = []

words_to_ignore = ["that","what","with","this","would","from","your","which","while","these"]
things_to_strip = [".",",","?",")","(","\"",":",";","'s"]
words_min_size = 4

def analyze(text, outputFile):
    words = text.lower().split()
    wordcount = {}
    for word in words:
        for thing in things_to_strip:
            if thing in word:
                word = word.replace(thing,"")
        if word not in words_to_ignore and len(word) >= words_min_size:
            if word in wordcount:
                wordcount[word] += 1
            else:
                wordcount[word] = 1

    sortedbyfrequency =  sorted(wordcount,key=wordcount.get,reverse=True)
    sortedbyfrequency = sortedbyfrequency[0:100]
    #allWords = ' '.join(sortedbyfrequency)

    #tokenizedWords = nltk.word_tokenize(allWords)


    output_keywords = open(outputFile, "w")

    n = 0;
    for word, pos in nltk.pos_tag(sortedbyfrequency):
         if pos in ['JJ', "JJR", "JJS"]: # feel free to add any other noun tags
            if n < 50:
                output_keywords.write("%s \n" % word)
                n += 1


pos_reviews = open("yelp_positive_reviews.txt", "r").read()
neg_reviews = open("yelp_negative_reviews.txt", "r").read()

analyze(pos_reviews, "pos_keywords_test.txt")
analyze(neg_reviews, "neg_keywords_test.txt")






