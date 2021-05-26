import re, nltk
from collections import Counter
from nltk import RegexpParser
from nltk import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import gensim
import spacy
import json


raw_input = "BBchunkprep.txt"
no_punct ="Cleantokens_BB.json"
output = "BBembeddings.txt"
savemodel = "BB_w2v.model"
### allquestions = "BBquestions.json"

# raw_input = "MLMchunkprep.txt"
# no_punct = "Cleantokens_MLM.json"
# output = "MLMembeddings.txt"
# savemodel = "MLM_w2v.model"
## allquestions = "MLMquestions.json"


# raw_input = "nonMLMchunkprep.txt"
# no_punct = "Cleantokens_Other.json"
# output = "nonMLMembeddings.txt"
# savemodel = "nonMLM_w2v.model"
## allquestions = "nonMLMquestions.json"




lemmatizer = WordNetLemmatizer()
punctuation = r'[!?,…⠀.;:-]'
usernameregex = r'(@\w*)'
hashtagregex = r'(#\w*)'
#wordlist = ["girl", "woman", "mom", "dad", "mother", "boss", "business", "success", "challenge", "mascara", "lipstick", "foundation", "pandemic", "growing","building", "empire", "god", "team", "friend", "healthy","health", "progress", "sale", "friendship" "support","power","love","work","family", "hair", "beauty", "earning", "pretty", "cancer", "black", "independent", "income", "faith"]
wordlist = ["girl", "woman", "mom", "dad", "mother", "baby", "babe", "sister", "brother", "boss", "friend", "team", "family", "yourself",
"business", "success", "challenge", "progress", "sale", "work", "income", "entrepreneur", "debt", "empire",
"mascara", "lipstick", "foundation", "hair",
"pandemic", "health", "healthy", "pretty", "strong", "care", "help",
"growing", "grow", "building", "build", "earning", "earn", "independent", "big", "pyramid",
"god", "lord", "faith", "hope", "pray", "grateful", "praise",
"love", "friendship", "support", "power", "beauty", "dream", "mindset", "inspiration"]
with open(raw_input, 'r+', encoding='utf-8') as file:
    raw = file.read()



sentences = sent_tokenize(raw)
tokenized_sentences = []
questions = []
for sentence in sentences:
    if "?" in sentence:
        questions.append(sentence)
    removeusernames = re.sub(usernameregex,"", sentence)
    removehashtags = re.sub(hashtagregex, "", removeusernames)
    clean = re.sub(punctuation, "", removehashtags)
    chkalphanum = re.search("\w", clean)
    if chkalphanum != None:
        lemmatized = lemmatizer.lemmatize(sentence)
        tokenized = clean.split()
        tokenized_sentences.append(tokenized)

# with open(allquestions, "w", encoding="utf-8") as outputfile:
#     json.dump(questions, outputfile)

#with open(testoutput, "w", encoding="utf-8") as outputfile:
#    json.dump(tokenized_sentences, outputfile)



#sg: 0 for CBOW, 1 for skip-gram
post_embeddings = gensim.models.Word2Vec(tokenized_sentences, size=100, window=5, min_count=4, workers=10, sg=1)


post_embeddings.save(savemodel)

print(type(post_embeddings))


tobeprinted = []
tobeprinted.append("Embeddings for file "+ raw_input + "\n")
for word in wordlist:
    tobeprinted.append("Token frequency for word " + word + ": ")
    word_freq = raw.count(word)
    tobeprinted.append(word_freq)
    tobeprinted.append("Embeddings for word "+ word +": \n")
    try:
        similar = post_embeddings.wv.most_similar(word, topn = 30)
        tobeprinted.append(similar)
        tobeprinted.append("\n\n")
    except:
        tobeprinted.append("Word not in vocabulary \n\n")

tobeprinted.append("Word Similarities based on file " + raw_input + "\n")

j=0
while j < len(wordlist):
    word=wordlist[j]
    i=j+1
    while i < len(wordlist):
        try:
            compare = post_embeddings.wv.similarity(w1 = word, w2 = wordlist[i])
            tobeprinted.append("Similarity between " + word + " and " + wordlist[i] +": \n")
            tobeprinted.append(compare)
            tobeprinted.append("\n\n")
        except:
            pass
        i+=1
    j+=1



with open(output, "w", encoding="utf-8") as outputfile:
    for item in tobeprinted:
        print(item, file=outputfile)
