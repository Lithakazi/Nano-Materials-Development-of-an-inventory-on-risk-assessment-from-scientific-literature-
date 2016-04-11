from __future__ import print_function
import nltk, sklearn, string, os
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from configparser import ConfigParser
import os
from string import punctuation
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.pyplot as plt

# read config file
config = ConfigParser()
config.read(r'datadir.ini')
direct = config.get('Path', 'Corpusdirectoy')

# Preprocessing text with NLTK package
# import nltk
token_dict = {}
stemmer = PorterStemmer()

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems
    # return tokens

def strip_punctuation(s):
    return''.join(c for c in s if c not in punctuation)

titles = []
titlespdf = []
for (subdir, dirs, files) in os.walk(direct):
    for i, f in enumerate(files):
        if f.endswith('.txt'):
            file_path = subdir + os.path.sep + f
            shakes = open(file_path, 'r', encoding='utf-8')
            text = shakes.read()
            no_punctuation = strip_punctuation(text)
            token_dict[f] = no_punctuation
            titles.append(f)

silho_score = []

true_k =100

print("\n Performing stemming and tokenization...")
vectorizer = TfidfVectorizer(tokenizer=tokenize, encoding='utf-8', stop_words='english')
X = vectorizer.fit_transform(token_dict.values())
tfidf_matrix = vectorizer.fit_transform(token_dict.values())

print("n_samples: %d, n_features: %d" % X.shape)
print()

###############################################################################

for i in range(2, true_k+1):
    km = KMeans(n_clusters=i, init='k-means++', max_iter=1000, n_init=1,verbose=0, random_state=100000, copy_x=True, n_jobs=1)# random_state=5000)
    y = km.fit(X)

    cluster_labels = km.fit_predict(X)
    silhouette_avg = silhouette_score(X, cluster_labels)
    # print("For n_clusters =", i,"The average silhouette_score is :", silhouette_avg)
    silho_score.append(silhouette_avg)

truek=[]
for i in range(2,true_k + 1):
    truek.append(i)
print(silho_score)

plt.plot(truek, silho_score, label='The average Silhouette Score for varying cluster numbers')
plt.xlabel('Number of K-means Clusters (K)')
plt.ylabel('Average Silhouette Score')
plt.show()