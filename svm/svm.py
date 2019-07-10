import operator
from pandas import json
from sklearn.linear_model import LogisticRegression

from sklearn import svm
import pylab as pl
import numpy as np
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV

stopwords = [ "above", "across", "after", "afterwards","two", "un", "under", "until", "up", "upon", "us","de", "describe", "detail", "do","&amp;", "again", "against", "all", "almost", "alone", "along",
             "already","fire", "first", "five", "for", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything",
             "anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand",
             "behind", "being",  "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else",
             "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find",
              "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has",
             "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however",
             "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd",
             "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name",
             "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off",
             "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per",
             "perhaps","a", "about", "above", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side",
             "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system",
             "take", "ten", "than", "that", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co",
             "con", "could", "couldnt", "cry", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein",
             "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together",
             "too", "top", "toward", "towards", "twelve", "twenty",  "very", "via", "was", "we", "well", "were",
             "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which",
             "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours",
             "yourself", "yourselves", "the"]

tweet= []
for line in open('labeled_tweets.txt').readlines():
    items = line.split(',')
    tweet.append([int(items[0]), items[1].lower().strip()])

# Extract the vocabulary of keywords
vocabulary = dict()

for class_label, text in tweet:
    for t in text.split():
        t = t.lower()
        if len(t) > 2 and t not in stopwords:
            if vocabulary.has_key(t):
                vocabulary[t] = vocabulary[t] + 1
            else:
                vocabulary[t] = 1
# Remove terms whose frequencies are less than a threshold (e.g., 15)
vocabulary = {t: freq for t, freq in vocabulary.items() if freq > 15}
sorted_vocab = sorted(vocabulary.items(), key=operator.itemgetter(1), reverse=True)[:10]
#print sorted_vocab
d = dict(sorted_vocab)

for key, value in d.iteritems():
    print key,value
# Generate an id (starting from 0) for each term in vocab
vocabulary = {t: idx for idx, (t, freq) in enumerate(vocabulary.items())}

# Generate X and y
X = []
y = []
for class_label, text in tweet:
    x = [0] * len(vocabulary)
    terms = [t for t in text.split() if len(t) > 2]
    for t in terms:
        if vocabulary.has_key(t):
            x[vocabulary[t]] += 1
    y.append(class_label)
    X.append(x)

# 10 folder cross validation to estimate the best w and b
svc = svm.SVC(kernel='linear')
Cs = range(1, 20)
clf = GridSearchCV(estimator=svc, param_grid=dict(C=Cs), cv = 10)
clf.fit(X, y)

print "      "
print "X"
a = np.array([X])
print a
print "y" # predict the class labels of new tweets
print np.array(y)

tweet = []
for line in open('unlabeled_tweets.txt').readlines():
    tweet.append(line)


X = [] # Generate X for testing tweets
for text in tweet:
    x = [0] * len(vocabulary)
    terms = [t for t in text.split() if len(t) > 2]
    for t in terms:
        if vocabulary.has_key(t):
            x[vocabulary[t]] += 1
    X.append(x)


svc = svm.SVC(kernel='linear')
Cs = range(1, 20)
clf = GridSearchCV(estimator=svc, param_grid=dict(C=Cs), cv = 10)
clf.fit(X, y)
y = clf.predict(X)

print " Model Accuracy of the SVM Model : "
print clf.best_score_
print " Best Parameters of the SVM Model : "
print clf.best_params_['C']

# print 100 example tweets and their class labels
with open('predicted_tweets.txt', 'a') as f:
    for idx in range(500):
        f.write(str(y[idx]) + ", " + tweet[idx])

print "See predicted_tweets.txt"
print sum(y), len(y)