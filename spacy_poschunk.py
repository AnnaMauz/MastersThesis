import re, nltk
from collections import Counter
import gensim
import spacy
import json
import pandas as pd
from statistics import mean



nlp = spacy.load("en_core_web_sm")

def chkalphanum(string):
    test = re.search("\w", string)
    if test != None:
        return True
    else:
        return False


raw_input = "MLMnoEmojis.txt"
nounchunks = "MLMNPchunks.json"
nouns = "MLMnouns.json"
adjchunks = "MLMadjectivesoverview.json"
vbchunks = "MLMverbsoverview.json"
pronounstats = "MLMpronounsoverview.json"

# raw_input = "BeautyBrandsnoemojis.txt"
# nounchunks = "BBNPchunks.json"
# nouns = "BBnouns.json"
# adjchunks = "BBadjectivesoverview.json"
# vbchunks = "BBverbsoverview.json"
# pronounstats = "BBpronounsoverview.json"

# raw_input = "nonMLMnoemojis.txt"
# nounchunks = "nonMLMNPchunks.json"
# nouns = "nonMLMnouns.json"
# adjchunks = "nonMLMadjectivesoverview.json"
# vbchunks = "nonMLMverbsoverview.json"
# pronounstats = "nonMLMpronounsoverview.json"


usernameregex = r'(@\w*)'
hashtagregex = r'(#\w*)'
#punctuation not relevant for POS detection
punctuation = r'[•…_~*"()$€£%&=+]'

with open(raw_input, encoding = "utf-8") as input:
    text = input.read().lower()

text = re.sub(hashtagregex, "", text)
text = re.sub(usernameregex, "", text)
text = re.sub(punctuation, "", text)

posts = text.split(";;;")




processedposts = []

for post in posts:
    doc = nlp(post)
    processedposts.append(doc)


#find and count noun chunks
noun_chunks_all = []
for post in processedposts:
    for chunk in post.noun_chunks:
        chkalphanum = re.search("\w", chunk.text)
        if chkalphanum != None:
            noun_chunks_all.append(chunk.text)
nounchunk_count = Counter(noun_chunks_all)
nounchunks_top = nounchunk_count.most_common(150)

with open(nounchunks, "w", encoding = "utf-8") as output:
    i = 0
    for item in nounchunks_top:
        i +=1
        print(str(i) + ". " + str(item), file = output)
    #json.dump(nounchunk_count.most_common(150), output)



nouns_all = []
#find and count adjective chunks

adj_chunks_all = []
adjbase = []
comparatives = []
superlatives = []

#list for verb forms
VPs_all = []

pronouns = []

for post in processedposts:
    for token in post:
        #Verbs
        if token.pos_ == "VERB" and token.is_stop == False:
            #VPs_all.append(token.text)
            VPs_all.append(token.lemma_)
        elif token.pos_ == "NOUN":
            #nouns_all.append(token.text)
            nouns_all.append(token.lemma_)
        elif token.pos_ == "PRON":
            pronouns.append(token.text)
        #Adjectives
        elif token.pos_ == "ADJ":
            adj_chunks_all.append(token.text)
            if token.tag_ == "JJ":
                adjbase.append(token.text)
            if token.tag_ == "JJR":
                comparatives.append(token.text)
            if token.tag_ == "JJS":
                superlatives.append(token.text)

nouns_count = Counter(nouns_all)
nouns_top = nouns_count.most_common(150)

with open(nouns, "w", encoding = "utf-8") as output:
    i = 0
    for item in nouns_top:
        i +=1
        print(str(i) + ". " + str(item), file = output)
    #json.dump(nouns_top, output)

adjbase_count = Counter(adjbase)
comparative_count = Counter(comparatives)
superlative_count = Counter(superlatives)

top_adj = adjbase_count.most_common(100)
top_comp = comparative_count.most_common(25)
top_sup = superlative_count.most_common(25)

with open(adjchunks, "w", encoding="utf-8") as output:
    output.write("Token frequency of all adjectives: " + str(len(adj_chunks_all)) + "\n")
    output.write("Token frequency positive forms: " + str(len(adjbase)) + "\n")
    output.write("Token frequency comparative forms: " + str(len(comparatives)) + "\n")
    output.write("Token frequency superlative forms: " + str(len(superlatives)) + "\n")
    output.write("Most Common Positives: \n")
    i = 0
    for item in top_adj:
        i +=1
        print(str(i) + ". " + str(item), file = output)
    #json.dump(adjbase_count.most_common(50), output)
    output.write("\n\n")
    output.write("Most Common Comparatives: \n")
    i = 0
    for item in top_comp:
        i +=1
        print(str(i) + ". " + str(item), file = output)
    #json.dump(comparative_count.most_common(25), output)
    output.write("\n\n")
    output.write("Most Common Superlatives: \n")
    i = 0
    for item in top_sup:
        i +=1
        print(str(i) + ". " + str(item), file = output)
    #json.dump(superlative_count.most_common(25), output)
    output.write("\n\n")


#count and print most common verbs

vb_count = Counter(VPs_all)
top_vb = vb_count.most_common(50)

with open(vbchunks, "w", encoding="utf-8") as output:
    output.write("Token frequency of all verbs: " + str(len(VPs_all)) + "\n \n")
    output.write("Most common verbs: \n")
    i = 0
    for item in top_vb:
        i +=1
        print(str(i) + ". " + str(item), file = output)
    #json.dump(vb_count.most_common(50), output)


#count and print most common pronouns
pron_count = Counter(pronouns)
top_pron = pron_count.most_common(35)

with open(pronounstats, "w", encoding ="utf-8") as output:
    output.write("Most common pronouns: \n")
    i = 0
    for item in top_pron:
        i +=1
        print(str(i) + ". " + str(item), file = output)
    #json.dump(pron_count.most_common(25), output)


# #rate concreteness of nouns
# df= pd.read_excel('13428_2013_403_MOESM1_ESM.xlsx', header = 0, usecols = "A,C", names = ["word", "conc"])
#
# concreteness = []
# #print(df)
# #print(type(nouns_top))
# i= 0
# nounlist = []
# for item in nouns_top:
#     nounlist.append(nouns_top[i][0])
#     i+=1
#
# for item in nounlist:
#     try:
#         conc_val = df[df.word == item].values[0]
#         concreteness.append(conc_val[1])
#     except:
#         pass
# print(len(concreteness))
#
# avg_concreteness = mean(concreteness)
#
# print("Average concreteness of most common nouns: " + str(avg_concreteness))
