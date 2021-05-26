#code adapted from "Natural Language Processing: Python and NLTK"
import json
from gensim import corpora, models, similarities
from gensim.models import Phrases, LdaModel, LsiModel, CoherenceModel
from itertools import chain
import nltk
from pprint import pprint
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from operator import itemgetter
import re
from nltk.tokenize import RegexpTokenizer
import logging
from gensim.models.callbacks import PerplexityMetric, ConvergenceMetric, CoherenceMetric
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.basicConfig(filename="model_callbacks.log",
                    format="%(asctime)s:%(levelname)s:%(message)s",
                    level=logging.NOTSET)

#inputfile = "MLMclean.txt"
# inputfile = "MLMnoEmojis.txt"
# topics = "MLM_Topics.txt"
# #wordtokenized = "MLM_WordTok.json"


#inputfile = "nonMLMclean.txt"
inputfile = "nonMLMnoemojis.txt"
topics = "nonMLM_Topics.txt"
# wordtokenized = "nonMLM_WordTok.json"

# #inputfile = "BeautyBrandsClean.txt"
# inputfile = "BeautyBrandsnoemojis.txt"
# topics = "BB_Topics.txt"
## wordtokenized = "BB_WordTok.json"


#### Preprocessing #####
punctuation = r'[!?.•;…:-_~*"()$%&=+\/-]'
usernameregex = r'(@\w*)'
hashtagregex = r'(#\w*)'

lemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')

with open(inputfile, encoding = "utf-8") as input:
    data = input.read().lower()

posts = data.split(";;;")

stopwordlist = set(stopwords.words('english'))

stopwordlist.update("want", "us", "go", "like", "would", "get", "let", "make", "one", "have", "give", "need")


cleanposts = []

for post in posts:
    clean = re.sub(punctuation, "", post)
    #seperate emojis from each other so they appear as seperate tokens later
    clean = re.sub("§§", "§ §", clean)
    clean = re.sub(hashtagregex, "", clean)
    clean = re.sub(usernameregex, "", clean)
    lemmatized = lemmatizer.lemmatize(clean)
    lowercase = lemmatized.lower()
    tokenized = tokenizer.tokenize(lowercase)
    #tokenized = lowercase.split()
    cleanposts.append(tokenized)



#Remove tokens that only consists of numbers
docs = [[token for token in post if not token.isnumeric()] for post in cleanposts]
# Remove words that are only one character
docs = [[token for token in doc if len(token) > 1] for doc in docs]

docs = [[token for token in doc if token not in stopwordlist] for doc in docs]

##############Preprocessing end #########################################

postnum = len(docs)

#taken from gensim documentation
# Add bigrams (frequency larger than 20)
bigram = Phrases(docs, min_count=20)
for idx in range(postnum):
    for token in bigram[docs[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            docs[idx].append(token)


# with open(wordtokenized, "w", encoding="utf-8") as output:
#     json.dump(docs, output)

dictionary = corpora.Dictionary(docs)

#Filter terms with fewer than n occurences and terms that appear in more than a certain percentage of posts
no_below = 50
no_above = 0.3

dictionary.filter_extremes(no_below=no_below, no_above=no_above)

#converting to a BOW-Model
corpus = [dictionary.doc2bow(doc) for doc in docs]

# #converting to a tf-idf-Model
#
# tfidf = models.TfidfModel(corpus)
# corpus_tfidf = tfidf[corpus]


#Latent Dirichlet allocation
# Make a index to word dictionary.
temp = dictionary[0]
id2word = dictionary.id2token
# chunksize controls how many documents are processed at a time in the training algorithm, may influence quality
chunksize = 300
num_topics = 7
iterations = 300
passes = 20
minimum_probability = 0.01

model = LdaModel(
    corpus=corpus,
    #corpus = corpus_tfidf,
    id2word=id2word,
    chunksize=chunksize,
    alpha='auto',
    eta='auto',
    iterations=iterations,
    num_topics=num_topics,
    passes=passes,
    minimum_probability = minimum_probability,
    #eval_every= 1
)
top_topics = model.top_topics(corpus)


# model_lsi = LsiModel(
#     corpus=corpus,
#     #corpus = corpus_tfidf,
#     id2word=id2word,
#     chunksize=chunksize,
#     num_topics=num_topics,
#     onepass = False
# )

#lsi_top_topics = model_lsi.show_topics(num_topics=10, log=False, formatted=True)

avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
print('Average topic coherence (LDA): %.4f.' % avg_topic_coherence)


# lsi_avg_topic_coherence = CoherenceModel(topics=lsi_top_topics[:10], texts=corpus, dictionary=dictionary, window_size=10).get_coherence()
# print('Average topic coherence (LSI): %.4f.' % lsi_avg_topic_coherence)


pprint(top_topics)

#pprint(lsi_top_topics)


with open(topics, "w", encoding= "utf-8") as output:

    print('Number of unique tokens: %d' % len(dictionary), file = output)
    print('Number of documents: %d' % len(corpus), file = output)
    print("Parameters: \n", file=output)
    print("Chunk Size: %d \n" % chunksize, file=output)
    print("Iterations: %d \n" % iterations, file=output)
    print("Passes: %d \n" % passes, file=output)
    try:
        print("Minimum Token Frequency: %d \n" % no_below, file=output)
        print("Maximum Token Frequency: " + str(no_above) + "\n", file=output)
    except:
        print("No minimum / maximum token frequency defined. \n", file = output)

    print("Topics for file " + inputfile + " using a Latent Dirichlet Allocation model: \n \n ", file=output)
    print('\n \n Average topic coherence: %.4f. \n \n ' % avg_topic_coherence, file=output)
    i=1
    for topic in top_topics:
        print("Topic Nr. "+ str(i) + "\n" + str(topic) +"\n \n", file=output)
        i+=1
    # print("Topics for file " + inputfile + " using a Latent Semantic Indexing model: \n \n ", file=output)
    # # print('\n \n Average topic coherence: %.4f. \n \n ' % lsi_avg_topic_coherence, file=output)
    # i=1
    # for topic in lsi_top_topics:
    #     print("Topic Nr. "+ str(i) + "\n" + str(topic) +"\n \n", file=output)
    #     i+=1
