from textblob import TextBlob


words_to_ignore = ["that","what","with","this","would","from","your","which","while","these"]
words_min_size = 4

def compute_score(sentence):
    new_sentence = sentence.split(',')[0]
    words = new_sentence.lower().split()
    new_sentence = ""
    for word in words:
        if word not in words_to_ignore and len(word) >= words_min_size:
            new_sentence += word
            new_sentence += " "
    testimonial = TextBlob(sentence)
    score = testimonial.sentiment.polarity
    #print score
    if (score > 0.25): return 'positive'
    elif(score > -.25): return 'neutral'
    else: return 'negative'


testing_data = open("yelp_rest_reviews.json", "r")
for line in testing_data.readlines():
    jitem = json.loads(line)
    text = cleanse_data(jitem.get("text").encode("UTF-8"))
    #if len(text) > 500:
    #   continue
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
